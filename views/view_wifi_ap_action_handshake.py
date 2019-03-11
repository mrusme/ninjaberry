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

from helpers.system import getAvailableIfaces

class ViewWifiApActionHandshake(View):
    def __init__(self, resources, event_handler):
        self._resources = resources
        self._event_handler = event_handler
        self._partial_menu = PartialMenu(resources=self._resources, event_handler=self._event_handler)
        self._view = [
            self._partial_menu.partial,
            {
                'id': 'label_ap',
                'element': UILabel(
                    resources = { 'font': self._resources['fonts']['hack'] },
                    position = [0, 16],
                    size = [(self._resources['display']['width'] - 1), self._resources['fonts']['hack']['size']],
                    label = ''
                )
            }
        ]

        self._bettercap = None
        self._thread_ap_handshake = None
        self._ap = {}
        self._capture_file = None

    def callback(self, screen, event = None):
        if self._capture_file == None:
            self._view[1]['element'].label = 'Scanning ...'
        else:
            self._view[1]['element'].label = 'Done! Capture stored to:\n' + self._capture_file
        return True

    def event(self, element_id, event, next, payload={}):
        print('WifiScanApActionHandshake Event:')
        print(event)
        print(payload)
        self._partial_menu.event(element_id=element_id, event=event, next=next, payload=payload)
        if event == 'display':
            self._bettercap = payload['args']['bettercap']
            # TODO: Handle errors with bettercap
            self._ap = payload['args']['ap']

            self._thread_ap_handshake = threading.Thread(target=self._thread_bettercap_capture_and_deauth, args=())
            self._thread_ap_handshake.daemon = True
            self._thread_ap_handshake.start()
        elif event == 'conceal':
            print('Stopping thread ..')
            self._bettercap.stop() # We stop Bettercap so that the thread can't continue reading and returns.
            self._thread_ap_handshake.join()
            print('Stopped')
            self._ap = {}
        return True

    def _thread_bettercap_capture_and_deauth(self):
        if self._bettercap != None:
            capture_file = self._bettercap.capture_and_deauth(bssid=self._ap['bssid'], channel=self._ap['channel'])
            self._capture_file = capture_file
            return self._capture_file
        return None
