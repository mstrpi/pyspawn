import os
import sys
from globals import *


def checkroot():
    """Here it should verify admin privileges"""
    if os.getuid() == 0:
        pass
    else:
        sys.exit("Super user access required, please try again with root access.\n")


def checkbtrfs():
    print('''If btrfs is in place, should a new subvolume be created?
    (This defaults to ''' + ct_path + ").")
    print("\n[ If you don't know what btrfs is, please enter 'n' ]\n")
    i = input(" ::> ")
    if i.lower == "y":
        os.system('btrfs subvolume create ' + ct_path)


def machdir(path):
    """This will create the machine directory if it does not exist
    "/var/lib/machines\""""
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except ValueError:
            print('Please manually create machine folder with:')
            print('mkdir -p ' + path)


def nspawndir(path):
    """This will create the nspawn directory if it does not exist
    /etc/systemd/nspawn"""
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except ValueError:
            print('Please manually create nspawn folder with:')
            print('mkdir -p ' + path)


def choosepmgr():
    """This potentially determines the primary package manager
    if its binary exists"""
    choices = list()
    for b in pkg_mgrs:
        if os.path.exists(b):
            choices.append(b)
        if len(choices) < 2:
            chosen = choices[0]
            pkginstall(chosen)
        else:
            select_mgr(choices)


def select_mgr(choices):
    """If more than one package manager is found in the previous function,
    this will prmpt the user to select the preferred one"""
    print('More than one package manager found.\n')
    print('Please choose the default one to use:\n')
    for li in choices:
        print(li)
    while True:
        i = input(' ::> ')
        match i:
            case 'f"(a.t)"':
                chosen = apt[0]
                return pkginstall(chosen)
            case "dnf":
                chosen = dnf[0]
                return pkginstall(chosen)
            case "pacman":
                chosen = pacman[0]
                return pkginstall(chosen)
            case _:
                print('Please type out the name of your choice:\n')
                continue


def pkginstall(chosen):
    """This installs the dependencies for systemd-nspawn
    using the found package manager"""
    match chosen:
        case "apt":
            os.system(apt[1]), os.system(apt[2] + deb_depends)
        case "dnf":
            os.system(dnf[1]), os.system(dnf[2] + fed_depends)
        case "pacman":
            os.system(pacman[1]), os.system(pacman[2] + arc_depends)


def ndebian():
    """Give the option to try unstable branch in container
    Selects stable otherwise and installs root fs"""
    print('Would you like to test the unstable branch? [y/n]\n')
    stbl = input(" ::> ")
    match stbl.lower():
        case "y":
            branch = 'unstable '
        case _:
            branch = 'stable '
    os.system("debootstrap --include=dbus-broker,systemd-resolved " + branch + " " + ct_path)


def nfedora():
    """Here we set up the container with fedora 40 as the base. Potentially it
    would check which version is current and auto select that one"""
    releasever = 40
    os.system("\"$(cat fedora-repo-data.xml)\" >> /etc/dnf/dnf.conf")
    os.system("dnf --releasever=" + str(releasever) + ''' --best \
    --setopt=install_weak_deps=False --installroot=''' + ct_path + '''/ install \
    -y dhcp-client dnf fedora-release glibc glibc-langpack-en glibc-langpack-de \
    iputils less ncurses passwd systemd util-linux''')


def narch():
    """Set up process for a minimal arch container"""
    os.system("pacstrap -K -c " + ct_path + "/ base dbus-broker")


def selinux_disable():
    """This checks if selinux binary is present to disable it during password set for root"""
    os.system('''if [ -f /usr/sbin/setenforce ]; then \
    setenforce 0 \
    fi''')


def selinux_enable():
    """Checks if setenforce binary is present to re-enable it after root password has been set"""
    os.system('''if [ -f /usr/sbin/setenforce ]; then \
    setenforce 1 \
    fi''')


def root_passwd():
    """function to actually set root password"""
    os.system("systemd-nspawn -M " + str(cn) + " passwd")


