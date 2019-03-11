#!/usr/bin/env python3
# coding=utf8

from ui.ui_element import UIElement
from PIL import ImageDraw
import math

class UIButton(UIElement):
    def __init__(self, resources = {}, event_handler = None, position = [0, 0], size = [0, 0], label = ''):
        super().__init__(event_handlers = [self.event, event_handler], can_focus = False, can_highlight = True)
        self._resources = resources
        self._position = position
        self._size = size
        self._label = label

    def event(self, event, next, payload={}):
        print('BUTTON EVENT')
        print(event)

        if event == 'click':
            self.propagate(event='clicked')

        return True

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def render(self, screen):
        draw = ImageDraw.Draw(screen)

        button_x = self._position[0]
        button_y = self._position[1]
        button_w = self._size[0]
        button_h = self._size[1]
        button_w_abs = button_x + button_w
        button_h_abs = button_y + button_h

        label_size = self._resources['font']['ttf'].getsize(self._label)

        label_x = button_x + math.ceil((button_w - label_size[0]) / 2)
        label_y = button_y + math.floor((button_h - label_size[1]) / 2)

        if self._has_highlight is True:
            draw.rectangle([button_x, button_y, button_w_abs, button_h_abs], fill=255, outline=None, width=0)
            draw.text((label_x, label_y), self._label, font=self._resources['font']['ttf'], fill=0)
        else:
            draw.rectangle([button_x, button_y, button_w_abs, button_h_abs], fill=0, outline=None, width=0)
            draw.text((label_x, label_y), self._label, font=self._resources['font']['ttf'], fill=255)

        return screen
