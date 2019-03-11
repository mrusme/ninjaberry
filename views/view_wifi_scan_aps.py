#!/usr/bin/env python3
# coding=utf8

import time
import threading

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from views.view import View

from ui.ui_animation import UIAnimation
from ui.ui_button import UIButton
from ui.ui_label import UILabel
from ui.ui_line import UILine
from ui.ui_list import UIList

from partials.partial_menu import PartialMenu

from bettercap import Bettercap
from helpers.system import getAvailableIfaces

class ViewWifiScanAps(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'list_aps',
                'element': UIList(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    event_handler = (lambda event, next, payload={}: self._event_handler(element_id='list_aps', event=event, next=next, payload=payload)),
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), (self._resources['display']['height'] - 16 - 1)],
                    entries = [],
                    selected = 0
                )
            }
        ]

        self._bettercap = None
        self._thread_scan_aps = None
        self._scanned_aps = []

    def callback(self, screen, event = None):
        if len(self._scanned_aps) > 0 and len(self._view[1]['element'].entries) != len(self._scanned_aps):
            print('Setting aps')
            ap_list = []
            for scanned_ap in self._scanned_aps:
                ap_list.append({
                    'id': scanned_ap['bssid'],
                    'label': scanned_ap['clients'] + ' | ' + scanned_ap['ssid'],
                    'args': scanned_ap
                })
            self._view[1]['element'].entries = ap_list
        return True

    def event(self, element_id, event, next, payload={}):
        print('WifiScanAps Event:')
        print(event)
        print(payload)
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)
        if event == 'display':
            self._bettercap = payload['args']['bettercap']
            # TODO: Handle errors with bettercap
            self._thread_scan_aps = threading.Thread(target=self.thread_bettercap_scan_aps, args=())
            self._thread_scan_aps.daemon = True
            self._thread_scan_aps.start()
        elif event == 'picked':
            ssid = payload['id']
            ap = payload['args']
            return self._event_handler(element_id=element_id, event='navigate', next=None, payload={ 'to': 'wifi_ap_actions', 'args': { 'bettercap': self._bettercap, 'ap': ap } })
        elif event == 'conceal':
            if 'to' in payload:
                if payload['to'] != 'wifi_ap_actions':
                    print('Destroying WifiScanAps ..')
                    self._thread_scan_aps.join()
                    self._scanned_aps = []
                    print('Destroyed')
        return True

    def thread_bettercap_scan_aps(self):
        if self._bettercap != None:
            self._scanned_aps = self._bettercap.scan_aps()
        return self._scanned_aps
