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
                    event_handler = (lambda ev, nxt: self._event_handler('list_aps', ev, nxt)),
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), (self._resources['display']['height'] - 16 - 1)],
                    entries = [],
                    selected = 0
                )
            }
        ]

        self._bettercap = Bettercap()
        self._thread_scan_aps = None
        self._scanned_aps = []

    def callback(self, screen, event = None):
        if len(self._scanned_aps) > 0 and len(self._view[1]['element'].entries) != len(self._scanned_aps):
            print('Setting aps')
            ap_list = []
            for scanned_ap in self._scanned_aps:
                ap_list.append({
                    'id': scanned_ap['bssid'],
                    'label': scanned_ap['ssid']
                })
            self._view[1]['element'].entries = ap_list
        return True

    def event(self, element_id, event, next, payload={}):
        print('WifiScanAps Event:')
        print(event)
        print(payload)
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)
        if event == 'display':
            self._bettercap.iface = payload['args']['iface']
            self._bettercap.start()
            self._thread_scan_aps = threading.Thread(target=self.thread_bettercap_scan_aps, args=())
            self._thread_scan_aps.daemon = True
            self._thread_scan_aps.start()
        elif event == 'destroy':
            print('Destroying WifiScanAps ..')
            self._thread_scan_aps.join()
            self._bettercap.stop()
            self._scanned_aps = []
            print('Destroyed')

    def thread_bettercap_scan_aps(self):
        self._scanned_aps = self._bettercap.scan_aps()
        return self._scanned_aps
