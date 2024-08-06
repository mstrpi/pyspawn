#!/usr/bin/env python3
def cname():
    print("Please enter a unique name for this container:\n")
    cn = input(" ::> ")
    return cn


def bdistro():
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
                bd = distros[0]
                return bd
            case 2:
                bd = distros[1]
                return bd
            case 3:
                bd = distros[2]
                return bd
            case _:
                print("Enter a single digit [1-3]:\n")
                continue


def ntype():
    print("Choose a network type:\n")
    nets = ["host", "private"]
    num = 1
    for i in nets:
        print(str(num) + " " + i)
        num += 1
    while True:
        net = input(" ::> ")
        match int(net):
            case 1:
                nt = nets[0]
                return nt
            case 2:
                nt = nets[1]
                return nt
            case _:
                print("Enter a number [1-2]:\n")
                continue


class Container:
    def __init__(self, name, base_distro, net_type):
        self.name = name
        self.base_distro = base_distro
        self.net_type = net_type
