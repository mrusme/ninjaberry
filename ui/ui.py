#!/usr/bin/env python3
# coding=utf8

import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from displays.display_ssd1306 import DisplaySSD1306

from inputs.input_generic import InputGeneric

from outputs.output_buzzer import OutputBuzzer
from outputs.output_led import OutputLED

from ui.ui_router import UIRouter

from ui.ui_animation import UIAnimation
from ui.ui_button import UIButton
from ui.ui_label import UILabel
from ui.ui_line import UILine
from ui.ui_list import UIList

from views.view_logo import ViewLogo
from views.view_under_construction import ViewUnderConstruction

from views.view_wifi import ViewWifi
from views.view_wifi_scan_aps import ViewWifiScanAps
from views.view_wifi_ap_actions import ViewWifiApActions

class UI:
    def __init__(self, external_resources = {}):
        self._display = DisplaySSD1306()
        self._display.begin()
        self._screen = Image.new('1', (self._display.width, self._display.height))
        self._display.clear()
        self._display.image(self._screen)
        self._display.display()

        self._inputs = {
            'generic': InputGeneric()
        }

        self._outputs = {
            'buzzer': OutputBuzzer(),
            'led1': OutputLED()
        }

        self._resources = {
            'display': {
                'width': self._display.width,
                'height': self._display.height
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
            },
            'external': external_resources
        }

        self._router = UIRouter(display=self._display, inputs=self._inputs, outputs=self._outputs)
        self._router.views = {
            'logo': ViewLogo(resources=self._resources, event_handler=self._router.element_event_handler),
            'wifi': ViewWifi(resources=self._resources, event_handler=self._router.element_event_handler),
            'wifi_scan_aps': ViewWifiScanAps(resources=self._resources, event_handler=self._router.element_event_handler),
            'wifi_ap_actions': ViewWifiApActions(resources=self._resources, event_handler=self._router.element_event_handler),
            'bt': ViewUnderConstruction(resources=self._resources, event_handler=self._router.element_event_handler),
            'eth': ViewUnderConstruction(resources=self._resources, event_handler=self._router.element_event_handler),
            'settings': ViewUnderConstruction(resources=self._resources, event_handler=self._router.element_event_handler)
        }

    def display(self):
        while True:
            self._router.route()
            time.sleep(0.1)

    def destroy(self):
        self._router.destroy()
        for input_name, input_instance in self._inputs.items():
            input_instance.destroy()
        for output_name, output_instance in self._outputs.items():
            output_instance.destroy()
        self._display.destroy()
