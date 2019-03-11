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

class ViewUnderConstruction(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._view = [
            {
                'id': 'animation_under_construction',
                'element': UIAnimation(
                    resources = {},
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='animation_under_construction', event=event, next=next, payload=payload)),
                    position = [0, 0],
                    size = [(self._resources['display']['width'] - 1), (self._resources['display']['height'] - 1)],
                    frame_files = ['assets/greatwave.bmp']
                )
            },
            {
                'id': 'label_title',
                'element': UILabel(
                    resources = { 'font': self._resources['fonts']['kosugi'] },
                    position = [53, 0],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['kosugi']['size']],
                    label = '工事中'
                )
            }
        ]

        self._rounds = 0

    def callback(self, screen, event = None):
        return True

    def event(self, element_id, event, next, payload={}):
        print('UnderConstruction event')
        print(event)
        if event == 'clicked':
            return self._event_handler(element_id=element_id, event='navigate', next=None, payload={ 'to': 'wifi' })
        return True
