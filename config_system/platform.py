
class Platform(JSONFile):
	__fields__ = {
		'arch': None,
		'os': {
			'os_ver': None,
			'os_features': [],
		},
		'variant': None,
		'features': [],
	}

	def __init__(self, platform_arch, os_ver, variant, os_features, platform_features, json_file):
		super().__init__(json_file)
		self.__fields__['arc'] = platform_arch
		self.__fields__['os']['os_ver'] = os_ver
		self.__fields__['os']['os_features'] = os_features
		self.__fields__['variant'] = variant
		self.__fields__['features'] = platform_features

	def __eq__(self, other):
		return self.__fields__ == other.__fields__

