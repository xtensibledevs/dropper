class ClusterManager:

	def __init__(self):
		if self.client:
			try:
				self.reload()
			except Exception as ex:
				print(e)

	def version(self):
		self._version

	def get_unlock_get(self):
		''' get the unlock key for the cluster '''

	def boot_cluster(self, advertise_addr=None, listen_addr='0.0.0.0:4556', force_new_cluster=False, default_addr_pool=None, subnet_size=None, data_path_addr=None, data_path_port = None, task_history_retention_lim=None, heart_beat_tick)
	'''
	snapshot_interval
	keep_old_snaps
	log_entires_for_slow_followers
	election_tick
	heartbeat_tick
	dispatcher_tick
	dispatcher_heartbeat_period
	node_cert_expiry
	external_ca
	name
	lables
	signing_ca_cert
	signing_ca_key
	ca_force_rotate
	autolock_managers
	log_driver
	'''

	def join(self):

	def leave(self):

	def reload(self):

	def unlock(self, key):

	def update(self, rotate_worker_token=False, rotate_manager_token=False, rotate_manager_unlock_key=False):

	def 