#!/usr/bin/env python3
# coding=utf8

import RPi.GPIO as GPIO
import smbus
import time

class InputGeneric:
    def __init__(self, keys=[20, 21], address=0x20, bus=smbus.SMBus(1)):
        self._event_handler = None
        self._keys = keys
        self._address = address
        self._bus = bus

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._keys, GPIO.IN, GPIO.PUD_UP)
        for channel in self._keys:
            GPIO.add_event_detect(channel, GPIO.BOTH, self.key_handler, bouncetime=400)

    @property
    def event_handler(self):
        return self._event_handler

    @event_handler.setter
    def event_handler(self, value):
        self._event_handler = value

    def key_handler(self, key):
        event = None

        if key == 20:
            time.sleep(0.01)
            event = 'click'
        else:
            self._bus.write_byte(self._address, 0x0F|self._bus.read_byte(self._address))
            value = self._bus.read_byte(self._address) | 0xF0

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
                self._bus.write_byte(self._address, 0x0F|self._bus.read_byte(self._address))
                value = self._bus.read_byte(self._address) | 0xF0
                time.sleep(0.01)

        if event != None and self._event_handler != None:
            self._event_handler(event=event)

    def destroy(self):
        print('All good')
