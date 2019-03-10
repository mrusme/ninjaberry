#!/usr/bin/env python3
# coding=utf8

import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from partials.partial import Partial

from ui.ui_animation import UIAnimation
from ui.ui_button import UIButton
from ui.ui_label import UILabel
from ui.ui_line import UILine
from ui.ui_list import UIList

class PartialMenu(Partial):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial = {
            'id': 'menu',
            'horizontal': [
                {
                    'id': 'button_wifi',
                    'element': UIButton(
                        resources = { 'font': self._resources['fonts']['fa_solid'] },
                        event_handler = (lambda ev, nxt: self._event_handler('button_wifi', ev, nxt)),
                        position = [0, 0],
                        size = [15, 14],
                        label = chr(0xf1eb)
                    )
                },
                {
                    'id': 'button_bt',
                    'element': UIButton(
                        resources = { 'font': self._resources['fonts']['fa_brands'] },
                        event_handler = (lambda ev, nxt: self._event_handler('button_bt', ev, nxt)),
                        position = [16, 0],
                        size = [15, 14],
                        label = chr(0xf294)
                    )
                },
                {
                    'id': 'button_eth',
                    'element': UIButton(
                        resources = { 'font': self._resources['fonts']['fa_solid'] },
                        event_handler = (lambda ev, nxt: self._event_handler('button_eth', ev, nxt)),
                        position = [32, 0],
                        size = [15, 14],
                        label = chr(0xf796)
                    )
                },
                {
                    'id': 'button_settings',
                    'element': UIButton(
                        resources = { 'font': self._resources['fonts']['fa_solid'] },
                        event_handler = (lambda ev, nxt: self._event_handler('button_settings', ev, nxt)),
                        position = [48, 0],
                        size = [15, 14],
                        label = chr(0xf013)
                    )
                },
                {
                    'id': 'line_menu',
                    'element': UILine(
                        resources = {},
                        position = [0, 15, self._resources['display']['width'], 15],
                        size = 1,
                        fill = 255
                    )
                }
            ]
        }
