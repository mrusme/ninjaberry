#!/usr/bin/env python3
# coding=utf8

import sys
from ui.ui import UI
from bettercap import Bettercap

bettercap = Bettercap()

ui = UI(external_resources={ 'bettercap': bettercap })

def destroy():
    ui.destroy()
    bettercap.stop()

def main():
    ui.display()
    # ^ that's a loop
    destroy()
    print("Leaving main()")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit\n")
        destroy()
        sys.exit(0)
