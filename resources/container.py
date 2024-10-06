#!/usr/bin/env python3

def cname():
    print("Please enter a unique name for this container:\n")
    __cname__ = input(" ::> ")
    return __cname__


def base_distro():
    print("Select a distribution:\n")
    distros = ["debian", "fedora", "arch"]
    num = 1
    for i in distros:
        print(str(num) + " " + i)
        num += 1
    while True:
        base = input(" ::> ")
        match int(base):
            case 1:
                __base_distro__ = distros[0]
                return __base_distro__
            case 2:
                __base_distro__ = distros[1]
                return __base_distro__
            case 3:
                __base_distro__ = distros[2]
                return __base_distro__
            case _:
                print("Please enter a single digit [1-3]:\n")
                continue


def net_type():
    print("Choose a network type:\n")
    types = ["host", "private"]
    num = 1
    for i in types:
        print(str(num) + " " + i)
        num += 1
    while True:
        net = input(" ::> ")
        match int(net):
            case 1:
                __net_type__ = types[0]
                return __net_type__
            case 2:
                __net_type__ = types[1]
                return __net_type__
            case _:
                print("Enter a number [1-2]:\n")
                continue


class Container:
    def __init__(self):
        self.cname = cname()
        self.base_distro = base_distro()
        self.net_type = net_type()


if __name__ == "__main__":
    nspawn = Container()
