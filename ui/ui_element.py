#!/usr/bin/env python3
# coding=utf8

import math

class UIElement:
    def __init__(self, event_handlers = [], can_focus = False, can_highlight = False):
        self._event_handlers = event_handlers

        self._can_focus = can_focus
        self._has_focus = False

        if can_focus is True and can_highlight is False:
            raise Exception('Element cannot allow focusing without highlighting!')
        self._can_highlight = can_highlight
        self._has_highlight = False

    def propagate(self, ev):
        for event_handler_index, event_handler in enumerate(self._event_handlers):
            if event_handler != None:
                next_event_handler_index = event_handler_index + 1
                next_event_handler = None

                if next_event_handler_index < len(self._event_handlers):
                    next_event_handler = self._event_handlers[next_event_handler_index]

                continue_handling = event_handler(ev, next_event_handler)
                if continue_handling is False:
                    return False
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
    def can_focus(self):
        return self._can_focus

    @property
    def has_focus(self):
        return self._has_focus

    @property
    def can_highlight(self):
        return self._can_highlight

    @property
    def has_highlight(self):
        return self._has_highlight

    def focus(self):
        if self._can_focus is False or self._has_focus is True:
            return False

        self._has_focus = True
        return self.propagate('focused')

    def blur(self):
        if self._can_focus is False or self._has_focus is False:
            return False

        self._has_focus = False
        was_blurred = self.propagate('blurred')

        if was_blurred == False:
            self._has_focus = True
            return False

        return True

    def highlight(self):
        if self._can_highlight is False or self._has_highlight is True:
            return False

        self._has_highlight = True
        return self.propagate('highlighted')

    def lowlight(self):
        if self._can_highlight is False is True or self._has_highlight is False:
            return False

        self._has_highlight = False
        return self.propagate('lowlighted')
