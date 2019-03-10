#!/usr/bin/env python3
# coding=utf8

import sys
from ui.ui import UI

ui = UI()

def main():
    ui.display()
    # ^ that's a loop
    ui.destroy()
    print("Leaving main()")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit\n")
        ui.destroy()
        sys.exit(0)
