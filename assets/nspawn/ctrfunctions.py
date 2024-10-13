import os


def machdir(path):
    """
    This will create the machine directory if it does not exist
    '/var/lib/machines'
    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except ValueError:
            print('Please manually create machine folder with:')
            print('mkdir -p ' + path)


def nspawndir(path):
    """
    This will create the nspawn directory if it does not exist
    /etc/systemd/nspawn
    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except ValueError:
            print('Please manually create nspawn folder with:')
            print('mkdir -p ' + path)


def ndebian(ct_path):
    """Give the option to try unstable branch in container
    Selects stable otherwise and installs root fs"""
    print('Would you like to test the unstable branch? [y/n]\n')
    stbl = input(" ::> ")
    match stbl.upper():
        case "Y":
            branch = 'unstable '
        case _:
            branch = 'stable '
    os.system("debootstrap --include=dbus-broker,systemd-resolved "
              + branch + " " + ct_path)


def nfedora(ct_path):
    """Here we set up the container with fedora 40 as the base. Potentially it
    would check which version is current and auto select that one"""
    releasever = 40
    os.system("\"$(cat fedora-repo-data.xml)\" >> /etc/dnf/dnf.conf"
              + "\ndnf --releasever=" + str(releasever) + " --best " +
              "--setopt=install_weak_deps=False --installroot="
              + ct_path + "/ install -y dhcp-client dnf fedora-release" +
              "glibc glibc-langpack-en glibc-langpack-de iputils less" +
              "ncurses passwd systemd util-linux")


def narch(ct_path):
    """Set up process for a minimal arch container"""
    os.system("pacstrap -K -c " + ct_path + "/ base dbus-broker")



def spwn_boot_shell(cn):
    """one of 2 boot options for the container. This does not load dbus"""
    os.system("/usr/bin/systemd-nspawn -M " + cn)


def spwn_boot_dbus(cn):
    """second of 2 boot options. This one loads dbus"""
    os.system("/usr/bin/systemd-nspawn -M " + cn + " -b")


def host_net(nspawn_file):
    """Shares network and ports with host device"""
    os.system("cat> " + nspawn_file + " <<EOF" + "\n" +
              "[Exec]\nPrivateUsers=False\n\n[Network]\n" +
              "Private=off\nVirtualEthernet=false\nEOF" + "\n")


def priv_net(nspawn_file, ct_net_if, ct_net_mv):
    """first stage of setting up independent network for the container"""
    print("Here, there are a few options depending on the host's set up. \n")
    print("Is there currently a network bridge in place?" +
          "\n(if unknown, enter 'n') \n")
    i = input(" ::> ")
    if i.upper() == "Y":
        p_net_bridge(nspawn_file, ct_net_if)
    else:
        p_net_mvlan(nspawn_file, ct_net_mv)


def p_net_bridge(nspawn_file, ct_net_if):
    """private network with a bridged network"""
    print("Enter the interface name of the network bridge")
    i = input(" ::> ")
    print("To enable ipv6, remove the comments [#] in " + nspawn_file)
    print("If manually setting ip details is preferred, edit this same file")
    os.system('cat> ' + nspawn_file + ' <<EOF' + "\n[Network]\n" +
              "Bridge=" + str(i) + "\n" + "EOF" + "\n")
    os.system("cat> " + ct_net_if + " <<EOF" + "\n[Match]\nName=host*\n" +
              "\n[Link]\n#ARP=True\n\n[Network]\nDHCP=yes\n" +
              "#LinkLocalAddressing=yes\n#IPv6AcceptRA=yes\n\n" +
              "[IPv6AcceptRA]\n#UseOnLinkPrefix=true\n" +
              "#UseAutonomousPrefix=true\nEOF" + "\n")


def p_net_mvlan(nspawn_file, ct_net_mv):
    """set up a macvlan for private network attached to the host system"""
    print("Enter the interface name to use as the primary:\n")
    i = input(" ::> ")
    print('''For manual network settings, and/or to enable ipv6,
    remove the comments '#' (at the beginning with lines) in
    ''' + nspawn_file + ".")
    os.system("cat> " + nspawn_file + " <<EOF" + '''\n
    [Network]\n
    MACVLAN=''' + str(i) + "\nEOF" + "\n")
    os.system("cat> " + ct_net_mv + " <<EOF" + "\n[Match]" +
              "\nName=mv*\n\n[Link]\n#ARP=True\n\n" +
              "[Network]\nDHCP=yes\n#LinkLocalAddressing=yes\n" +
              "#IPv6AcceptRA=yes\n\n[IPv6AcceptRA]\n" +
              "#UseOnLinkPrefix=True\n#UseAutonomousPrefix=True\n" +
              "EOF" + "\n")

    def ct_hostname(ct_path):
        """sets a hostname for the container"""
        print("Would you like to set a custom hostname with domain?\n")
        while True:
            confirm = input(" ::> ")
            match confirm.upper():
                case "Y":
                    print("Enter hostname:\n")
                    hname = input(" ::> ")
                    os.system("/usr/bin/systemd-nspawn -d " + ct_path +
                              " hostnamectl set-hostname " + hname)
                case "N":
                    pass
                case _:
                    print("Please enter 'Y' or 'N' without the single quotes:\n")
                    continue


def firstcmd(__mach_path__, __nspawn_path__):
    machdir(__mach_path__)
    nspawndir(__nspawn_path__)


def secondcmd():