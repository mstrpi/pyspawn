from .assets.nspawn.container import nspawn
from .assets.roothost.functions import *
from .assets.pmanager import pkginstall as pkm
from nspawn.ctrfunctions import *


def main():
    cn = nspawn.cname
    bd = nspawn.base_distro
    nt = nspawn.net_type

    print("\nConfirming container details:\nName: " + str(cn) + "\nPreferred Distro: " +
          str(bd) + "\nNetwork Type: " + str(nt))

    # global mach_path
    mach_path = "/var/lib/machines"
    # global ct_path
    ct_path = mach_path + '/' + str(cn)
    # global nspawn_path
    nspawn_path = "/etc/systemd/nspawn"
    # global nspawn_file
    nspawn_file = nspawn_path + "/" + str(cn) + ".nspawn"
    # global ct_net_path
    ct_net_path = ct_path + "/etc/systemd/network"
    # global ct_net_if
    ct_net_if = ct_net_path + "/host0.network"
    # global ct_net_mv
    ct_net_mv = ct_net_path + "/mv0.network"

    checkbtrfs(ct_path)

    firstcmd(mach_path, nspawn_path)

    pkm.main(pakbins, choices, chosen, apt_cmds, dnf_cmds, pac_cmds)

    match bd:
        case "debian":
            ndebian(ct_path)
        case "fedora":
            nfedora(ct_path)
        case "arch":
            narch(ct_path)

    match nt:
        case "host":
            host_net(nspawn_file)
        case "private":
            priv_net(nspawn_file, ct_net_mv, ct_net_if)

    selinux_disable()
    root_passwd(cn)
    selinux_enable()

    match nt:
        case "host":
            systemd_nr_disable(ct_path)
        case "private":
            systemd_nr_enable(ct_path)

    ct_hostname(ct_path)

    outro(cn)


if __name__ == "__main__":
    main()