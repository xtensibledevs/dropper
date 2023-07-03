
import os
import errno



class CPUController(BaseController):
	''' CPU controller '''

	cfs_period_us = IntegerFile("cpu.cfs_period_us")
	cfs_quota_us = IntegerFile("cpu.cfs_quota_us")
	rt_peroid_us = IntegerFile("cpu.rt_period_us")
	rt_runtime_us = IntegerFinle("cpu.rt_runtime_us")
	shares = IntegerFile("cpu.shares")
	stat = DictFile("cpu.stat", readonly=True)

class CpuAcctController(BaseController):
	acct_stat = DictFile("cpuacct.stat", readonly=True)
	usage = IntegerFile("cpuacct.usage")
	usage_percpu = IntegerListFile("cpuacct.usage_percpu", readonly=True)

class CpuSetController(BaseController):
	cpus = CommaDashSetFile("cpuset.cpus")
    mems = CommaDashSetFile("cpuset.mems")

    cpu_exclusive = FlagFile("cpuset.cpu_exclusive")
    mem_exclusive = FlagFile("cpuset.mem_exclusive")
    mem_hardwall = FlagFile("cpuset.mem_hardwall")
    memory_migrate = FlagFile("cpuset.memory_migrate")
    memory_pressure = FlagFile("cpuset.memory_pressure")
    memory_pressure_enabled = FlagFile("cpuset.memory_pressure_enabled")
    memory_spread_page = FlagFile("cpuset.memory_spread_page")
    memory_spread_slab = FlagFile("cpuset.memory_spread_slab")
    sched_load_balance = FlagFile("cpuset.sched_load_balance")

    sched_relax_domain_level = IntegerFile("cpuset.sched_relax_domain_level")

class MemoryController(BaseController):
    ''' Memory Controller '''

	failcnt = IntegerFile("memory.failcnt")
    memsw_failcnt = IntegerFile("memory.memsw.failcnt")

    limit_in_bytes = IntegerFile("memory.limit_in_bytes")
    soft_limit_in_bytes = IntegerFile("memory.soft_limit_in_bytes")
    usage_in_bytes = IntegerFile("memory.usage_in_bytes")
    max_usage_in_bytes = IntegerFile("memory.max_usage_in_bytes")

    memsw_limit_in_bytes = IntegerFile("memory.memsw.limit_in_bytes")
    memsw_usage_in_bytes = IntegerFile("memory.memsw.usage_in_bytes")
    memsw_max_usage_in_bytes = IntegerFile("memory.memsw.max_usage_in_bytes")
    swappiness = IntegerFile("memory.swappiness")

    stat = DictFile("memory.stat", readonly=True)

    use_hierarchy = FlagFile("memory.use_hierarchy")
    force_empty = FlagFile("memory.force_empty")
    oom_control = DictOrFlagFile("memory.oom_control")

    move_charge_at_immigrate = BitFieldFile("memory.move_charge_at_immigrate")


class DevicesController(Controller):
	allow = TypedFile("devices.allow", DeviceAccess, writeonly=True)
	deny = TypedFile("devices.deny", DeviceAccess, writeonly=True)
	list = TypedFile("devices.list", DeviceAccess, readonly=True, may=True)

class BlkIOController(Controller):
	io_merged = SplitValueFile("blkio.io_merged", 1, int)
    io_merged_recursive = SplitValueFile("blkio.io_merged_recursive", 1, int)
    io_queued = SplitValueFile("blkio.io_queued", 1, int)
    io_queued_recursive = SplitValueFile("blkio.io_queued_recursive", 1, int)
    io_service_bytes = SplitValueFile("blkio.io_service_bytes", 1, int)
    io_service_bytes_recursive = SplitValueFile("blkio.io_service_bytes_recursive", 1, int)
    io_serviced = SplitValueFile("blkio.io_serviced", 1, int)
    io_serviced_recursive = SplitValueFile("blkio.io_serviced_recursive", 1, int)
    io_service_time = SplitValueFile("blkio.io_service_time", 1, int)
    io_service_time_recursive = SplitValueFile("blkio.io_service_time_recursive", 1, int)
    io_wait_time = SplitValueFile("blkio.io_wait_time", 1, int)
    io_wait_time_recursive = SplitValueFile("blkio.io_wait_time_recursive", 1, int)
    leaf_weight = IntegerFile("blkio.leaf_weight")
    # TODO: Uncomment the following properties after researching how to interact with files
    # leaf_weight_device =
    reset_stats = IntegerFile("blkio.reset_stats")
    # sectors =
    # sectors_recursive =
    # throttle_io_service_bytes =
    # throttle_io_serviced =
    throttle_read_bps_device = TypedFile("blkio.throttle.read_bps_device", contenttype=DeviceThrottle, many=True)
    throttle_read_iops_device = TypedFile("blkio.throttle.read_iops_device", contenttype=DeviceThrottle, many=True)
    throttle_write_bps_device = TypedFile("blkio.throttle.write_bps_device ", contenttype=DeviceThrottle, many=True)
    throttle_write_iops_device = TypedFile("blkio.throttle.write_iops_device ", contenttype=DeviceThrottle, many=True)
    # time =
    # time_recursive =
    weight = IntegerFile("blkio.weight")


class NetClsController(BaseController):
	clsss_id = IntegerFile("net_cls.classid")


class NetPrioController(BaseController):
	prioidx = IntegerFile("net_prio.prioidx", readonly=True)
	ifpriomap = DictFile("net_prio.ifpriomap")

