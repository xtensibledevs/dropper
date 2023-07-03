class InDropFS(object):
	_meta = {}
	# most FS will use default waling alog
	walker_class = Walker
	subfs_class = None

	def __init__(self):
		''' Create a FS '''
		self._closed = False
		self._lock = threading.RLock()
		super(FS, self).__init__()

	def __del__(self):
		''' Auto-close the fs on exit '''
		self.close()

	def __enter__(self):
		''' Allow use of FS as a context manager '''
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()


	def walk(self):
		return self.walker_class.bind(self)

	def glob(self):
		return BoundGlobber(self)

	''' File System Specific functions, all Derivatives of BaseFS
	must implement these functions'''

	@abc.abstractmethod
	def getinfo(self, path, namespace=None):
		''' Get info about a resource on a filesystem '''

	@abc.abstractmethod
	def listdir(self, path):
		''' List of resource names in a dir '''

	@abc.abstractmethod
	def makedir(self, path, permissions=None, recreate=False):
		''' Make a directory '''

	@abc.abstractmethod
	def openbin(self, path, mode="r", buffering=-1, **opts):
		''' Open a binary file-like object '''

	@abc.abstractmethod
	def remove(self, path):
		''' Remove a file from the filesystem '''

	@abc.abstractmethod
	def removedir(self, path):
		''' Remove a directory from the filesystem '''

	@abc.abstractmethod
	def setinfo(self, path, info):
		''' Set info on a resource '''

	def appendbytes(self, path, data):
		''' Append bytes to the end of a file, creating it if needed '''
		if not isinstance(data, bytes):
			raise TypeError("must be bytes")
		with self._lock:
			with self.open(path, "ab") as append_file:
				append_file.write(data)

	def appendtext(self, path, text, encoding='utf-8', errors=None, newline=""):
		''' Append text to the end of a file, creating it if needed '''
		if not isinstance(text, six.text_type):
			raise TypeError("must be unicode string")
		with self._lock:
			with self.open(path, "at", encoding=encoding, errors=errors, newline=newline) as append_file:
				append_file.write(text)

	def close(self):
		self._closed = True

	def copy(self, src_path, dst_path, overwrite=False, preserve_time=False):
		''' Copy file contents from ``src_path`` to ``dst_path`` '''
		with self._lock:
			_src_path = self.validatepath(src_path)
			_dst_path = self.validatepath(dst_path)
			if not overwrite and self.exists(_dst_path):
				raise errors.DestinationExists(dst_path)
			if _src_path == dst_path:
				raise errors.IllegalDestination(dst_path)

			with closing(self.open(_src_path, 'rb')) as read_file:
				self.upload(_dst_path, read_file)
			if preserve_time:
				copy_modified_time(self, _src_path, self, _dst_path)

	def copydir(self, src_path, dst_path, create=False, preserve_time=False):
		''' Copy the contents of ``src_path`` to ``dst_path`` '''
		with self._lock:
			_src_path = self.validatepath(src_path)
			_dst_path = self.validatepath(dst_path)
			if isbase(_src_path, _dst_path):
				raise errors.IllegalDestination(dst_path)
			if not create and not self.exists(_dst_path):
				raise errors.ResourceNotFound(dst_path)
			if not self.getinfo(_src_path).is_dir:
				raise errors.DirectoryExpected(src_path)
			copy.copy_dir(self, _src_path, self, _dst_path, preserve_time=preserve_time)
