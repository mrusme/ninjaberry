#!/usr/bin/env python3
# coding=utf8

import time
import threading

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

class ViewWifiApActions(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'button_handshake',
                'element': UIButton(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='button_handshake', event=event, next=next, payload=payload)),
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = 'Capture handshake'
                )
            }
        ]

        self._bettercap = None
        self._ap = None

    def callback(self, screen, event = None):
        return True

    def event(self, element_id, event, next, payload={}):
        print('WifiApActions Event:')
        print(event)
        print(payload)
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)
        if event == 'display':
            self._bettercap = payload['args']['bettercap']
            self._ap = payload['args']['ap']
        elif event == 'clicked':
            if element_id == 'button_handshake':
                return self._event_handler(element_id=element_id, event='navigate', next=None, payload={ 'to': 'wifi_ap_action_handshake', 'args': { 'bettercap': self._bettercap, 'ap': self._ap } })
        elif event == 'conceal':
            self._ap = None
        return True
