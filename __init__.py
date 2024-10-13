from functions import checkroot
from main import main as start


def __init__():
    checkroot()

    print("Hello! Thanks for giving pyspawn a try. It's been torturous fun " +
    "working on this project. I hope you'll find it a little easier " +
    "to work with systemd-nspawn moving forward. Enjoy! ")

    print("\n\nLet's get started:\n")

    start()


if __name__ == "__init__":
    __init__()