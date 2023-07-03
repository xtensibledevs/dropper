class ClusterNode:

	def version(self):
		return self._version

	def udpate(self, node_spec):
		''' Update the node's config '''

	def remove(self, force=False):
		''' Remove the node from the Cluster '''


class NodeManager:
	def get(self, node_id):
		''' Get a node object '''

	def list_nodes(self, filters=None):
		''' List all nodes under the cluster '''
