#!/usr/bin/env python3
# coding=utf8

from ui.ui_element import UIElement
from PIL import Image
import math

class UIAnimation(UIElement):
    def __init__(self, resources = {}, event_handler = None, position = [0, 0], size = [0, 0], frame_files = []):
        super().__init__(event_handlers = [self.event, event_handler], can_focus = False, can_highlight = False)
        self._resources = resources
        self._position = position
        self._size = size

        self._frame_files = frame_files
        self._frames = []
        for frame_file in frame_files:
            self._frames.append(Image.open(frame_file).convert('1'))
        self._current_frame = 0

    def event(self, event, next, payload={}):
        print('ANIMATION EVENT')
        print(event)

        if event == 'click':
            self.propagate(event='clicked')

        return True

    @property
    def frame_files(self):
        return self._frame_files

    @frame_files.setter
    def frame_files(self, value):
        self._frame_files = value

    def frame_next(self):
        self._current_frame = self._current_frame + 1
        if self._current_frame >= len(self._frames):
            self._current_frame = 0

    def frame_previous(self):
        self._current_frame = self._current_frame - 1
        if self._current_frame < 0:
            self._current_frame = len(self._frames) - 1

    def render(self, screen):
        # animation_x = self._position[0]
        # animation_y = self._position[1]
        # animation_w = self._size[0]
        # animation_h = self._size[1]
        # animation_w_abs = animation_x + animation_w
        # animation_h_abs = animation_y + animation_h

        screen = self._frames[self._current_frame]

        return screen
