#!/usr/bin/env python3
# coding=utf8

from subprocess import Popen, PIPE, STDOUT
import re
import time

class Bettercap:
    def __init__(self, iface='wlan0'):
        self._bettercap = None
        self._iface = iface

    def start(self):
        if self._bettercap == None:
            self._bettercap = Popen(['bettercap', '-iface', self._iface, '-no-colors', '-no-history'], shell=False, cwd='/tmp', encoding='utf-8', bufsize=-1, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        else:
            print('Bettercap was running already')

        return True

    def stop(self):
        print('Writing quit ...')
        self._bettercap.stdin.write('quit\n');
        print('Flushing ...')
        self._bettercap.stdin.flush()
        print('Closing ...')
        self._bettercap.stdin.close()
        print('Waiting ...')
        self._bettercap.wait()
        print('Resetting ...')
        self._bettercap = None
        return True

    def _read(self):
        keep_reading = True
        stdout = ""

        while keep_reading:
            stdout_line = self._bettercap.stdout.readline()
            if stdout_line == '%NINJAEND%\n':
                keep_reading = False
            else:
                stdout = stdout + stdout_line

        return stdout


    def scan_aps(self):
        regex = r'^\u2502\s([\+\-][0-9]{1,4})\sdBm\s\u2502\s([a-f0-9\:]{17})\s\u2502\s([^│;]+)\s\u2502\s([^│;]*)\s+\u2502\s(2\.0|1\.0|)(\s*\([a-zA-Z ]+\))?\s+\u2502\s([0-9]{1,3})\s+\u2502\s([0-9]{0,10})\s+\u2502\s([^│;]*)\s+\u2502\s([^│;]*)\s+\u2502\s([^│;]*)\s+\u2502'
        index_dbm = 1
        index_bssid = 2
        index_ssid = 3
        index_encryption = 4
        index_wps = 5
        index_wps_info = 6
        index_channel = 7
        index_clients = 8
        index_data_sent = 9
        index_data_received = 10
        index_seen = 11

        print('Writing command ...')
        # TODO: Change ticker.period & time.sleep
        self._bettercap.stdin.write('set wifi.show.sort clients desc; set ticker.period 5; set ticker.commands "clear; wifi.show; !echo \'%NINJAEND%\'; exit;"; wifi.recon on; ticker on;\n')
        print('Flushing ...')
        self._bettercap.stdin.flush()
        print('Sleeping ...')
        time.sleep(5)
        print('Reading ...')
        stdout = self._read(bc)

        aps = []
        matches = re.finditer(regex, stdout, re.UNICODE | re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            ap = {
                'bssid': match.group(index_bssid),
                'ssid': match.group(index_ssid),
                'encryption': match.group(index_encryption),
                'wps': match.group(index_wps),
                'wps_info': match.group(index_wps_info),
                'channel': match.group(index_channel),
                'dbm': match.group(index_dbm),
                'clients': match.group(index_clients),
                'seen': match.group(index_seen),
                'clients': match.group(index_clients),
                'data': {
                    'sent': match.group(index_data_sent),
                    'received': match.group(index_data_received)
                }
            }
            aps.append(ap)

        return aps
