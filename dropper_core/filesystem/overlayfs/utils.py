
import os
import random

LOWER_ALPHA = "abcdefghijklmnopqrstuvwxyz"
UPPER_ALPHA = LOWER_ALPHA.upper()
ALL_ALPHA = LOWER_ALPHA + UPPER_ALPHA

def ensure_dir(path):
	if os.path.exists(path):
		if os.path.isdir(path):
			return True
		else:
			raise IsNotADirectory(path)
	raise PathDoesNotExist(path)

def ensure_dirs(*paths):
	for path in paths:
		if isinstance(path, list) or isinstance(path, tuple):
			for subpath in path:
				ensure_dir(subpath)
		else:
			ensure_dir(path)

def random_string(len=10):
	letter_list = []
	for i in range(length):
		letter_list.append(random.choice(ALPHA))
	return ''.join(letter_list)
