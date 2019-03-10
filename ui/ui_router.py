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

class UIRouter:
    # Raspberry Pi pin configuration:
    KEY = [20, 21]

    RST = 19
    DC = 16
    busId = 0
    deviceId = 0

    bus = smbus.SMBus(1)
    address = 0x20

    def __init__(self, display):
        self._display = display
        self._display_width = self._display.width
        self._display_height = self._display.height

        self.screen = Image.new('1', (self._display_width, self._display_height))

        self._display.clear()
        self._display.image(self.screen)
        self._display.display()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.KEY, GPIO.IN, GPIO.PUD_UP)
        for channel in self.KEY:
            GPIO.add_event_detect(channel, GPIO.BOTH, self.key_handler, bouncetime=400)

        self._view = 'wifi'
        self._view_instances = {}
        self._views = {}

        self._selected = 0
        self._hselected = 0
        self._focused = None

    def _refresh_views(self):
        for view_name, view_instance in self._view_instances.items():
            self._views[view_name] = view_instance.view

    @property
    def views(self):
        return self._view_instances

    @views.setter
    def views(self, value):
        self._view_instances = value
        self._refresh_views()

    def beep_on(self):
        self.bus.write_byte(self.address,0x7F&self.bus.read_byte(self.address))
    def beep_off(self):
        self.bus.write_byte(self.address,0x80|self.bus.read_byte(self.address))

    def led_off(self):
        self.bus.write_byte(self.address,0x10|self.bus.read_byte(self.address))
    def led_on(self):
        self.bus.write_byte(self.address,0xEF&self.bus.read_byte(self.address))

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
            self.route(event=event)

    def element_event_handler(self, element_id, event, next):
        if event == 'blurred':
            self._focused = None
            self.route(event=event)

        return True

    def route(self, view = None, event = None):
        if view != None:
            self._view = view
        else:
            view = self._view

        screen_local = Image.new('1', (self._display_width, self._display_height))

        if view in self._view_instances:
            self._view_instances[view].callback(screen=screen_local, event=event)

        self.navigation(view=view, event=event)
        screen_local = self.render(screen=screen_local, view=view)

        if screen_local != self.screen:
            self.screen = screen_local
            self._display.clear()
            self._display.image(self.screen)
            self._display.display()

    def navigation(self, view, event, recursion=0):
        if self._focused == None:
            if event == 'down':
                self._selected = self._selected + 1
                if self._selected >= len(self._views[view]):
                    self._selected = 0
                self._hselected = 0
            elif event == 'up':
                self._selected = self._selected - 1
                if self._selected < 0:
                    self._selected = len(self._views[view]) - 1
                self._hselected = 0
            elif event == 'right':
                if 'horizontal' in self._views[view][self._selected]:
                    self._hselected = self._hselected + 1
                    if self._hselected >= len(self._views[view][self._selected]['horizontal']):
                        self._hselected = 0
            elif event == 'left':
                if 'horizontal' in self._views[view][self._selected]:
                    self._hselected = self._hselected - 1
                    if self._hselected < 0:
                        self._hselected = len(self._views[view][self._selected]['horizontal']) - 1
            elif event == 'click':
                if 'horizontal' in self._views[view][self._selected]:
                    if self._views[view][self._selected]['horizontal'][self._hselected]['element'].focus():
                        self._focused = self._views[view][self._selected]['horizontal'][self._hselected]
                    else:
                        self._views[view][self._selected]['horizontal'][self._hselected]['element'].event('click', None)
                else:
                    if self._views[view][self._selected]['element'].focus():
                        self._focused = self._views[view][self._selected]
                    else:
                        self._views[view][self._selected]['element'].event('click', None)

            if event != 'click':
                if len(self._views[view]) > 0 and 'element' in self._views[view][self._selected]:
                    if self._views[view][self._selected]['element'].can_highlight is False:
                        recursion = recursion + 1
                        if recursion <= len(self._views[view]):
                            return self.navigation(view=view, event=event, recursion=recursion)
                elif len(self._views[view]) > 0 and 'horizontal' in self._views[view][self._selected]:
                    if self._views[view][self._selected]['horizontal'][self._hselected]['element'].can_highlight is False:
                        recursion = recursion + 1
                        if recursion <= len(self._views[view]):
                            return self.navigation(view=view, event=event, recursion=recursion)
        else:
            self._focused['element'].event(event, None)

    def render(self, screen, view):
        for selected_element_index, selected_element in enumerate(self._views[view]):
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
                screen = selected_element['element'].render(screen=screen)
            elif 'horizontal' in selected_element:
                for selected_helement_index, selected_helement in enumerate(selected_element['horizontal']):
                    screen = selected_helement['element'].render(screen=screen)

        return screen

    def destroy(self):
        GPIO.cleanup()

