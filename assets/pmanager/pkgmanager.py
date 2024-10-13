#!/usr/bin/env python3
"""
This library provides definitions for what is a package manager, and
what dependencies are needed to install for systemd-nspawn to work in
users selected container base-distribution. The paired module will do
the function calls based on this information.
"""
import json


def set_depends():
    _depends = 'systemd-container dbus-broker '
    deb_depends = 'debootstrap ' + _depends
    fed_depends = 'dnf ' + _depends
    arc_depends = 'arch-install-scripts ' + _depends
    x_depends = [deb_depends, fed_depends, arc_depends]
    print(x_depends)


def set_jsonpmgrs():
    with open('pkg_mgrs.json', 'r', encoding='UTF-8') as pmgr:
        data = json.load(pmgr)
        for mgr in data['pkg_managers']:
            print(type(mgr))
            debian = {'apt': mgr['pkg_managers'][0]['apt']}
            apt = debian['apt']
            fedora = {'dnf': mgr['pkg_managers'][0]['dnf']}
            dnf = fedora['dnf']
            arch = {'pacman': mgr['pkg_managers'][0]['pacman']}
            pac = arch['pacman']
            pakmans = [apt, dnf, pac]
            print(type(pakmans))
            for bins in mgr['apt']:
                apt = {'bin': bins['apt'][0]['bin']}
                abin = apt['bin']
            for bins in mgr['dnf']:
                dnf = {'bin': bins['dnf'][1]['bin']}
                dbin = dnf['bin']
            for bins in mgr['pacman']:
                pac = {'bin': bins['pacman'][2]['bin']}
                pbin = pac['bin']
                jpmbins = [abin, dbin, pbin]
                print(type(jpmbins))



        for pbin in debian['apt']:
            aptbin = {'bin': pbin['apt'][0]['bin']}
        for pcmd in debian['apt']:
            acmd = {'commands': pcmd['apt'][1]['commands']}
            for aupcmd in acmd['commands']:
                aptup = {'update': aupcmd['commands'][0]['update']}
            for ainstcmd in acmd['commands']:
                aptinst = {'install': ainstcmd['commands'][1]['install']}

        for pbin in fedora['dnf']:
            dnfbin = {'bin': pbin['dnf'][1]['bin']}
        for pcmd in fedora['dnf']:
            dcmd = {'commands': pcmd['dnf'][1]['commands']}
            for dupcmd in dcmd['commands']:
                dnfup = {'update': dupcmd['commands'][0]['update']}
            for dinstcmd in dcmd['commands']:
                dnfinst = {'install': dinstcmd['commands'][1]['install']}

        for pbin in arch['pacman']:
            pacbin = {'pacman': pbin['pacman'][2]['bin']}
        for pcmd in arch['pacman']:
            pacmd = {'commands': pcmd['pacman'][0]['commands']}
            for pupcmd in pacmd['commands']:
                pacup = {'update': pupcmd['commands'][0]['update']}
            for pinstcmd in pacmd['commands']:
                pacinst = {'install': pinstcmd['commands']['install']}

pakbins = [str(aptbin['bin']), str(dnfbin['bin']), str(pacbin['bin'])]
apt_cmds = [str(aptup['update']), [str(aptinst['install']) + str(deb_depends)]]
dnf_cmds = [str(dnfup['update']), [str(dnfinst['install']) + str(fed_depends)]]
pac_cmds = [str(pacup['update']), str(pacinst['install'] + arc_depends)]

print(pakmans, apt_cmds, deb_depends, dnf_cmds, fed_depends, pac_cmds, arc_depends)