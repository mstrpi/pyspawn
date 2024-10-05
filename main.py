import resources.container as ctr
import resources.functions as fx

nspawn = ctr.Container()

cn = nspawn.cname
bd = nspawn.base_distro
nt = nspawn.net_type

print("\nConfirming container details:\nName: " + cn + "\nPreferred Distro: " +
      bd + "\nNetwork Type: " + nt)


# global MACH_PATH
MACH_PATH = "/var/lib/machines"
# global ct_path
ct_path = MACH_PATH + '/' + cn
# global NSPAWN_PATH
NSPAWN_PATH = "/etc/systemd/nspawn"
# global nspawn_file
nspawn_file = NSPAWN_PATH + "/" + cn + ".nspawn"
# global ct_net_path
ct_net_path = ct_path + "/etc/systemd/network"
# global ct_net_if
ct_net_if = ct_net_path + "/host0.network"
# global ct_net_mv
ct_net_mv = ct_net_path + "/mv0.network"

apt = ["/usr/bin/apt", "apt-get update -y ", "apt install -y "]
dnf = ["/usr/bin/dnf", "dnf upgrade -y ", "dnf install -y "]
pacman = ["/usr/bin/pacman", "pacman -Syu --no-confirm ",
          "pacman -Sy --no-confirm "]
pkg_mgrs = [apt[0], dnf[0], pacman[0]]

ct_depends = ["systemd-container ", "dbus-broker "]
deb_depends = ["debootstrap ", ct_depends]
fed_depends = ["dnf ", ct_depends]
arc_depends = ["arch-install-scripts ", ct_depends]

fx.checkbtrfs(ct_path)

fx.machdir(MACH_PATH)

fx.nspawndir(NSPAWN_PATH)

fx.find_pmgr(pkg_mgrs)

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
