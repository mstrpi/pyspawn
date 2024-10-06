import resources.container as ctr
import resources.functions as fx
import os

fx.checkroot()

nspawn = ctr.Container()

cn = nspawn.cname
bd = nspawn.base_distro
nt = nspawn.net_type

print("\nConfirming container details:\nName: " + cn + "\nPreferred Distro: " +
      bd + "\nNetwork Type: " + nt)


# global mach_path
mach_path = "/var/lib/machines"
# global ct_path
ct_path = mach_path + '/' + cn
# global nspawn_path
nspawn_path = "/etc/systemd/nspawn"
# global nspawn_file
nspawn_file = nspawn_path + "/" + cn + ".nspawn"
# global ct_net_path
ct_net_path = ct_path + "/etc/systemd/network"
# global ct_net_if
ct_net_if = ct_net_path + "/host0.network"
# global ct_net_mv
ct_net_mv = ct_net_path + "/mv0.network"

choices = []
chosen = None
pkgmgrvar = None

apt = ["/usr/bin/apt", "apt-get update -y ", "apt install -y "]
dnf = ["/usr/bin/dnf", "dnf upgrade -y ", "dnf install -y "]
pacman = ["/usr/bin/pacman", "pacman -Syu --no-confirm ", "pacman -Sy --no-confirm "]
pkg_mgr = ["apt", "dnf", "pacman"]

ct_depends = ["systemd-container ", "dbus-broker "]
deb_depends = str(ct_depends + "debootstrap ")
fed_depends = str(ct_depends + "dnf ")
arc_depends = str(ct_depends + "arch-install-scripts ")
x_depends = [deb_depends, fed_depends, arc_depends]

pkg_mgr_bin = [apt[0], dnf[0], pacman[0]]
apt_up = str(apt[1])
dnf_up = str(dnf[1])
pacman_up = str(pacman[1])

apt_install = str(apt[2] + x_depends[0])
dnf_install = str(dnf[2] + x_depends[1])
pacman_install = str(pacman[2] + x_depends[2])

apt_cmds = str(apt_up + " && " + apt_install)
fed_cmds = str(dnf_up + " && " + dnf_install)
arc_cmds = str(pacman_up + " && " + pacman_install)

fx.checkbtrfs(ct_path)

fx.machdir(mach_path)

fx.nspawndir(nspawn_path)

fx.find_pmgr(pkg_mgr_bin, choices, chosen)

fx.deps_pmgr(chosen, pkgmgrvar, apt_cmds, fed_cmds, arc_cmds)

match bd:
    case "debian":
        fx.ndebian()
    case "fedora":
        fx.nfedora()
    case "arch":
        fx.narch()

match nt:
    case "host":
        fx.host_net()
    case "private":
        fx.priv_net()

fx.selinux_disable()

fx.root_passwd()

fx.selinux_enable()

