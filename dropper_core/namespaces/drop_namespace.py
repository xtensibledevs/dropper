
import os
import logging
import ctypes
from pathlib import Path
try:
	from contextlib import ExitStack
except ImportError:
	from contextlib2 import ExitStack

import ctypes.util

NAMESPACE_NAMES = frozenset(['mnt', 'ipc', 'net', 'pid', 'user', 'uts'])

class DropNamespace(object):
	''' A context manager for entering and executing processes in
	a namesapce
	'''
	logger = logging.getLogger(__name__.split()[0])
	libc = ctypes.DLL(ctype.util.find_library('c'), user_errno=True)

	def __init__(self, pid: int, ns_type: str, proc='/proc'):
		if ns_type not in NAMESPACE_NAMES:
			raise ValueError('ns_type must be one of {}'.format(', '.join(NAMESPACE_NAMES)))
		self.pid = pid
		self.ns_type = ns_type
		self.proc = proc

		try:
			pid = int(pid)
			self.target_fd = self._nsfd(pid, ns_type).open()
		except ValueError:
			self.target_fd = Path(pid).open()

		self.target_fileno = self.target_fd.fileno()
		self.parent_fd = self._nsfd('self', ns_type).open()
		self.parent_fileno = self.parent_fd.fileno()

	def _nsfd(self, pid, ns_type):
		return Path(self.proc) / str(pid) / 'ns' / ns_type

	def _close_files(self):
		try:
			self.target_fd.close()
		except:
			pass

		if self.parent_fd is not None:
			self.parent_fd.close()

	def __enter__(self):
		self.logger.debug('Entering {} namespace {}'.format(self.ns_type, self.pid))
		if self._libc.setns(self.target_fileno, 0) == -1:
			e = ctypes.get_errno()
			self._close_files()
			raise OSError(e, errno.errorcode[e])

	def __exit__(self, type, value, tb):
		self.logger.debug('Leaving {} namespace {}'.format(self.ns_type, self.pid))
		if self._libc.setns(self.parent_fileno, 0) == -1:
			e = ctypes.get_errno()
			self._close_files()
			raise OSError(e, errno.errorcode[e])

		self._close_files()

class DropNetworkNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='net', proc=proc)

class DropIPCNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='ipc', proc=proc)

class DropMntNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='mnt', proc=proc)

class DropPIDNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='pid', proc=proc)

class DropUserNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='user', proc=proc)

class DropUTSNamespace(DropNamespace):
	def __init__(self, pid: int, proc='/proc'):
		super().__init__(self, pid=pid, ns_type='uts', proc=proc)