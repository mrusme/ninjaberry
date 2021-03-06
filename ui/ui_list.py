#!/usr/bin/env python3
# coding=utf8

from ui.ui_element import UIElement
from PIL import ImageDraw
import math

class UIList(UIElement):
    def __init__(self, resources = {}, event_handler = None, position = [0, 0], size = [0, 0], entries = [], selected = None):
        super().__init__(event_handlers = [self.event, event_handler], can_focus = True, can_highlight = True)
        self._resources = resources
        self._position = position
        self._size = size
        self._entries = entries
        self._selected = selected

    def event(self, event, next, payload={}):
        print('LIST EVENT')
        print(event)

        if event == 'down':
            self.select_next()
        elif event == 'up':
            self.select_previous()
        elif event == 'click':
            self.propagate(event='picked', payload={ 'id': self.selected_id, 'args': self.selected_args })
            self.blur()

        return True

    @property
    def entries(self):
        return self._entries

    @entries.setter
    def entries(self, value):
        self._entries = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def selected_id(self):
        (entry_id, entry_label) = self._getIdAndLabelFromEntry(self._entries[self._selected])
        return entry_id

    @property
    def selected_label(self):
        (entry_id, entry_label) = self._getIdAndLabelFromEntry(self._entries[self._selected])
        return entry_label

    @property
    def selected_args(self):
        return self._getArgsFromEntry(self._entries[self._selected])

    def select_previous(self):
        self._selected = self._selected - 1

        if self._selected < 0:
            self._selected = (len(self._entries) - 1)

        return self._selected

    def select_next(self):
        self._selected = self._selected + 1

        if self._selected >= len(self._entries):
            self._selected = 0

        return self._selected

    def _getIdAndLabelFromEntry(self, entry):
        # An entry could either be a simple string or a dict with props:
        # { 'id': 123, 'label': 'Test Entry' }
        entry_id = None
        entry_label = None
        if type(entry) is str:
            entry_id = entry
            entry_label = entry
        elif type(entry) is dict and 'label' in entry and 'id' in entry:
            entry_id = entry['id']
            entry_label = entry['label']
        else:
            entry_id = '(DEVELOPER FUCKED UP)'
            entry_label = '(DEVELOPER FUCKED UP)'
        return (entry_id, entry_label)

    def _getArgsFromEntry(self, entry):
        entry_args = None
        if type(entry) is dict and 'args' in entry:
            entry_args = entry['args']
        return entry_args

    def render(self, screen):
        draw = ImageDraw.Draw(screen)
        iterator = 0

        list_x = self._position[0]
        list_y = self._position[1]
        list_w = self._size[0]
        list_h = self._size[1]
        list_w_abs = list_x + list_w
        list_h_abs = list_y + list_h

        list_entry_h = (self._resources['font']['size'] + 2)
        max_visible_list_entries = math.floor(list_h / list_entry_h)

        oms = []
        index_of_selected = self._selected

        for entry in self._entries:
            om = {}

            selected = True if iterator == self._selected else False
            selector = '» ' if selected else '  '

            # An entry could either be a simple string or a dict with props:
            # { 'id': 123, 'label': 'Test Entry' }
            (entry_id, entry_label) = self._getIdAndLabelFromEntry(entry)
            entry_string = selector + entry_label
            entry_string_size = self._resources['font']['ttf'].getsize(entry_string)

            entry_args = self._getArgsFromEntry(entry)

            w = entry_string_size[0]
            h = entry_string_size[1]

            om = {
                'index': iterator,
                'selected': selected,
                'id': entry_id,
                'label': entry_string,
                'args': entry_args,
                'w': w,
                'h': h
            }

            oms.append(om)
            iterator = iterator + 1

        available_list_entries = len(oms)
        visible_before_index = 0
        visible_after_index = available_list_entries

        if max_visible_list_entries < available_list_entries:
            visible_rest = max_visible_list_entries - 1 # the selected one

            before_part = math.floor((visible_rest / 2))
            after_part = visible_rest - before_part

            visible_before_index = index_of_selected - before_part

            visible_before_rest = 0
            if visible_before_index < 0:
                visible_before_rest = 0 - visible_before_index
            visible_after_index = index_of_selected + after_part + visible_before_rest + 1

            visible_after_rest = 0
            if visible_after_index > available_list_entries:
                visible_after_rest = (available_list_entries) - visible_after_index
                visible_after_index = visible_after_index + visible_after_rest

            visible_before_index = (visible_before_index + visible_after_rest)
            if visible_before_index < 0:
                visible_before_index = 0

        visible_iterator = 0
        for visible_entry_index in range(visible_before_index, visible_after_index):
            visible_entry = oms[visible_entry_index]
            x = self._position[0]
            y = self._position[1] + visible_iterator * list_entry_h

            draw.text((x, y), visible_entry['label'], font=self._resources['font']['ttf'], fill=255)
            visible_iterator = visible_iterator + 1

        if self._has_highlight is True:
            draw.rectangle([list_x, list_y, list_w_abs, list_h_abs], outline=255, width=1)

        return screen
