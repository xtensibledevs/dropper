
import repositioryapi

TAG_CHAR_SPACE = "abcdefghijklmnopqrstuvwxyz0123456789_-.ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TAG_DELIM = ":"

class DropTag:
	tag = None
	original = None

	def __init__(self, name, strict=False):
		name_parts = name.split(TAG_DELIM)
		if len(name_parts) > 1 and name_parts[len(name_parts) - 1].contains('/'):
			base_name = name_parts[:len(name_parts) - 1] + TAG_DELIM
			tag = name_parts[len(name_parts) - 1]

		if tag != "" or strict == True:
			self.check_tag(tag)

		if tag == "":
			tag = DEFAULT_TAG

		try:
			self.repo = repositioryapi.NewRepository(base_name)
		except Exception as ex:
			print(ex)

		self.tag = tag
		self.original = name
		self.name = self.repo.name() + TAG_DELIM + tag