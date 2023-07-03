'''
Dropstore REST API Endpoints

Get a list of drops, can apply filters - GET /drops

Get a drop with drop id - GET /drops/<drop_id>

Create a new drop - POST /drops/create/

Update the drop - PATCH /drops/update

Delete the drop - DELETE /drops/delete

'''

class DropStore:
	''' Interface for the online drop store '''

	API_URL = "https://dropstore.xcloud.io/"
	API_KEY = "API SECRET!"
	APP_SCOPE = {
		"appscope1": "appscopekey1",
		"appscope1": "appscopekey2",
	}

	def __init__(self):
		super().__init__()

	def get(self, drop_id):
		pass

	def list(self, filters):
		pass

	def create(self, container):
		pass

	def update(self, container, fieldpaths):
		pass

	def delete(self, drop_id):
		pass

	def setup_tool(drop_root):
		drop_store_home = os.path.join(drop_root, ".dropper", "drop-store")
		if not os.path.exists(drop_store_home):
			os.mkdir(drop_store_home)
		drops_dir = os.path.join(drop_root, "drops")
		if not os.path.exists(drops_dir):
			os.mkdir(drops_dir)


		with cloudlogger.progress('Downloading files', 100) as prog:
			# Download and set up image managers
			setuputil = urllib.urlopen("https://github.com/GFMS-XCloud/dropper-store/blob/master/setup-tool/debootstrap.tar.gz?raw=true").read()
			prog.success("Download Complete")

		path = drop_store_home + "setuputil.tar"
		with open(path, 'wb') as tarf:
			tarf.write(setuputil)
		tarfile.open(path).extractall(drop_store_home)
		os.remove(path)
		edit = open(drop_store_home, "setuputil/debootrstrap").read()
		edit = "DEBOOTSTRAP_DIR={}\n".format(drop_store_home + "setuputil") + edit
		with open(os.path.join(drop_store_home, "setuputil/debootrstrap"), 'w') as f:
			f.write(edit)


	def copy_image_base_fs(image: DropImage):
		''' Copy base FS of the drop image '''
		cloudlogger.info("Copying files : {}".format(path))
	
		# image details
		bfs_module_ver = DropImage.BaseFS._version
		bfs_module = DropImage.BaseFS._module
		bfs_features = DropImage.BaseFS._features

		cloudlogger.info("BaseFS using Module : {}, Version : {}".format(bfs_module, bfs_module_ver))

		# download the environment from the ImageRepo
		deb_cmd = "bash " + self.dorpper_root + "debootstrap/debootrstrap --arch=" + arch + " {} {}"
		try:
			DropImage.get_base_fs():
		except Exception as ex:
			cloudlogger.error(ex)

		get_source_list(path, version)


