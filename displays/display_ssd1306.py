#!/usr/bin/env python3
# coding=utf8

import spidev
import RPi.GPIO as GPIO
import spidev as SPI
import time

# Constants
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A

# This code was "borrowed" from the
# http://waveshare.com/wiki/File:Pioneer600-Code.tar.gz package and modify to
# fit a more generic implementation

class DisplaySSD1306:
    """class for SSD1306  128*64 0.96inch OLED displays."""

    def __init__(self, rst=19, dc=16, spi=SPI.SpiDev(0, 0)):
        self.width = 128
        self.height = 64
        self._pages = 8
        self._buffer = [0]*(self.width*self._pages)
        #Initialize DC RST pin
        self._dc = dc
        self._rst = rst
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._dc,GPIO.OUT)
        GPIO.setup(self._rst,GPIO.OUT)
        #Initialize SPI
        self._spi = spi
    def command(self,cmd):
        """Send command byte to display"""
        GPIO.output(self._dc,GPIO.LOW)
        self._spi.writebytes([cmd])
    def data(self,val):
        """Send byte of data to display"""
        GPIO.output(self._dc,GPIO.HIGHT)
        self._spi.writebytes([val])
    def begin(self,vccstate=SSD1306_SWITCHCAPVCC):
        """Initialize dispaly"""
        self._vccstate = vccstate
        self.reset()
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        self.command(0x80)                     # the suggested ra    tio 0x80

        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x3F)
        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        self.command(0x00)                            # 0x0 act like ks0108
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x12)
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x9F)
        else:
            self.command(0xCF)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6
        self.command(SSD1306_DISPLAYON)
    def reset(self):
        """Reset the display"""
        GPIO.output(self._rst,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self._rst,GPIO.LOW)
        time.sleep(0.010)
        GPIO.output(self._rst,GPIO.HIGH)
    def display(self):
        """Write display buffer to physical display"""
        self.command(SSD1306_COLUMNADDR)
        self.command(0)                  #Cloumn start address
        self.command(self.width-1)     #Cloumn end address
        self.command(SSD1306_PAGEADDR)
        self.command(0)                  #Page start address
        self.command(self._pages-1)      #Page end address
        #Write buffer data
        GPIO.output(self._dc,GPIO.HIGH)
        self._spi.writebytes(self._buffer)
    def image(self, image):
        """Set buffer to value of Python Imaging Library image."""
        if image.mode != '1':
            raise ValueError('Image must be in mode 1.')
        imwidth, imheight = image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        pix = image.load()
        # Iterate through the memory pages
        index = 0
        for page in range(self._pages):
            # Iterate through all x axis columns.
            for x in range(self.width):
            # Set the bits for the column of pixels at the current position.
                bits = 0
                # Don't use range here as it's a bit slow
                for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                    bits = bits << 1
                    bits |= 0 if pix[(x, page*8+7-bit)] == 0 else 1
                # Update buffer byte and increment to next byte.
                self._buffer[index] = bits
                index += 1
    def clear(self):
        """Clear contents of image buffer"""
        self._buffer = [0]*(self.width*self._pages)
    def set_contrast(self, contrast):
        """Sets the contrast of the display.
        Contrast should be a value between 0 and 255."""
        if contrast < 0 or contrast > 255:
            raise ValueError('Contrast must be a value from 0 to 255).')
        self.command(SSD1306_SETCONTRAST)
        self.command(contrast)

    def dim(self, dim):
        """Adjusts contrast to dim the display if dim is True,
        otherwise sets the contrast to normal brightness if dim is False."""
        # Assume dim display.
        contrast = 0
        # Adjust contrast based on VCC if not dimming.
        if not dim:
            if self._vccstate == SSD1306_EXTERNALVCC:
                contrast = 0x9F
            else:
                contrast = 0xCF
