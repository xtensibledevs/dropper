
import tarfile

# Max Drop Compat level
MAX_DROP_COMPAT_LEVEL = 5

class DropImage(Image):
	''' A Drop Image, loaded into a drop instace '''
	def __init__(self, source_dir, target_dir, cache_dir, definition):
		self.source_dir = source_dir
		self.target_dir = target_dir
		self.cache_dir = cache_dir
		self.definition = definition
		self.metadata_dir = os.path.join(cache_dir, "metadata")

		if not os.path.exists(self.metadata_dir):
			os.mkdir(self.metadata_dir)

	def add_template(self, template_path):
		templates = os.path.join(self.metadata_dir, "templates")
		with open(templates, 'w') as f:
			f.write("%s\n" % path)
		return

	def create_metadata(self):
		for c in self.definition.targets.dropper.config:
			if c.before == 0:
				c.before = MAX_DROP_COMPAT_LEVEL + 1
			for i in range(MAX_DROP_COMPAT_LEVEL + 1):
				if c.after < c.before:
					if i <= c.after or i >= c.before:
						continue
				elif c.after >= c.before:
					if i <= c.after and i >= c.before:
						continue

				if c.type == 'all':
					self._write_config(i, os.path.join(self.metadata_dir, "config"))
					self._write_config(i, os.path.join(self.metadata_dir, "config-user"))
				elif c.type == "system":
					self._write_config(i, os.path.join(self.metadata_dir, "config"))
				elif c.type == "user":
					self._write_config(i, os.path.join(self.metadata_dir, "config-user"))

		self._write_config(os.path.join(self.metadata_dir, "create-message"))
		self._write_metadata(os.path.join(self.metadata_dir, "expiry"))

		excluded_user = ''
		if os.path.exists(os.path.join(self.source_dir, "dev")):
			try:
				for root, dirs, files in os.walk(os.path.join(self.source_dir, "dev")):
					try:
					# check file modes and if os.mode_device != 0
					# exclude the user
					except Exception as e:
						print(e)

		self._write_metadata(os.path.join(self.metadata_dir, "excluded-user"), excluded_user, False)
		return

	def pack_metadata(self):
		files = ['create-message', 'expiry', 'excluded-user']
		try:
			configs = glob.glob(os.path.join(self.cache_dir, "metadata"), "config*", recursive=False)
		except Exception as e:
			print(e)

		for conf in configs:
			files.append(conf)

		if os.path.exists(os.path.join(self.metadata_dir, "templates")):
			files.append("templates")

		# Pack all the config files as meta.tar.xz
		return

	def _write_metadata(filename, content, append_content):
		out = render_template(content, self.definition)
		try:
			with open(filename, 'xw') as file:
				file.write(out)
		except OSError as ose:
			print("OSError occured")
		except Exception as e:
			print("Exception occured")

	def _write_config(compat_level, filename, content):
		if compat_level != MAX_DROP_COMPAT_LEVEL:
			filename = "%s.%d" % (filename, compat_level)
		self._write_metadata(filename, content, True)
		return


