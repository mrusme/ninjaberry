Ninjaberry
==========

![Ninjaberry](ninjaberry.gif)

*(Short demo of Ninjaberry. Wait for the huge GIF to load...)*

## Introduction

Ninjaberry is a Python 3 application that provides a minimalistic UI for running @Bettercap on the Raspberry Pi platform. It basically allows you to run around with your RPi + battery-pack and perform the most common Bettercap tasks (e.g. deauth) without needing a laptop or even a keyboard at all.

As of right now it has been developed for and tested on the [Raspberry Pi 3 A+](https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/) using a [Waveshare Pioneer600](https://www.waveshare.com/pioneer600.htm) (yes, the Pioneer600 is compatible with the Raspberry Pi 3 A+, even though Waveshare doesn't explicitly list it), but the code was written in a way in which it should quite easily be possible to port it to other HATs/displays/inputs as well.

A tiny UI library was built on top of [Pillow](https://pypi.org/project/Pillow/) and integrated into Ninjaberry, allowing developers to easily create views containing UI elements like labels, buttons and lists. In theory those elements are scalable, meaning that the UI should be working on larger displays as well. I wouldn't try anything smaller than 128x64px though.

If you have any hardware you'd like to get this project working on feel free to [create an issue on GitHub](https://github.com/mrusme/ninjaberry/issues/new) with your specific setup and I'll try to help you get Ninjaberry running on it.

## Installation

Your device needs to have drivers for the network interfaces you'd like to use and of course you need to have Bettercap installed. I won't go into details about installing either. Please rtfm of your hardware and check [Bettercap's installation guide](https://www.bettercap.org/installation/#compiling-from-sources) for help on this topic.

PS: The Docker installation won't work, since Ninjaberry requires the `bettercap` binary to be available within `$PATH`.

In order to get Ninjaberry running you need a couple of libraries:

```bash
pip3 install RPi.GPIO spidev Pillow
```

## Usage

```bash
python3 ./ninjaberry.py
```

Keep in mind that this is experimental software at the moment. Feel free to tinker around, but don't expect anything to be working as it is pre-0.1 as of right now.

## Features

So far Ninjaberry can:

### WiFi

- Scan for APs for a custom amount of time, through a configurable iface
- Display a list of all found APs, allow you to pick one
- Display information on the selected AP, allowing you to run a handshake scan + deauth
- Run the handshake scan + deauth

### Bluetooth

- Nothing yet

### Ethernet

- Nothing yet

### Settings

- Nothing to tweak around yet

## Common use cases

If you have commands you usually run with Bettercap, feel free to [create an issue on GitHub](https://github.com/mrusme/ninjaberry/issues/new) and request implementation of those!

## "Let me tell you..."

Sure, [tell me](https://twitter.com/intent/tweet?text=@mrusme%20regarding%20Ninjaberry,%20let%20me%20tell%20you%20that...)!
