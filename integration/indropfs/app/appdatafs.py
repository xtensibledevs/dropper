import typing

import abc
from appdirs import AppDirs


class DropAppDataFS(InDropFS):
	''' FileSystem for storing particularly user data for applications on a drop '''

	app_home_dirdir = None

	def __init__(self, app_name, author=None, version=None, roaming=False, create=True):
		''' Create a new app-sepcific AppFS '''
		self.app_dirs = AppDirs(appname, author, version, roaming)
		self._create = create
		super().__init__(self.app_dirs, self.app_dir, create=create)

	def __repr__(self):
		return "(DropAppDataFS - @appname:{} @author:{} @version:{} @roaming:{} )" % (app_name, author, version, roaming)

	def __str__(self):
		return "<{} '{}'>".format(self.__class__.__name__.lower(), self.app_dirs.appname)

class UserDataFS(DropAppDataFS):
	''' Filesystem for per-user application data '''
	app_dir = "user_data_dir"

class UserConfigFS(DropAppDataFS):
	''' A filesystem for pre-user application cache data '''
	app_dir = "user_config_dir"

class SiteDataFS(DropAppDataFS):
	''' A filesystem for application site data '''
	app_dir = "site_data_dir"

class SiteConfigFS(DropAppDataFS):
	''' A filesystem for application config data '''
	app_dir = "site_config_dir"

class UserLogFS(DropAppDataFS):
	''' A filesystem for application user log data '''
	app_dir = "user_log_dir"

