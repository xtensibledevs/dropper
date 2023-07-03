
from .json_config import JSONConfig

class ConfigFile(JSONConfig):
	__fields__ = {
		'architecture': None,
		'author': None,
		'drop': None,
		'created': None,
		'drop_version': None,
		'history': None,
		'os': None,
		'root_fs': None,
		'config': None,
		'variant': None,
	}

class History(JSONConfig):
	__fields__ = {
		'author': None,
		'created': None,
		'created_by': None,
		'comment': None,
		'empty_layer': False,
	}

class HealthConfig(JSONConfig):
	__fields__ = {
		'test': None,
		'interval': None,
		'timeout': None,
		'start_period': None,
		'retries': None,
	}

class Config(JSONConfig):
	__fields__ = {
		'attach_stderr' : None,
		'attach_stdin' : None,
		'attach_stdout' : None,
		'cmd' : None,
		'health_check': None,
		'domain_name': None,
		'entry_point': None,
		'env': None,
		'hostname': None,
		'image': None,
		'labels': [],
		'onbuild': None,
		'openstdin': True,
		'stdinonce': False,
		'tty': True,
		'user': None,
		'volumes': {},
		'working_dir': None,
		'exposed_port_map': {},
		'args_escaped': False,
		'network_disabled': False,
		'mac_addr': None,
		'stop_signal': signal.SIGINT,
		'shells': [],
	}

class Manifest(JSONConfig):
	__fields__ = {
		'schema_ver': None,
		'module': None,
		'config': None,
		'layers': [],
		'annotations': {},
	}

class IndexManifest(JSONConfig):
	__fields__ = {
		'schema_ver': None,
		'module': None,
		'manifests': None,
		'annotations': None,
	}

class Descriptior(JSONConfig):
	__fields__ = {
		'module': None,
		'size': None,
		'digest': None,
		'data': None,
		'urls': []
		'annotations': {},
		'platform': None,
	}