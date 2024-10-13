#!/usr/bin/env python3
"""
This library provides definitions for what is a package manager, and
what dependencies are needed to install for systemd-nspawn to work in
users selected container base-distribution. The paired module will do
the function calls based on this information.
"""
import json

_depends = "systemd-container dbus-broker "
deb_depends = "debootstrap " + _depends
fed_depends = "dnf " + _depends
arc_depends = "arch-install-scripts " + _depends
x_depends = [deb_depends, fed_depends, arc_depends]
print(x_depends)

with open('pkg_mgrs.json', 'r', encoding='UTF-8') as pmgrjson:
    data = json.load(pmgrjson)

    for mgr in data["pkg_managers"]:
        debian = {"apt": mgr["pkg_managers"][0]["apt"]}
        apt = debian["apt"]

        fedora = {"dnf": mgr["pkg_managers"][1]["dnf"]}
        dnf = fedora["dnf"]

        arch = {"pacman": mgr["pkg_managers"][2]["pacman"]}
        pac = arch["pacman"]
        pakmans = [apt, dnf, pac]

        for pbin in debian["apt"]:
            aptbin = {"bin": pbin["apt"][0]["bin"]}
        for pcmd in debian["apt"]:
            acmd = {"commands": pcmd["apt"][1]["commands"]}
            for aupcmd in acmd["commands"]:
                aptup = {"update": aupcmd["commands"][0]["update"]}
            for ainstcmd in acmd["commands"]:
                aptinst = {"install": ainstcmd["commands"][1]["install"]}

        for pbin in fedora["dnf"]:
            dnfbin = {"bin": pbin["dnf"][1]["bin"]}
        for pcmd in fedora["dnf"]:
            dcmd = {"commands": pcmd["dnf"][1]["commands"]}
            for dupcmd in dcmd["commands"]:
                dnfup = {"update": dupcmd["commands"][0]["update"]}
            for dinstcmd in dcmd["commands"]:
                dnfinst = {"install": dinstcmd["commands"][1]["install"]}

        for pbin in arch["pacman"]:
            pacbin = {"pacman": pbin["pacman"][2]["bin"]}
        for pcmd in arch["pacman"]:
            pacmd = {"commands": pcmd["pacman"][0]["commands"]}
            for pupcmd in pacmd["commands"]:
                pacup = {"update": pupcmd["commands"][0]["update"]}
            for pinstcmd in pacmd["commands"]:
                pacinst = {"install": pinstcmd["commands"]["install"]}

pakbins = [aptbin["bin"], dnfbin["bin"], pacbin["bin"]]
apt_cmds = [aptup["update"], aptinst["install"] + deb_depends]
dnf_cmds = [dnfup["update"], dnfinst["install"] + fed_depends]
pac_cmds = [pacup["update"], pacinst["install"] + arc_depends]

print(pakmans, apt_cmds, deb_depends, dnf_cmds, fed_depends, pac_cmds, arc_depends)