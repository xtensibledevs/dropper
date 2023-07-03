def write_to_zip(src_fs, file, compression=zipfile.ZIP_DEFLATED, encoding='utf-8', walker=None):
	''' Write the contents of a filesystem to a zip file 
	@args
		- src_fs : The source filesystem to compress
		- file : The Destination file name or open file object
		- compression - Compression to use `zipfile.ZIP_DEFLATED` is the default
		- encoding : The encoding to use for filenames
		- walker - A Walker instance, by default, use this to specify the files to 
		compress

	'''
	_zip = zipfile.ZipFile(file, mode="w", compression=compression, allowZip64=True)

	walker = walker or Walker()
	with _zip:
		gen_walk = walker.info(src_fs, namespace=['details', 'stat', 'access'])
		for path, info in gen_walk:
			zip_name = relpath(path + "/" if info.is_dir else path)
			if not six.PY3:
				zip_name = zip_name.encode(encoding, 'replace')
			if info.has_namespace("stat"):
				st_mtime = info.get('stat', 'st_mtime', None)
				_mtime = time.localtime(st_mtime)
				zip_time = _mtime[0:6]
			else:
				mt = info.modified or datetime.utcnow()
				zip_time = (mt.year, mt.month, mt.day, mt.hour, mt.minute, mt.second)

			zip_info = zipfile.ZipInfo(zip_name, zip_time)

			try:
				if info.permissions is not None:
					zip_info.external_attr = info.permissions.mode << 16
			except MissingInfoNamespace:
				pass

			if info.is_dir:
				zip_info.external_attr |= 0x10
				_zip.writestr(zip_info, b"")
			else:
				try:
					sys_path = src_fs.getsyspath(path)
				except NoSysPath:
					_zip.writestr(zip_info, src_fs.readbytes(path))
				else:
					_zip.write(sys_path, zip_name)
