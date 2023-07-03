'''
services
  service
  -> build
  -> blkio_config
  -> device_read_bps
    -> path
    -> rate
  -> device_write_bps
    -> path
    -> rate
  -> device_read_iops
    -> path
    -> rate
  -> device_write_iops
    -> path
    -> rate
  -> weight
  -> weight_device
    -> path
    -> weight
  -> cpu
    -> cpu_count
    -> cpu_percent
    -> cpu_shares
    -> cpu_period
    -> cpu_quota
    -> cpu_rt_runtime
    -> cpu_rt_period
    -> cpuset
  -> cap_apply
  -> cap_remove
  -> controller
  -> configs
     - -> source
       -> taget
       -> uid
       -> gid
       -> mode

  -> container_name
  -> credential_spec
    -> registery
    -> file
  -> deploy
  -> device_controller
  -> dns
  -> dns_opt
  -> dns_search
  -> domainname
  -> entrypoint
  -> env_file
  -> environment
  -> expose
  -> extends
  -> external_links
  -> extra_hosts
  -> group_add
  -> health_check
  -> hostname
  -> image
  -> init
  -> ipc
  -> isolation
  -> labels
  -> links
  -> logging
    -> driver
    -> opts
  -> network_mode
  -> networks
  -> aliases
  -> ipaddr
    -> ipv4addr
    -> ipv6addr
  -> link_local_ips
  -> priority
  -> mac_address
  -> mem_limit
  -> mem_reservation
  -> mem_swappiness
  -> memswap_limit
  -> pid
  -> pids_limit
  -> platform
  -> ports
    -> target
    -> hostip
    -> published
    -> protocol
    -> mode
  -> priviliged
  -> profiles
  -> pull_policy
  -> read_only
  -> restart
  -> runtime
  -> scale
  -> secrets
  -> sec_opts
  -> shm_size
  -> stdin_open
  -> stop_grace_period
  -> stop_signal
  -> storage_opt
  -> sysctls
  -> tmpfs
  -> tty
  -> ulimits
  -> user
  -> userns_mode
  -> volumes
  -> driver
  -> host
  -> name
  -> labels
  -> external
-> volumes
->configs
-> secrets
-> extensions
-> 

volumes
secrets
networks
configs

'''

import yaml

from rich.console import Console
from rich.json import JSON
import json

from yaml.loader import SafeLoader

console = Console()

with open('example.yaml') as dropperconfig:
  data = yaml.load(dropperconfig, Loader=SafeLoader)
  console.print_json(json.dumps(data))

