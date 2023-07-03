
class Sandbox:
	def start_sandbox():

	def stop_sandbox():

	def wait_sandbox():

	def update_sandbox():

	def pause_sandbox():

	def resume_sandbox():

	def sandbox_status():

	def ping_sandbox():

	class SandboxActions:
		def __init__(self, id, bundle_path, rootfs, opts):
			self.sandbox_id = id
			self.bundle_path = bundle_path
			self.rootfs = rootfs
			self.opts = opts

		def sandbox_start_req(id, bundle_path, rootfs, opts):
			self.sandbox_id = id
			self.bundle_path = bundle_path
			self.rootfs = rootfs
			self.opts = opts

		def start_sandbox_resp(pid):
			self.stop_pid = 1;





