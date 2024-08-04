#!/usr/bin/env python3
from main import nspawn


# global cn
cn = nspawn.name
# global mach_path
mach_path = "/var/lib/machines"
# global ct_path
ct_path = mach_path + '/' + cn
# global nspawn_path
nspawn_path = "/etc/systemd/nspawn"
# global nspawn_file
nspawn_file = nspawn_path + '/' + cn + ".nspawn"
# global ct_net_path
ct_net_path = ct_path + "/etc/systemd/network"
# global ct_net_if
ct_net_if = ct_net_path + "/host0.network"
# global ct_net_mv
ct_net_mv = ct_net_path + "/mv0.network"

choices = list()

global chosen

apt = ["/usr/bin/apt", "apt-get update -y ", "apt install -y "]
dnf = ["/usr/bin/dnf", "dnf upgrade -y ", "dnf install -y "]
pacman = ["/usr/bin/pacman", "pacman -Syu --no-confirm ", "pacman -Sy --no-confirm "]
pkg_mgrs = [apt[0], dnf[0], pacman[0]]

ct_depends = ["systemd-container ", "dbus-broker "]
deb_depends = ["debootstrap ", ct_depends]
fed_depends = ["dnf ", ct_depends]
arc_depends = ["arch-install-scripts ", ct_depends]

# print(ct_path)
