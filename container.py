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
        base = int(input(" ::> "))
        match base:
            case 1:
                bd = distros[0]
            case 2:
                bd = distros[1]
            case 3:
                bd = distros[3]
            case _:
                print("Enter a single digit [1-3]:\n")
                continue
        return bd


def ntype():
    print("Choose a network type:\n")
    nets = ["host", "private"]
    num = 1
    for i in nets:
        print(str(num) + " " + i)
        num += 1
    while True:
        net = int(input(" ::> "))
        match net:
            case 1:
                nt = nets[0]
            case 2:
                nt = nets[1]
            case _:
                print("Enter a number [1-2]:\n")
                continue
        return nt


class Container:
    def __init__(self, name, base_distro, net_type):
        self.name = name
        self.base_distro = base_distro
        self.net_type = net_type
