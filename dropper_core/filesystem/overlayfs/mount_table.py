
import re

DIR_REGEX = r'[^\s]+'
MAIN_REGEX_RAW = r'^(?P<device>%s) on (?P<point>%s) type (?P<fs_type>[\.\-,\w]+) \((?P<raw_options>.*)\)$'
MAIN_REGEX = MAIN_REGEX_RAW % (DIR_REGEX, DIR_REGEX)
MAIN_REGEX_OBJ = re.compile(MAIN_REGEX)

def match_entry_line(str_to_match, regex_obj=MAIN_REGEX_OBJ):
	''' Does a regex match of the mount point string '''
	match_obj = regex_obj.match(str_to_match)
	if not match_obj:
		raise UnrecognizedMountTableEntry('Line "%s" is not recognised' % (str_to_match))
	return match_obj.groupdict()

def split_mount_opts(mount_opts_str):
	split_opts = mount_opts_str.split(",")
	return map(lambda a: a.split("="), split_opts)

class UnrecognizedMountTableEntry(Exception):
	pass

class MountTableEntry(object):

	@classmethod
	def from_str(cls, entry_str=None):
		entry_dict = match_entry_line(entry_str)
		opts  = split_mount_opts(entry_dict['raw_opts'])
		return cls(entry_dict['point'], entry_dict['device'], entry_dict['fs_type'], opts)

	def __init__(self, mount_point, device, fs_module, opts):
		self.mount_point = mount_point
		self.device = device
		self.fs_module = fs_module
		self.opts = opts

class MountTable(object):

	@classmethod
	def from_str(cls, list_str, entry_cls=None):
		entry_cls = entry_cls or MountTableEntry
		# remove any trailing new lines
		list_str = list_str.strip()
		entry_list = map(entry_cls.from_str, list_str.splitlines())
		return cls(entry_list)

	@classmethod
	def load(cls, entry_cls=None):
		rsp = subwrap.run(['mount'])
		return cls.from_str(rsp.std_out.decode('utf-8'))

	def __init__(self, entry_list):
		self._entries = entry_list

	def as_list(self, fs_module=None):
		''' List mount entries '''
		entries = self._entries
		if fs_module:
			entries = filter(lambda a: a.fs_module == fs_module, entries)
		return entries

	def list_mount_points(self):
		return map(lambda a: a.mount_point, self._entries)

	def find_by_mount_point(self, mp):
		out = []
		for entry in self._entries:
			if entries.mount_point == mount_point:
				out.append(entry)
		return out

	def is_mounted(self, mount_point):
		res = self.find_by_mount_point(mp=mount_point)
		# something is at least mounted
		return len(res) != 0

