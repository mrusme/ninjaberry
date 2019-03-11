#!/usr/bin/env python3
# coding=utf8

from ui.ui_element import UIElement
from PIL import ImageDraw
import math

class UILabel(UIElement):
    def __init__(self, resources = {}, position = [0, 0], size = [0, 0], label = ''):
        super().__init__(event_handlers = [self.event], can_focus = False, can_highlight = False)
        self._resources = resources
        self._position = position
        self._size = size
        self._label = label

    def event(self, event, next, payload={}):
        print('LABEL EVENT')
        print(event)

        return True

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def render(self, screen):
        draw = ImageDraw.Draw(screen)

        label_x = self._position[0]
        label_y = self._position[1]
        label_w = self._size[0]
        label_h = self._size[1]
        label_w_abs = label_x + label_w
        label_h_abs = label_y + label_h

        draw.multiline_text((label_x, label_y), self._label, font=self._resources['font']['ttf'], fill=255)

        return screen
