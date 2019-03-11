#!/usr/bin/env python3
# coding=utf8

from ui.ui_element import UIElement
from PIL import ImageDraw
import math

class UILine(UIElement):
    # draw.line([0, 15, 128, 15], fill=255, width=1, joint=None)
    def __init__(self, resources = {}, position = [0, 0, 0, 0], size = 1, fill = 255):
        super().__init__(event_handlers = [self.event], can_focus = False, can_highlight = False)
        self._resources = resources
        self._position = position
        self._size = size
        self._fill = fill

    def event(self, event, next, payload={}):
        print('LINE EVENT')
        print(event)

        return True

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        self._fill = value

    def render(self, screen):
        draw = ImageDraw.Draw(screen)
        draw.line(self._position, fill=self._fill, width=self._size, joint=None)

        return screen
