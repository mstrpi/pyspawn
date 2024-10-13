#!/usr/bin/env python3
"""defining all functions for pyspawn"""
import os
import sys


def checkroot():
    """
    Here it should verify admin privileges
    """
    if os.getuid() == 0:
        pass
    else:
        sys.exit("Super user access required, " +
                 "please try again as root or with sudo.\n")


def checkbtrfs(ct_path):
    """
    Specify with user if using btrfs subvolume for container
    """
    print('''\nIf btrfs is in place, should a new subvolume be created?
    (This defaults to ''' + ct_path + ").")
    print("[ If you're not sure what btrfs is, please enter 'n' ]\n")
    i = input(" ::> ")
    if i.lower == "y":
        os.system('btrfs subvolume create ' + ct_path)


def selinux_disable():
    """This checks if selinux binary is present to disable it during password
    set for root"""
    os.system("if [ -f /usr/sbin/setenforce ]; then setenforce 0; fi")


def selinux_enable():
    """Checks if setenforce binary is present to re-enable it after root
    password has been set"""
    os.system("if [ -f /usr/sbin/setenforce ]; then setenforce 1; fi")


def root_passwd(cn):
    """function to set root password for container"""
    os.system("/usr/bin/systemd-nspawn -M " + cn + " passwd")


def systemd_nr_disable(ct_path):
    """if nspawn network is set as host, this will disable systemd-networkd
     and systemd-resolved"""
    os.system("/usr/bin/systemd-nspawn -d " + ct_path +
              " systemctl disable systemd-networkd systemd-resolved")


def systemd_nr_enable(ct_path):
    """if nspawn network is set as private, this will enable systemd-networkd
    and systemd-resolved"""
    os.system("/usr/bin/systemd-nspawn -d " + ct_path +
              " systemctl enable systemd-networkd")


def outro(cn):
    """end script"""
    print(cn + " has been created. /usr/bin/machinectl is available for "
          + "some common commands. To enable/disable " + cn + " at boot, " +
          cn + "use:\n'machinectl [ enable | disable ] " + cn + "'")
    print("To start/stop " + cn + ":\n'machinectl [ start | stop ] " + cn
          + "'")
    print("See additional help via: man machinectl and man systemd-nspawn")
    print("\nEnjoy your shiny new nspawn container!\n")