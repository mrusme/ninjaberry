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

class ViewWifiScanAps(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'list_aps',
                'element': UIList(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda ev, nxt: self._event_handler('list_aps', ev, nxt)),
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), (self._resources['display']['height'] - 16 - 1)],
                    entries = [],
                    selected = 0
                )
            }
        ]

    def callback(self, screen, event = None):
        draw = ImageDraw.Draw(screen)

    def event(self, element_id, event, next, payload={}):
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)
