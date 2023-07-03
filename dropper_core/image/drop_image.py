from dropstore import DropStore

drop_store = DropStore()

class DropImage(object):
	img_id = None
	img_store = None
	img_history = {}
	img_repo = None
	img_name = None
	img_tag = 'latest'

	def __init__(self, src: str):
		nw_tag = create_new_tag()
		try:
			img = dropstore.download(nw_tag.img_identifier)
		except Exception as ex:
			raise Exception('Error downloading image')
		self.img_id = img.img_digest.sha256
		self.img_store = nw_tag.img_store()
		self.img_repo = nw_tag.img_repo()
		self.img_name = nw_tag.img_name()
		self.img_tag = nw_tag


	def __repr__(self):
		return "<{}: '{}'>".format(self.__class__.__name__, self.img_id)

	def labels(self):
		return self.labels or {}

	def short_id(self):
		if self.img_id.startswith('sha256:'):
			return self.img_id[:19]
		return self.id[:12]

	@property
	def tag(self):
		return self.img_tag

	def exists_locally(self):
		images = get_all_local_imgs()
		for img in range(images):
			if img.img_id == self.imd_id:
				return True
		return False

	def get_all_local_imgs(self):
		local_repos = []
		images = []
		with open(repositories.LOCAL_REPO_FILE)

	def history(self):
		return self.img_history

	def remove(self, force=False, noprune=False):
		''' Remove the image '''
		pass

	def save(self, chunk_size=DEFAULT_DATA_CHUNK_SIZE, named=False):
		''' Get a tarball archive of the image '''
		pass
	
	def tag(self, category, tag=None, force=False):
		''' Applies a tag to this image '''
		pass

	def layers(self):
		''' Returns an orderd collection of filesystem layers that 
		constitute the image 
		The order is oldest/base layer -> diff1 -> diff2 -> latest/top
		'''
		pass

	def size(self):
		''' Return the size of the manifest '''
		pass

	def media_type(self):
		pass

	def config_file(self):
		pass

	def image_digest(self):
		''' Return the digests of the image SHA256, MD5, etc 
		Standard is SHA256
		'''
		pass

	def view_manifest(self):
		''' Return the manifest in Dict format '''
		pass

	def get_layer_by_diff_id(self, diff_id: str):
		''' Get the layer by diff id '''
		pass

