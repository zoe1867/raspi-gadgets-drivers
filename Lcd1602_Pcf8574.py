#!/usr/bin/env python3
# -*- coding: utf-8-*-
# author: Tiger
# (YwRobot) I2C interface & pin connection
# NC ---(1)(2)---VCC
# SDA---(3)(4)
# SCL---(5)(6)
# NC ---(7)(8)
# GND---(9)(10)

import time
import smbus

SMBUS_PORT = 1
LCD_ADDR = 0x27

class LCD:

    def __init__(self, addr, port):
        self.addr = addr
        self.bus = smbus.SMBus(port)
        self.bl = 0x08

    def send_command(self, comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= self.bl 
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.bus.write_byte(self.addr ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.bus.write_byte(self.addr ,buf)
            
        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= self.bl
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        self.bus.write_byte(self.addr ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.bus.write_byte(self.addr ,buf)

    def send_data(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= self.bl
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.bus.write_byte(self.addr, buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.bus.write_byte(self.addr, buf)
            
        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= self.bl
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        self.bus.write_byte(self.addr ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        self.bus.write_byte(self.addr ,buf)

    def init(self):
        try:
            self.send_command(0x33) # Must initialize to 8-line mode at first
            time.sleep(0.005)
            self.send_command(0x32) # Then initialize to 4-line mode
            time.sleep(0.005)
            self.send_command(0x28) # 2 Lines & 5*7 dots
            time.sleep(0.005)
            self.send_command(0x0C) # Enable display without cursor
            time.sleep(0.005)
            self.send_command(0x01) # Clear Screen
        except:
            return False
        else:
            return True

    def clear(self):
        self.send_command(0x01) # Clear Screen

    def black_ctrl(self, en):
        if en == 0:
            self.bl = 0x00
        elif en == 1:
            self.bl = 0x08

    def display_string(self, x, y, str):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y <0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)
        
        for chr in str:
            self.send_data(ord(chr))

if __name__ == '__main__':

    lcd=LCD(LCD_ADDR, SMBUS_PORT)
    lcd.init()
    
    lcd.display_string(0, 0, 'Hello, world!')
    lcd.display_string(0, 1, '&raspberry pi')
