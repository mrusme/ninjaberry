#!/usr/bin/env python3
# coding=utf8

import RPi.GPIO as GPIO
import spidev as SPI
import SSD1306
import smbus
import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from ui.ui_router import UIRouter

from ui.ui_animation import UIAnimation
from ui.ui_button import UIButton
from ui.ui_label import UILabel
from ui.ui_line import UILine
from ui.ui_list import UIList

from views.view_logo import ViewLogo
from views.view_wifi import ViewWifi

class UI:
    # Raspberry Pi pin configuration:
    KEY = [20, 21]

    RST = 19
    DC = 16
    busId = 0
    deviceId = 0

    bus = smbus.SMBus(1)
    address = 0x20

    def __init__(self):
        # 128x32 display with hardware SPI:
        self.disp = SSD1306.SSD1306(rst=self.RST,dc=self.DC,spi=SPI.SpiDev(self.busId,self.deviceId))
        self.disp.begin()
        self.width = self.disp.width
        self.height = self.disp.height
        self.screen = Image.new('1', (self.width, self.height))
        self.disp.clear()
        self.disp.image(self.screen)
        self.disp.display()

        self.resources = {
            'display': {
                'width': self.disp.width,
                'height': self.disp.height
            },
            'fonts': {
                'hack': {
                    'size': 8,
                    'ttf': ImageFont.truetype('assets/Hack-Regular.ttf', 8)
                },
                'kosugi': {
                    'size': 8,
                    'ttf': ImageFont.truetype('assets/KosugiMaru-Regular.ttf', 8)
                },
                'fa_solid': {
                    'size': 11,
                    'ttf': ImageFont.truetype('assets/fa-solid-900.ttf', 11)
                },
                'fa_regular': {
                    'size': 11,
                    'ttf': ImageFont.truetype('assets/fa-regular-400.ttf', 11)
                },
                'fa_brands': {
                    'size': 11,
                    'ttf': ImageFont.truetype('assets/fa-brands-400.ttf', 11)
                }
            }
        }

        self.router = UIRouter(self.disp)
        self.router.views = {
            'logo': ViewLogo(resources=self.resources, event_handler=self.router.element_event_handler),
            'wifi': ViewWifi(resources=self.resources, event_handler=self.router.element_event_handler)
        }

    def destroy():
        self.router.destroy()

    def display(self):
        while True:
            self.router.route()
            time.sleep(0.1)