def spwn_boot_shell():
    """one of 2 boot options for the container. This does not load dbus"""
    os.system("systemd-nspawn -M " + str(cn))


def spwn_boot_dbus():
    """second of 2 boot options. This one loads dbus"""
    os.system("systemd-nspawn -M " + str(cn) + " -b")


def host_net():
    """Shares network and ports with host device"""
    os.system("cat> " + nspawn_file + " <<EOF" + "\n" + '''[Exec]\n
    PrivateUsers=False\n
    \n
    [Network]\n
    Private=off\n
    VirtualEthernet=false\n
    EOF''' + "\n")


def priv_net():
    """first stage of setting up independent network for the container"""
    print("Here, there are a few options depending on the host's set up. \n")
    print("Is there currently a network bridge in place? (if unknown, enter 'n') \n")
    i = input(" ::> ")
    if i == "y":
        p_net_bridge()
    else:
        p_net_mvlan()


def p_net_bridge():
    """private network with a bridged network"""
    print("Enter the interface name of the network bridge")
    i = input(" ::> ")
    print("To enable ipv6, remove the comments [#] in " + nspawn_file)
    print("If manually setting ip details is preferred, edit this same file")
    os.system('cat> ' + nspawn_file + ' <<EOF \n')
    os.system("[Network]\nBridge=" + str(i) + "\n" + "EOF" + "\n")
    os.system("cat> " + ct_net_if + " <<EOF" + "\n" + '''[Match]\n
    Name=host*\n
    \n
    [Link]\n
    #ARP=True\n
    \n
    [Network]\n
    DHCP=yes\n
    #LinkLocalAddressing=yes\n
    #IPv6AcceptRA=yes\n
    \n
    [IPv6AcceptRA]\n
    #UseOnLinkPrefix=true\n
    #UseAutonomousPrefix=true\n
    EOF''' + "\n")


def p_net_mvlan():
    """set up a macvlan for private network attached to the host system"""
    print("Enter the interface name to use as the primary:\n")
    i = input(" ::> ")
    print('''For manual network settings, and/or to enable ipv6, 
    remove the comments '#' (at the beginning with lines) in 
    ''' + nspawn_file + ".")
    os.system("cat> " + nspawn_file + " <<EOF" + '''\n
    [Network]\n
    MACVLAN=''' + str(i) + "\nEOF" + "\n")
    os.system("cat> " + ct_net_mv + " <<EOF" + '''\n
    [Match]\n
    Name=mv*\n
    \n
    [Link]\n
    #ARP=True\n
    \n
    [Network]\n
    DHCP=yes\n
    #LinkLocalAddressing=yes\n
    #IPv6AcceptRA=yes\n
    \n
    [IPv6AcceptRA]\n
    #UseOnLinkPrefix=True\n
    #UseAutonomousPrefix=True\n
    EOF''' + "\n")


def systemd_nr_disable():
    """if nspawn network is set as host, this will disable systemd-networkd
     and systemd-resolved"""
    os.system('''(systemctl disable --now systemd-networkd \
    systemd-resolved) >/dev/null | machinectl shell ''' + cn)


def systemd_nr_enable():
    """if nspawn network is set as private, this will enable systemd-networkd
    and systemd-resolved"""
    os.system('''(systemctl enable --now systemd-networkd \
    systemd-resolved) >/dev/null | machinectl shell ''' + cn)
    
    
def ct_hostname():
    """sets a hostname for the container"""
    print("Would you like to set a hostname with domain?\n")
    while True:
        confirm = input(" ::> ")
        match confirm.upper():
            case "Y":
                print("Enter hostname:\n")
                hname = input(" ::> ")
                os.system("hostnamectl set-hostname " + hname + ''' | \
                          machinectl shell ''' + cn)
            case "N":
                pass
            case _:
                print("Please enter 'Y' or 'N' without the single quotes:\n")
                continue
        