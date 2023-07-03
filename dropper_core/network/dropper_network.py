

class DropNetworkIFace:
	''' A Dropper network model '''
	@property
	def name(self):
		return self._name

	@property
	def containers(self):
		return self.drops

	def connect(self, drop, aliases, links, ipv4_address, ipv6_address, link_local_ips = [], driver_opt={}):
		''' Connect a drop to the network '''
		if isinstance(drop, Drop):
			drop_id = drop.drp_id
		# TODO

	def disconnect(self, drop, force_disconnect=False):
		''' Disconnect a drop from the network '''
		if isinstance(drop, Drop):
			drop_id = drop.drp_id

	def remove(self):
		''' Remove the network '''

	def unregister(self):
		''' Unregister the network '''


class DropperNetworkManager(Collection):
	def create(self, name, driver, opts, ipan, check_duplicate=False, internal=True, labels={}, enable_ipv6=False, attachable=True, scope='local', ingress=False):

	
	def get(self, network_id, scope):


	def list(self, names, ids, filters):

	def prune(self, filters=None):

	def setup_bridge(self, bridge_name):
		''' Create a bridge network if not exist '''
		pass

	def setup_veth(self, name, peer):
		''' Setup virtual ethernet '''
		pass

	def link_set_master(self, link_id, master_id):
		''' Set master id network iface as master '''
		pass

	def link_add_gateway(self, link_id, gateway_ip):
		''' add link gateway '''
		pass

	def link_setup(self, link_id):
		pass

	def link_rename(self, old, new):
		pass

	def ip_exists(self, ip):
		pass


