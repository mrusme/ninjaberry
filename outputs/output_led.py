#!/usr/bin/env python3
# coding=utf8

import smbus
import time

class OutputLED:
    def __init__(self, address=0x20, bus=smbus.SMBus(1)):
        self._event_handler = None
        self._address = address
        self._bus = bus

    def _led_off(self):
        self._bus.write_byte(self._address,0x10|self._bus.read_byte(self._address))
    def _led_on(self):
        self._bus.write_byte(self._address,0xEF&self._bus.read_byte(self._address))

    def short(self):
        self._led_on()
        time.sleep(0.1)
        self._led_off()

    def destroy(self):
        print('All good')
