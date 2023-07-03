
import os

from ..util.drop_utils import random_digset

DROPS_DIR = "/var/run/dropper/drops"
DROPPER_NET_NS_PATH = "/var/run/dropper/netns"
DROP_CONFIG_FILE = "config.json"
DIGEST_STD_LEN = 64
MB = 1 << 20

class Drop:
	drp_id = None
	drp_name = None
	drp_default_cmd = None

	drp_config = None
	root_fs = None

	drp_pids = []
	drp_mem = None
	drp_swap = None
	drp_pid = None
	cpus = None

	project = None
	service = None
	drp_status = None
	drp_health = None
	publishers = None

	drp_image = None
	loop_device = None
	root_fs = None
	root_fs_dir = None
	size = None

	def __init__(self, drop_image, drp_config, loop_device, root_fs, root_fs_module="EXT4"):
		if root_fs not in SUPPORTED_FS:
			raise Exception("Unsupported FS : %s" % root_fs)
		if size == 0:
			size = 4294967296
			
		self.drp_config = config
		self.drp_digest = random_digset()

		self.root_fs = root_fs
		self.drp_image = drop_image
		self.loop_device = loop_device
		self.size = size

	def sethostname(self):
		if self.drp_config.hostname == "":
			self.drp_config.hostname = self.drp_digest[:12]
		# sethostname(self.drp_config.hostname)

	def get_loop_device(self):
		return self.loop_device

	def get_rootfs_dev(self):
		return "%sp2" % self.loop_device

	def get_uefi_dev(self):
		return "%sp1" % self.loop_device

	def create_empty_disk_image(self, image_name):
		pass

	@property
	def name(self):
		if self.drp_name is not None:
			return self.drp_name.lstrip("/")

	@property
	def image(self):
		if self.drp_image.image_id is not None:
			return self.drp_image.image_id
		fs_signature = hash(self.image.dir_struct)
		matching_image = self.drop_store.image_api.query_image_with_fs_signature(fs_signature)
		if matching_image is not None:
			return matching_image
		return None

	@property
	def labels(self):
		return self.drp_config.labels

	@property
	def status(self):
		return self.drp_status

	@property
	def port_map(self):
		return self.drp_network.port_map

	def package(self, repository=None, tag=None, **kwargs):
		pass

	def diff(self):
		''' Inspect the drop's overlay fs '''

	def exec_cmd(self, cmd, stdout=True, stderr=True, stdin=False, tty=False, previliged=False, user='', detach=False, stream=False, socket=False, env=None, work_dir=None, demux=False):
		''' Run a command inside a drop '''
		cwd = os.getcwd()
		rr = op.open("/", os.O_RDONLY)
		os.chroot(os.path.join(self.drops_dir, drop_name))
		os.chdir("/")
		os.system(cmd, *args)
		os.fchdir(rr)
		os.chroot(".")
		os.chdir(cwd)

	def export(self, chunk_size=DEFAULT_DATA_CHUNK_SIZE):
		''' export the contents of a drop's fs as a tar archive '''
		pass

	def get_archive(self, path, chunk_size=DEFAULT_DATA_CHUNK_SIZE, encode_stream=False):
		''' Retrive a file or folder from the container in the form of a tar archive '''
		pass

	def kill(self, signal=None):
		''' Kill or send signal to the Drop '''
		pass

	def peek_logs(self, **kwargs):
		pass

	def pause(self):
		''' Pause the drop processes '''
		pass

	def put_archive(self, path, data):
		''' Insert a file or folder in this drop using a tar archive as a source file '''
		pass

	def delete(self, force=False):
		try:
			shutil.rmtree(os.path.join(DROPS_DIR, self.drp_digest))
		except Exception as ex:
			raise Exception("can't remove drop root")
		try:
			shutil.rmtree(os.path.join(DROPPER_NET_NS_PATH, self.drp_digest))
		except Exception as ex:
			raise ex
		try:
			remove_cgroups()

	def rename(self, name):
		''' Rename the drop '''
		pass

	def mount_from_image(drop_img: DropImage):
		drop_target = os.path.join(DROPS_DIR, self.drp_digest, "mnt")
		try:
			os.mkdir(drop_target, 0700)
		except Exception as ex:
			raise Exception("Can't create %s directory" % (drop_target))
		self.root_fs = drop_target
		layers_dir, img_layers_digset = drop_img.UnpackLayers(drop_target)
		overlay = overlayfs.mount(upper=layers_dir[0], lower=layers_dir[1], work_dir=layers_dir[2])
		return overlay


	def resize(self, height, width):
		''' Resize the tty session '''
		pass

	def restart(self, force=False):

		pass

	def start(self, **kwargs):
		pass

	def stop(self, **kwargs):
		pass

	def top(self, **kwargs):
		''' Display all running processes inside the drop '''
		pass

	def unpause(self):
		pass

	def update(self, blkio_weight, cpu_period, cpu_quota, cpu_shares, cpuset_cpus, cpuset_mems, mem_lim, mem_reserv, memswap_lim, kernel_mem, restart_policy):
		pass

	def wait(self, timeout, condition):
		''' Block until the drop stops '''
		pass
