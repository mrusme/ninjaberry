#!/usr/bin/env python3
# coding=utf8

from ui_element import UIElement
import math

class UIButton(UIElement):
    def __init__(self, resources = {}, event_handler = None, position = [0, 0], size = [0, 0], label = ''):
        super().__init__(event_handlers = [self.event, event_handler], can_focus = False, can_highlight = True)
        self._resources = resources
        self._position = position
        self._size = size
        self._label = label

    def event(self, event, next):
        print('BUTTON EVENT')
        print(event)

        if event == 'click':
            self.propagate('clicked')

        return True

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def render(self, draw):
        iterator = 0

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

        return draw
