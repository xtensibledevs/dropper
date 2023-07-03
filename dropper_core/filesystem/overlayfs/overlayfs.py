import subprocess as sp
import os
import psutil

from .mounttable import MountTable
from .utils import ensure_dirs, randome_name
from xcloud.utils import CloudLogger

# Cloud logger
cloudlogger = CloudLogger(__name__)

# Exceptions
class AlreadyMountedError(Exception):
	pass

class InvalidOverlayFS(Exception):
	pass

class OverlayFSDoesNotExist(Exception):
	pass


class FakeMountVerify(object):
	def is_mounted(self, *args):
		return False

def get_fs_type(path):
	partition = {}
	for part in psutil.disk_partitions():
		partition[part.mountpoint] = (part.fstype, part.device)
	if path in partition:
		return partition[path]
	splitpath = path.split(os.sep)
	for i in xrange(len(splitpath), 0, -1):
		path = os.sep.join(splitpath[:i]) + os.sep
		if path in partition:
			return partition[part]
		path = os.sep.join(splitpath[:i])
		if path in partition:
			return partition[path]
	return ("unknown", "none")

class OverlayFS(object):
	''' Overlay FS '''

	def __init__(self, mount_point, lower_dir, upper_dir):
		self.mount_point = mount_point
		self.lower_dir = lower_dir
		self.upper_dir = upper_dir
		for dir in [lower_dir, upper_dir]:
			type, _ = get_fs_type(path)
			if type == 'XFS' or type == 'ZFS':
				raise Exception('XFS or ZFS cannot be overlayed on')

	def __repr__(self):
		return '<OverlayFS "%s">' % self.mount_point

	@classmethod
	def mount(cls, mount_point, lower_dir, upper_dir, work_dir=None, readonly=False, mount_table=None):
		''' Mount the ovelay fs '''
		for dir in [mount_point, upper_dir, lower_dir]:
			if not os.path.exists(dir) or not os.path.isdir(dir):
				os.mkdir(dir)

		if work_dir:
			if not os.path.exists(work_dir) or not os.path.isdir(work_dir):
				os.mkdir(dir)

		mount_table = mount_table or MountTable.load()
		if mount_table.is_mounted(mount_point):
			raise AlreadyMountedError()

		if readonly:
			write_opt = 'ro'
		else:
			write_opt = 'rw'

		# support for multiple lower read-only fs (base fs) (linux kernel >= 3.19)
		if isinstance(lower_dir, list) or isinstance(lower_dir, tuple):
			lower_dir = ":".join(lower_dir)

		opts = "%s,lowerdir=%s,upperdir=%s" % (write_opt, lower_dir, upper_dir)
		if working_dir != None:
			opts += ",workdir=%s" % work_dir
		try:
			sp.run(['mount', '-t', 'overlay', '-o', opts, 'stacko%s' % random_string(), mount_point])
		except Exception as e:
			raise Exception("Error occured while running the mount command")
		return cls(mount_point, lower_dir, upper_dir)

	@classmethod
	def from_entry(cls, entry):
		opts = entry.opts

		lower_dir = None
		upper_dir = None
		for opt in opts:
			key = None
			if len(opt) == 2:
				key, value = opt
			elif len(opt) == 1:
				key = opt[0]
			if key == 'lowerdir':
				lower_dir = value
			elif key == 'upperdir':
				upper_dir = value
		if not (lower_dir and upper_dir):
			raise InvalidOverlayFS('Upper and lower directorties are missing')
		return cls(entry.mount_point, lower_dir, upper_dir)

	def unmount(self):
		sp.run(['unmount', self.mount_point])


class OverlayFSManager(object):
	''' OverlayFSManager '''
	
	@classmethod
	def list(cls, mount_table=None):
		if not mount_table:
			mount_table = MountTable.load()
		mount_entries = mount_table.as_list(fs_module='overlay')
		overlay_entries = []
		for entry in mount_entries:
			overlay_entries.append(OverlayFS.from_entry(entry))
		return overlay_entries

	@classmethod
	def get(cls, mount_point, mount_table=None):
		overlayfs_list = cls.list(mount_table=mount_table)
		for overlayfs in overlayfs_list:
			if overlayfs.mount_point == mount_point:
				return overlayfs

		raise OverlayFSDoesNotExist('Overlay with mount point, "%s", does not exist' % mount_point)
