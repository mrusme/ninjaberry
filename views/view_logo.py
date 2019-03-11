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

class ViewLogo(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._view = [
            {
                'id': 'animation_logo',
                'element': UIAnimation(
                    resources = {},
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='animation_logo', event=event, next=next, payload=payload)),
                    position = [0, 0],
                    size = [(self._resources['display']['width'] - 1), (self._resources['display']['height'] - 1)],
                    frame_files = ['assets/bettercap01.bmp', 'assets/bettercap02.bmp', 'assets/bettercap03.bmp', 'assets/bettercap04.bmp']
                )
            },
            {
                'id': 'label_title',
                'element': UILabel(
                    resources = { 'font': self._resources['fonts']['kosugi'] },
                    position = [31, 0],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['kosugi']['size']],
                    label = 'ベッターキャップ'
                )
            }
        ]

        self._rounds = 0

    def callback(self, screen, event = None):
        if self._rounds >= 12:
            print('Calling wifi view')
            self._event_handler(element_id='view_logo', event='navigate', next=None, payload={ 'to': 'wifi' })
            return False
        self._view[0]['element'].frame_next()
        self._rounds = self._rounds + 1
        return True

    def event(self, element_id, event, next, payload={}):
        return True
