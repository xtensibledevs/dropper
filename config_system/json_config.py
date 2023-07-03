import json

class JSONConfig:
	def __init__(self, json_file):
		if json_file is None:
			raise Exception('No JSON file specified')
		with open(json_file) as f:
			json_data = json.load(f)
		for field in self.__fields__:
			self.__fields__[field] = json_data[field]

	def dump_to_json(self, filepath):
		with open(filepath, 'w') as out:
			json.dump(self.__fields__, out)