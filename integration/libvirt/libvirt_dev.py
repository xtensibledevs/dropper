
import sys
import libvirt
from xml.dom import minidom
import libxml2
from typing import Any, Dict

LIBVIRT_DIRVERS = ['qemu', 'xen', 'xenapi', 'uml', 'lxc', 'vbox', 'openvz', 'esx', 'gsx', 'vpx', 'hyperv']

def xpath_eval(ctxt, path: str) -> str:
	res = ctxt.xpathEval(path)
	if res is None or len(res) == 0:
		value = ''
	else:
		value = res[0].content
	return value

SASL_USER = "my-super-user"
SASL_PASS = "my-super-pass"
remote_hostname = "clusterhost"

def request_cred(credentials, user_data):
	for credential in credentials:
		if credential[0] == libvirt.VIR_CRED_AUTHNAME:
			credential[4] = SASL_USER
		elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
			credential[4] = SASL_PASS
	return 0

auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], request_cred, None]
QEMU_URL = 'qemu+tls://{hostname}/system'.format(hostname=remote_hostname)

try:
	conn = libvirt.openAuth(QEMU_URL, auth, 0)
except libvirt.libvirtError as err:
	print("Failed to connect to the hypervisor" + repr(e), file=sys.stderr)
	exit(1)

try:
	capsXML = conn.getCapabilities()
except libvirt.libvirtError:
	print("Failed to request capabilities")
	exit(1)

hostname = conn.getHostname()
vcpus = conn.getMaxVcpus(None)
caps = minidom.parseString(capsXML)
cells = caps.getElementsByTagName("cells")[0]
nodeInfo = conn.getInfo()

nodeIDs = [
	int(proc.getAttribute("id"))
	for proc in cells.getElementsByTagName("cell")
]

nodesMem = [
	conn.getMemoryStats(int(proc))
	for proc in nodesIDs
]

doms = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)

domsStrict = [
	proc
	for proc in doms
	if proc.numaParamaters()["numa_mode"] == libvirt.VIR_DOMAIN_NUMATUNE_MEM_STRICT
]

domsStrictCfg = {}
for dom in domsStrict:
	xmlStr = dom.XMLDesc()
	doc = libxml2.parseDoc(xmlStr)
	ctxt = doc.xpathNewContext()

	domsStrictCfg[dom] = {}

	pin = ctxt.xpathEval("string(/domain/numatune/memory/@nodeset)")
	memsize = ctxt.xpathEval("string(/domain/memory)")
	domsStrictCfg[dom]["memory"] = {"size": int(memsize), "pin": pin}

	for memnode in ctxt.xpathEval("/domain/numatune/memnode"):
		ctxt.setContextNode(memnode)
		cellid = xpath_eval(ctxt, "@cellid")
		nodeset = xpath_eval(ctxt, "@nodeset")

		nodesize = xpath_eval(ctxt, "/domain/cpu/numa/cell[@id='%s']/@memory" % cellid)
		domsStrictCfg[dom][cellid] = {"size": int(nodesize), "pin": nodeset}

print('-' * 100)
print("Library Information")
print("Package Version : " + libvirt.sys.version)
print("Library Version : " + str(libvirt.sys.version_info))
print('-' * 100)

print('Hostname : ' + str(hostname))
print('Model : ' + str(nodeInfo[0]))
print('Memory size : ' + str(nodeInfo[1]) + "MB")
print('Number of CPUs : ' + str(nodeInfo[2]))
print('MHz of CPUs : ' + str(nodeInfo[3]))
print('Number of NUMA nodes : ' + str(nodeInfo[4]))
print('Number of CPU sockets : ' + str(nodeInfo[5]))
print('Number of CPU cores per socket : ' + str(nodeInfo[6]))
print('Number of CPU threads per core : ' + str(nodeInfo[7]))
print('Maximux support virtual CPUs : ' + str(vcpus))

print("NUMA stats")
print("NUMA nodes:\t" + "\t".join(str(node) for node in nodeIDs))
print("MemTotal:\t" + "\t".join(str(i.get("total") // 1024) for i in nodesMem))
print("MemFree:\t" + "\t".join(str(i.get("free") // 1024) for i in nodesMem))

for dom, v in domsStrictCfg.items():
	print("Domain '%s' : \t" % dom.name())

	toPrint = "\tOverall memory: %d MiB" % (v["memory"]["size"] // 1024)
	if v["memory"]["pin"] is not None and v["memory"]["pin"] != "":
		toPrint = toPrint + " nodes %s" % v["memory"]["pin"]
	print(toPrint)

	for k, node in sorted(v.items()):
		if k == "memory":
			continue
		toPrint = "\tNode %s:\t%d MiB" % (k, node["size"] // 1024)
		if node["pin"] is not None and node["pin"] == "":
			toPrint = toPrint + " nodes %s" % node["pin"]
		print(toPrint)