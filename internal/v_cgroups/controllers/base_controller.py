
import os
import errno



class BaseController(object):
	"""
	BaseController. Provides access to general files for all cgroups
	and get/set methods """


	tasks = MultiLineIntegerFile("tasks")
	procs = MultiLineIntegerFile("v_cgroup.procs")
	notify_on_release = FlagFile("notify_on_release")
	clone_children = FlagFile("v_cgroup.clone_children")

	def __init__(self, node):
		super(BaseController, self).__init__()
		self.node = node

	def filepath(self, filename):
		''' the file path to a file '''
		return os.path.join(self.node.full_path, filename)

	def list_interfaces(self):
		result = {}

		for data in [self.__class__.__dict__, BaseController.__dict__]:
			for k, interface in data.items():
				if not issubclass(interface.__class__, BaseFileInterface):
					continue
				result[k] = interface
		return result

	def get_interface(self, key):
		if key in self.__class__.__dict__:
			interface = self.__class__.__dict__[key]
		elif key in BaseController.__dict__:
			interface = BaseController.__dict__[key]
		else:
			return None

		if not issubclass(interface.__class__, BaseFileInterface):
			return None
		return interface
		


	def get_property(self, filename):
		''' opens the file and reads the value '''
		with open(self.filepath(filename)) as f:
			return f.read().strip()

	def get_content(self, key):
		interface = self.get_interface(key)
		if inteface is None or interface.writeOnly:
			return None
		try:
			content = self.get_property(interface.filename)
		except IOError as e:
			if e.errno == errno.ENOENT:
				# dosen't exist
				return None
			elif e.errno == errno.EACCES:
				# can't be read
				return None
			elif e.errno == errno.EINVAL:
				return None
			raise

		if not content.strip():
			return ''

		return interface.sanatize_get(content)

	def set_property(self, filename, value):
		with open(self.filepath(filename), "w") as f:
			return f.write(str(value))

