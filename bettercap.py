#!/usr/bin/env python3
# coding=utf8

from subprocess import Popen, PIPE, STDOUT
import re
import time
from datetime import datetime
import math

class Bettercap:
    END_OF_OUTPUT = '%NINJAEND%'
    CAPTURE_LOCATION = '/mnt/capture'

    def __init__(self, iface='wlan0'):
        self._bettercap = None
        self._iface = iface
        self._iface_active = None

    @property
    def iface(self):
        return self._iface

    @iface.setter
    def iface(self, value):
        self._iface = value

    def start(self):
        if self._bettercap == None:
            self._bettercap = Popen(['bettercap', '-iface', self._iface, '-no-colors', '-no-history'], shell=False, cwd='/tmp', encoding='utf-8', bufsize=-1, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            self._iface_active = self._iface
        else:
            print('Bettercap is running already, checking for iface change ...')
            if self._iface != self._iface_active:
                print('Interface changed! Restarting ...')
                self.restart()
            else:
                print('Bettercap interface did not change, not doing anything.')
        return True

    def stop(self):
        if self._bettercap != None:
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

    def restart(self):
        if self._bettercap != None:
            ret_val = self.stop()
            if ret_val != True:
                return False
            time.sleep(1)
        return self.start()

    def _read(self, stop_on='', retrieve_stdout=True):
        print('Reading ...')
        keep_reading = True
        stdout = ""
        regextype = type(re.compile(''))

        while keep_reading:
            stdout_line = self._bettercap.stdout.readline()
            if type(stop_on) is str:
                if stdout_line == stop_on:
                    keep_reading = False
            elif type(stop_on) is regextype:
                if stop_on.match(stdout_line) != None:
                    keep_reading = False
            if retrieve_stdout == True:
                stdout = stdout + stdout_line

        if retrieve_stdout == True:
            return stdout
        else:
            return None

    def _execute(self, command):
        print('Writing command:' + command)
        self._bettercap.stdin.write(command)
        self._bettercap.stdin.flush()
        print('Command executed!')
        return True

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

        # TODO: Change ticker.period & time.sleep
        self._execute('set wifi.show.sort clients desc; set ticker.period 5; set ticker.commands "clear; wifi.show; !echo \'' + self.END_OF_OUTPUT + '\'; wifi.recon off; ticker off;"; wifi.recon on; ticker on;\n')
        print('Sleeping ...')
        time.sleep(5)
        stdout = self._read(stop_on=(self.END_OF_OUTPUT + '\n'), retrieve_stdout=True)

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

    def capture_and_deauth(self, bssid, channel):
        try:
            os.makedirs(self.CAPTURE_LOCATION)
        except FileExistsError:
            pass

        capture_file = self.CAPTURE_LOCATION + '/' + math.floor(datetime.now().timestamp()) + '.pcap'

        self._execute('set net.sniff.verbose true; set net.sniff.filter ether proto 0x888e; set net.sniff.output ' + capture_file + '; net.sniff on; wifi.recon.channel ' + channel + '; wifi.recon on; wifi.recon ' + bssid + '; wifi.deauth ' + bssid + ';\n')
        self._read(stop_on=re.compile(r'.* captured .* handshake .*'), retrieve_stdout=False)

        return capture_file

    def all_off(self):
        self._execute('net.sniff off; wifi.recon off; ticker off;\m')
        return true;
