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

from ui_list import UIList
from ui_button import UIButton

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
        self.disp.clear()
        self.disp.display()

        self.font_hack_size = 8
        self.font_hack = ImageFont.truetype('assets/Hack-Regular.ttf', self.font_hack_size)

        self.font_kosugi_size = 8
        self.font_kosugi = ImageFont.truetype('assets/KosugiMaru-Regular.ttf', self.font_kosugi_size)

        self.font_fa_solid_size = 11
        self.font_fa_solid = ImageFont.truetype('assets/fa-solid-900.ttf', self.font_fa_solid_size)

        self.font_fa_regular_size = 11
        self.font_fa_regular = ImageFont.truetype('assets/fa-regular-400.ttf', self.font_fa_regular_size)

        self.font_fa_brands_size = 11
        self.font_fa_brands = ImageFont.truetype('assets/fa-brands-400.ttf', self.font_fa_brands_size)

        self.background = Image.new('1', (self.width, self.height))
        self.content = Image.new('1', (self.width, self.height))
        self.logo_frames = [
                Image.open('assets/bettercap01.bmp').convert('1'),
                Image.open('assets/bettercap02.bmp').convert('1'),
                Image.open('assets/bettercap03.bmp').convert('1'),
                Image.open('assets/bettercap04.bmp').convert('1')
            ]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.KEY, GPIO.IN, GPIO.PUD_UP)
        for channel in self.KEY:
            GPIO.add_event_detect(channel, GPIO.BOTH, self.key_handler, bouncetime=400)

        self.view = 'main'
        self.views = {
            'main': [
                {
                    'id': 'menu',
                    'horizontal': [
                        {
                            'id': 'button_wifi',
                            'element': UIButton(
                                resources = { 'font': { 'ttf': self.font_fa_solid, 'size': self.font_fa_solid_size } },
                                event_handler = (lambda ev, nxt: self.element_event_handler('button_wifi', ev, nxt)),
                                position = [0, 0],
                                size = [15, 14],
                                label = chr(0xf1eb)
                            )
                        },
                        {
                            'id': 'button_bt',
                            'element': UIButton(
                                resources = { 'font': { 'ttf': self.font_fa_brands, 'size': self.font_fa_brands_size } },
                                event_handler = (lambda ev, nxt: self.element_event_handler('button_bt', ev, nxt)),
                                position = [16, 0],
                                size = [15, 14],
                                label = chr(0xf294)
                            )
                        },
                        {
                            'id': 'button_eth',
                            'element': UIButton(
                                resources = { 'font': { 'ttf': self.font_fa_solid, 'size': self.font_fa_solid_size } },
                                event_handler = (lambda ev, nxt: self.element_event_handler('button_eth', ev, nxt)),
                                position = [32, 0],
                                size = [15, 14],
                                label = chr(0xf796)
                            )
                        },
                        {
                            'id': 'button_settings',
                            'element': UIButton(
                                resources = { 'font': { 'ttf': self.font_fa_solid, 'size': self.font_fa_solid_size } },
                                event_handler = (lambda ev, nxt: self.element_event_handler('button_settings', ev, nxt)),
                                position = [48, 0],
                                size = [15, 14],
                                label = chr(0xf013)
                            )
                        }
                    ]
                },
                {
                    'id': 'list_ssid_functions',
                    'element': UIList(
                        resources = { 'font': { 'ttf': self.font_hack, 'size': self.font_hack_size } },
                        event_handler = (lambda ev, nxt: self.element_event_handler('list_ssid_functions', ev, nxt)),
                        position = [0, 30],
                        size = [(self.width - 1), 10],
                        entries = ['Capture handshake', 'Deauth', 'Lolz', 'Dafaq', 'Fu', 'Bar'],
                        selected = 0
                    )
                },
                {
                    'id': 'list_ssid_functions2',
                    'element': UIList(
                        resources = { 'font': { 'ttf': self.font_hack, 'size': self.font_hack_size } },
                        event_handler = (lambda ev, nxt: self.element_event_handler('list_ssid_functions2', ev, nxt)),
                        position = [0, 40],
                        size = [(self.width - 1), 10],
                        entries = ['Capture handshake', 'Deauth', 'Lolz', 'Dafaq', 'Fu', 'Bar'],
                        selected = 0
                    )
                }
            ]
        }

        self._selected = 0
        self._hselected = 0
        self._focused = None

    def destroy():
        GPIO.cleanup()

    def beep_on(self):
        self.bus.write_byte(self.address,0x7F&self.bus.read_byte(self.address))
    def beep_off(self):
        self.bus.write_byte(self.address,0x80|self.bus.read_byte(self.address))

    def led_off(self):
        self.bus.write_byte(self.address,0x10|self.bus.read_byte(self.address))
    def led_on(self):
        self.bus.write_byte(self.address,0xEF&self.bus.read_byte(self.address))

    def logo(self):
        for x in range(0,3):
            for logo_frame in range(0,4):
                self.content.paste(self.logo_frames[logo_frame], (0,0))
                self.screen = Image.composite(self.background, self.content, self.background)
                draw = ImageDraw.Draw(self.screen)
                draw.text((31,0), 'ベッターキャップ', font=self.font_kosugi, fill=255)
                self.disp.image(self.screen)
                self.disp.display()
                time.sleep(0.1)

    def key_handler(self, key):
        event = None

        if key == 20:
            self.beep_on()
            time.sleep(0.01)
            self.beep_off()
            time.sleep(0.01)
            event = 'click'
        else:
            self.bus.write_byte(self.address, 0x0F|self.bus.read_byte(self.address))
            value = self.bus.read_byte(self.address) | 0xF0

            if value == 0xF7:
                event = 'right'
            elif value == 0xFB:
                event = 'down'
            elif value == 0xFD:
                event = 'up'
            elif value == 0xFE:
                event = 'left'
            elif value == 0xFF:
                event = None
            while value != 0xFF:
                self.bus.write_byte(self.address, 0x0F|self.bus.read_byte(self.address))
                value = self.bus.read_byte(self.address) | 0xF0
                time.sleep(0.01)

        if event != None:
            self.router(event=event)

    def element_event_handler(self, element_id, event, next):
        if event == 'blurred':
            self._focused = None
            self.router(event=event)

        return True

    def view_main(self, event = None):
        self.content = Image.new('1', (self.width, self.height))
        self.screen = Image.composite(self.background, self.content, self.background)
        draw = ImageDraw.Draw(self.screen)

        draw.line([0, 15, 128, 15], fill=255, width=1, joint=None)
        draw.text((0,16), '74:ba:3a:c7:66:e0', font=self.font_hack, fill=255)

    def navigation(self, view, event):
        if self._focused == None:
            if event == 'down':
                self._selected = self._selected + 1
                if self._selected >= len(self.views[view]):
                    self._selected = 0
                self._hselected = 0
            elif event == 'up':
                self._selected = self._selected - 1
                if self._selected < 0:
                    self._selected = len(self.views[view]) - 1
                self._hselected = 0
            elif event == 'right':
                if 'horizontal' in self.views[view][self._selected]:
                    self._hselected = self._hselected + 1
                    if self._hselected >= len(self.views[view][self._selected]['horizontal']):
                        self._hselected = 0
            elif event == 'left':
                if 'horizontal' in self.views[view][self._selected]:
                    self._hselected = self._hselected - 1
                    if self._hselected < 0:
                        self._hselected = len(self.views[view][self._selected]['horizontal']) - 1
            elif event == 'click':
                if 'horizontal' in self.views[view][self._selected]:
                    if self.views[view][self._selected]['horizontal'][self._hselected]['element'].focus():
                        self._focused = self.views[view][self._selected]['horizontal'][self._hselected]
                    else:
                        self.views[view][self._selected]['horizontal'][self._hselected]['element'].event('click', None)
                else:
                    if self.views[view][self._selected]['element'].focus():
                        self._focused = self.views[view][self._selected]
                    else:
                        self.views[view][self._selected]['element'].event('click', None)
        else:
            self._focused['element'].event(event, None)

        self.render(view=view)

    def render(self, view):
        draw = ImageDraw.Draw(self.screen)

        for selected_element_index, selected_element in enumerate(self.views[view]):
            if self._focused == None:
                if selected_element_index == self._selected:
                    if 'element' in selected_element:
                        selected_element['element'].highlight()
                    elif 'horizontal' in selected_element:
                        for selected_helement_index, selected_helement in enumerate(selected_element['horizontal']):
                            if selected_helement_index == self._hselected:
                                selected_helement['element'].highlight()
                            else:
                                selected_helement['element'].lowlight()
                else:
                    if 'element' in selected_element:
                        selected_element['element'].lowlight()
                    elif 'horizontal' in selected_element:
                        for selected_helement_index, selected_helement in enumerate(selected_element['horizontal']):
                            selected_helement['element'].lowlight()

            if 'element' in selected_element:
                selected_element['element'].render(draw)
            elif 'horizontal' in selected_element:
                for selected_helement_index, selected_helement in enumerate(selected_element['horizontal']):
                    selected_helement['element'].render(draw)

        self.disp.image(self.screen)
        self.disp.display()


    def router(self, view = None, event = None):
        if view != None:
            self.view = view
        else:
            view = self.view


        if view == 'main':
            self.view_main(event=event)

        self.navigation(view=view, event=event)

    def display(self):
        self.router()
        while True:
            time.sleep(10)
