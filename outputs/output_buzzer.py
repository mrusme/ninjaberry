#!/usr/bin/env python3
# coding=utf8

import smbus
import time

class OutputBuzzer:
    def __init__(self, address=0x20, bus=smbus.SMBus(1)):
        self._event_handler = None
        self._address = address
        self._bus = bus

    def _beep_on(self):
        self._bus.write_byte(self._address,0x7F&self._bus.read_byte(self._address))
    def _beep_off(self):
        self._bus.write_byte(self._address,0x80|self._bus.read_byte(self._address))

    def short(self):
        self._beep_on()
        time.sleep(0.01)
        self._beep_off()

    def destroy(self):
        print('All good')
