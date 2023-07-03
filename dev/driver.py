
# Default driver - the driver used for the driver
# implemented in local package


# Scopes define the scopes of the volume
# Scopes -> Local Scope, and Cluster Scope

# Driver is for creating and removing volumes
class Driver:
	# name of the volume driver
	def name():
		pass

	# create a new volume with the name
	def create(name, opts):

	# remove or delete a volume
	def remove(volume):

	# list all the volumes the driver has
	def list():

	# get the volume with the requested name
	def get(name):

	# scope of the driver
	def scope()

class Cap:
	# Scope is the scope of the driver 'cluster', 'local'
	# with 'cluster' scope we can manage the volume across the cluster
	# with 'local' scope we can manage the volume from local host
	def scope():

class Volume:
	# name of the volume
	def name():
	# name of the driver that controls the volume
	def driver_name():
	# path returns the absolute path to the volume
	def path():
	# mounts the volume and returns the abs path to where it can be consumed
	def mount(id):
	# unmount the volume when it is no longer in use
	def unmount(id):
	# returns the time the volume was created
	def created_at():
	# status - low-level status information about a volume
	def status():

# Wraps a volume with user-defined labels, options and cluster
class DetailedVolume:
	volume

	def labels()

	def options()

	def scope()


class VolumeAdapter:
	name = None
	scope_path = None
	caps = None
	proxy = None
	driver_name = None
	e_mount = None
	created_at = None
	status = None

	def name(self):
		return self.name

	def create(name, opts):

	def remove(volume)

	def list()

	def get(name):

	def scope():

	def get_caps():

	def path():

	def cached_path():

	def mount():

	def unmount():

	def created_at():

	def status():

class ProxyVolume:
	name = None
	mont_point = None
	created_at = None
	status = None



