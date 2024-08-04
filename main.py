from container import *
from functions import *

# checkroot()

nspawn = Container(name=cname(), base_distro=bdistro(), net_type=ntype())

print(nspawn.name, nspawn.base_distro, nspawn.net_type)

machdir(mach_path), nspawndir(nspawn_path)

choosepmgr(), pkginstall(chosen)

checkbtrfs()
