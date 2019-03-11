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

from helpers.system import getAvailableIfaces

class ViewWifi(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'label_ssid',
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
                    event_handler = (lambda ev, nxt: self._event_handler('list_ifaces', ev, nxt)),
                    position = [0, 30],
                    size = [(self._resources['display']['width'] - 1), 10],
                    entries = getAvailableIfaces(),
                    selected = 0
                )
            },
            {
                'id': 'button_scan_aps',
                'element': UIButton(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda ev, nxt: self._event_handler('button_scan_aps', ev, nxt)),
                    position = [0, (self._resources['display']['height'] - self._resources['fonts']['hack']['size'] - 1)],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = 'Scan for APs'
                )
            }
        ]

    def callback(self, screen, event = None):
        return True

    def event(self, element_id, event, next, payload={}):
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)

        if element_id == 'button_scan_aps' and event == 'clicked':
            return self._event_handler(element_id=element_id, event='navigate', next=None, payload={ 'to': 'wifi_scan_aps', 'args': { 'iface': self._view[2]['element'].selected_id } })
