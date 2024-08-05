from container import *
from functions import *


global chosen
# checkroot()

nspawn = Container(name=cname(), base_distro=bdistro(), net_type=ntype())

print(nspawn.name, nspawn.base_distro, nspawn.net_type)

checkbtrfs()

machdir(mach_path), nspawndir(nspawn_path)

choosepmgr(), pkginstall(chosen)

match nspawn.base_distro:
    case "debian":
        ndebian()
    case "fedora":
        nfedora()
    case "arch":
        narch()

match nspawn.net_type:
    case "host":
        host_net()
    case "private":
        priv_net()

selinux_disable(), root_passwd(), selinux_enable()
