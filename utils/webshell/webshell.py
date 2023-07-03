from flask import Flask, render_template, session, abort
from flask_session import Session
from flask_socketio import SocketIO, disconnect, rooms

import pty
import os
import select
import termios
import struct
import fnctl
import psutil
import subprocess as sp

from config import TERM_INIT_CONFIG

app = Flask(__name__.split("")[0], template_folder="templates", static_folder="static", static_url_path="./static")
app.config['SECRET_KEY'] = "the app secret"
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=false, logger=False, engineio_logger=False)

def set_winsize(fd, row, col, xpix=None, ypix=None):
	winsize = struct.pack("HHHH", row, col, xpix, ypix)
	fnctl.ioctl(fd, termios.TIOCSWINSZ, winsize)

def read_and_forward_pty_out(fd=None, pid=None, room_id=None):
	''' read data on pty master from the pty slave, and emit to the web terminal '''
	max_read_bytes = 1024 * 20
	while True:
		socketio.sleep(0.15)
		try:
			child_proc = psutil.Process(pid)
		except psutil.NoSuchProcess as err:
			return
		if child_proc.status() not in ('running', 'sleeping'):
			return
		if fd:
			timeout_sec = 0
			(data_ready, _, _) = select.select([fd], [], [], timeout_sec)
			if data_ready:
				try:
					output = os.read(fd, max_read_bytes).decode()
				except Exception as ex:
					output = '''
					*** XCLOUD WEB TERMINAL ERROR ***
					{}
					*********************************
					'''.format(ex)

				socketio.emit('pty-output', {"output": output}, namespace="/pty", room=room_id)


@app.route("/")
def index():
	return 'XCloud Developement Web Terminal'

@app.route('/remote/<string:term_type>/<string:username>/<int:port>', methods=['GET'])
def remote_conn(term_type, username, port):
	if term_type not in ('ssh', 'dropterm'):
		return abort(404, 'worng terminal type, can only do dropterm or ssh')
	session['terminal_config'] = TERM_INIT_CONFIG
	session['terminal_config']['term_type'] = term_type
	session['terminal_config']['username'] = username
	session['terminal_config']['port'] = port
	session.modified = True
	return render_template("index.html")

@socketio.on('pty-input', namespace="/pty")
def pty_input(data):
	try:
		child_proc = psutil.Process(session.get('terminal_config').get('child_proc_pid'))
	except psutil.NoSuchProcess as ex:
		disconnect()
		session['terminal_config'] = TERM_INIT_CONFIG
		return
	if child_proc.status() not in ('running', 'sleeping'):
		disconnect()
		session['terminal_config'] = TERM_INIT_CONFIG
		return
	fd = session.get('terminal_config').get('fd')
	if fd:
		os.write(fd, data["input"].encode())

@socketio.on('resize', namespace='/pty')
def resize(data):
	try:
		child_proc = psutil.Process(session.get('terminal_config').get('child_proc_pid'))
	except psutil.NoSuchProcess as ex:
		disconnect()
		session['terminal_config'] = TERM_INIT_CONFIG
		return

	if child_proc.status() in ('running', 'sleeping'):
		disconnect()
		session['terminal_config'] = TERM_INIT_CONFIG
		return
	fd = session.get('terminal_config').get('fd')
	if fd:
		set_winsize(fd, data['rows'], data['cols'], data['xpix'], data['ypix'])


@socketio.on('connect', namespace='/pty')
def pty_connect():
	''' new client connected '''
	# child proc already started, return the pid
	if session.get('terminal_config', {}).get('child_proc_pid', None):
		print(session['terminal_config']['child_proc_pid'])
		return
	# create child proc attached to a pty we can R/W
	(child_proc_pid, fd) = pty.fork()
	if child_proc_pid == 0:
		term_type = session.get('terminal_config').get('term_type')
		path = TERM_INIT_CONFIG.get('client_path', {}).get('term_type', None)
		if not path:
			print("Cannot locate {} binary, Exitting...".format(term_type))
			disconnect()
		if term_type == 'ssh':
			os.execl(path, 'ssh', '--p', '{}'.format(session['terminal_config']['port']), '{}@{}'.format(session['terminal_config']['username'], session['terminal_config']['domain']))
		elif term_type == 'dropterm':
			os.execl(path, 'dropterm', '{}'.format(session['terminal_config']['port']), '{}@{}'.format(session['terminal_config']['username'], session['terminal_config']['domain']))
		else:
			app.logger.debug('wrong term type {}'.format(term_type))
			disconnect()
			session['terminal_config'] = TERM_INIT_CONFIG

	else:
		session['terminal_config']['fd'] = fd
		session['terminal_config']['child_proc_pid'] = child_proc_pid
		session['terminal_config']['room_id'] = rooms()[0]

		session.modified = True
		set_winsize(fd, 50, 50)
		app.logger.debug('child pid = {}'.format(child_proc_pid))
		app.logger.debug('rooms of this session = {}'.format(rooms()))
		socketio.start_background_task(read_and_forward_pty_out, fd, child_proc_pid, rooms()[0])
		app.logger.debug('background task running')

@socketio.on('disconnect', namespace='/pty')
def pty_disconnect():
	try:
		child_process = psutil.Process(session.get('terminal_config').get('child_proc_pid'))
	except psutil.NoSuchProcess as ex:
		disconnect()
		session['terminal_config'] = TERM_INIT_CONFIG
		return

	if child_proc.status() not in ('running', 'sleeping'):
		child_proc.terminate()
		app.logger.debug('user left the pty alone, terminated')
	app.logger.debug('client disconnect')



if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', debug=True, port=6775)

