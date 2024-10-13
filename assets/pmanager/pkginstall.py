#!/usr/bin/env python3
import os
import re
from test.pmanager.pkgmanager import *
# from pmanager.pkgmanager import pakbins,apt_cmds,dnf_cmds,pac_cmds

choices = []
chosen = None
pkgmgrvar = None

def find_pmgr(__pakbins__, __choices__, __apt_cmds__, __dnf_cmds__, __pac_cmds__):
    """
    This potentially determines the primary package manager
    if its binary exists
    """
    for b in __pakbins__:
        if os.path.exists(b):
            __choices__.append(b)
            if len(__choices__) == 1:
                __chosen__ = __choices__[0]
                deps_pmgr(__chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__)
            else:
                select_mgr(__choices__, __pakbins__, __apt_cmds__, __dnf_cmds__, __pac_cmds__)


def select_mgr(__choices__, __pakbins__, __apt_cmds__, __dnf_cmds__, __pac_cmds__):
    """
    If more than one package manager is found in the previous function,
    this will prmpt the user to select the preferred one
    """
    print('More than one package manager found.\n')
    print('Please choose the default one to use:\n')
    for li in __choices__:
        print(li)
    while True:
        i = input(' ::> ')
        match i:
            case re.Match('.*(apt)'):
                __chosen__ = __pakbins__[0]
                deps_pmgr(__chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__)
            case re.Match('.*(dnf)'):
                __chosen__ = __pakbins__[1]
                deps_pmgr(__chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__)
            case re.Match('.*(pacman)'):
                __chosen__ = __pakbins__[2]
                deps_pmgr(__chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__)
            case _:
                print('Please type out the name of your choice:\n')
                continue


def deps_pmgr(__chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__):
    """
    This step adds specific container installation dependencies
    to the chosen package manager dependencies in a single variable
    """
    match __chosen__:
        case re.Match('.*(apt)'):
            __pkgmgrvar__ = __apt_cmds__
            os.system(__pkgmgrvar__)
        case re.Match('.*(dnf)'):
            __pkgmgrvar__ = __dnf_cmds__
            os.system(__pkgmgrvar__)
        case re.Match('.*(pacman)'):
            __pkgmgrvar__ = __pac_cmds__
            os.system(__pkgmgrvar__)


def main(__pakbins__, __choices__, __chosen__, __apt_cmds__, __dnf_cmds__, __pac_cmds__):
    find_pmgr(__pakbins__, __choices__)
    if __chosen__ is None:
        select_mgr(__choices__, __pakbins__, str(__apt_cmds__), str(__dnf_cmds__), str(__pac_cmds__))
    deps_pmgr(__chosen__, str(__apt_cmds__), str(__dnf_cmds__), str(__pac_cmds__))


if __name__ == "__main__":
    main(pakbins, choices, chosen, apt_cmds, dnf_cmds, pac_cmds)