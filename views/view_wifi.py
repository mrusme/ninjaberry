#!/usr/bin/env python3
# coding=utf8

import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from views.view import View

from ui.ui_animation import UIAnimation
from ui.ui_button import UIButton
from ui.ui_label import UILabel
from ui.ui_line import UILine
from ui.ui_list import UIList

from partials.partial_menu import PartialMenu

from bettercap import Bettercap
from helpers.system import getAvailableIfaces

class ViewWifi(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'label_iface',
                'element': UILabel(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = 'Select network interface:'
                )
            },
            {
                'id': 'list_ifaces',
                'element': UIList(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='list_ifaces', event=event, next=next, payload=payload)),
                    position = [0, 28],
                    size = [(self._resources['display']['width'] - 1), 10],
                    entries = getAvailableIfaces(),
                    selected = 0
                )
            },
            {
                'id': 'label_timeout',
                'element': UILabel(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    position = [0, 38],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = 'Number of sec. to scan:'
                )
            },
            {
                'id': 'list_timeout',
                'element': UIList(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='list_timeout', event=event, next=next, payload=payload)),
                    position = [0, 46],
                    size = [(self._resources['display']['width'] - 1), 10],
                    entries = ['5', '10', '30', '60', '120', '240'],
                    selected = 0
                )
            },
            {
                'id': 'button_scan_aps',
                'element': UIButton(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='button_scan_aps', event=event, next=next, payload=payload)),
                    position = [0, 56],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = 'Scan for APs'
                )
            }
        ]

        self._bettercap = self._resources['external']['bettercap']

    def callback(self, screen, event = None):
        return True

    def event(self, element_id, event, next, payload={}):
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)

        if element_id == 'button_scan_aps' and event == 'clicked':
            selected_iface = self._view[2]['element'].selected_id
            self._bettercap.iface = selected_iface
            self._bettercap.start()

            selected_timeout = self._view[4]['element'].selected_id

            return self._event_handler(element_id=element_id, event='navigate', next=None, payload={ 'to': 'wifi_scan_aps', 'args': { 'iface': selected_iface, 'timeout': selected_timeout, 'bettercap': self._bettercap } })
        elif event == 'conceal':
            if 'to' in payload and payload['to'] != 'wifi_scan_aps':
                self._bettercap.stop()
        elif event == 'destroy':
            self._bettercap.stop()

        return True
