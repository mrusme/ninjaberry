#!/usr/bin/env python3
# coding=utf8

import os
import time

def getAvailableIfaces():
    return os.listdir('/sys/class/net/')
