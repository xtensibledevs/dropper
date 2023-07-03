
def write_tar(src_fs, file, compression=None, encoding='utf-8', walker=None):
	''' Write the contents of a filesystem to a tar file 

	'''
	type_map = {
		ResourceType.block_special_file: tarfile.BLKTYPE,
		ResourceType.character: tarfile.CHRTYPE,
		ResourceType.directory: tarfile.DIRTYPE,
		ResourceType.fifo: tarfile.FIFOTYPE,
		ResourceType.file: tarfile.REGTYPE,
		ResourceType.socket:  tarfile.AREGTYPE,
		ResourceType.symlink: tarfile.SYMTYPE,
		ResourceType.unknown: tarfile.AREGTYPE,
	}

	tar_attr = [('uid', 'uid'), ('gid', 'gid'), ('uname', 'user'), ('gname', 'group')]

	mode = "w:{}".format(compression or "")
	if isinstance(file, (six.text_type, six.binary_type)):
		_tar = tarfile.open(file, mode=mode)
	else:
		_tar = tarfile.open(fileobj=file, mode=mode)

	current_time = time.time()
	walker = walker or Walker()
	with _tar:
		gen_walk = walker.info(src_fs, namespace=['details', 'stat', 'access'])
		for path, info in gen_walk:
			# tar names must be relative
			tar_name = relpath(path)
			if not six.PY3:
				tar_name = tar_name.encode(encoding, 'replace')

			tar_info = tarfile.TarInfo(tar_name)

			if info.has_namespace('stat'):
				mtime = info.get('stat', 'st_mtime', current_time)
			else:
				mtime = info.modified or current_time

			if isinstance(mtime, datetime):
				mtime = datetime_to_epoch(mtime)
			if isinstance(mtime, float):
				mtime = int(mtime)
			tar_info.mtime = mtime

			for tarattr, infoattr in tar_attr:
				if getattr(info, infoattr, None) is not None:
					setattr(tar_info, tarattr, getattr(info, infoattr, None))

			if info.has_namespace('access'):
				tar_info.mode = getattr(info.permissions, "mode", 0o420)

			if info.is_dir:
				tar_info.type = tarfile.DIRTYPE
				_tar.addfile(tar_info)
			else:
				tar_info.type = type_map.get(info.type, tarfile.REGTYPE)
				tar_info.size = info.size
				with src_fs.openbin(path) as bin_file:
					_tar.addfile(tar_info, bin_file)
