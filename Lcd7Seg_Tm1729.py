#!/usr/bin/env python3
# -*- coding: utf-8-*-
# author: Tiger
# I2C interface& pin connection
# VCC---(1)(2)
# SDA---(3)(4)
# SCL---(5)(6)
# NC ---(7)(8)
# GND---(9)(10)

import time
import smbus

SMBUS_PORT = 1
LCD_ADDR = 0x3E

ICSET = 0xEA
BLKCTL = 0xF0
DISCTL = 0xA2
MODESET = 0xC8
APCTL8 = 0xFE
APCTL = 0xFC
ADSET = 0X00

Table=[0x5f,0x06,0x3d,0x2f,0x66,0x6b,0x7b,0x0e,0x7f,0x6f]

class LCD:

    def __init__(self,addr,port):
        self.addr = addr
        self.bus = smbus.SMBus(port)
        self.ICSET = 0xEA

    def init(self):
        buf = [ICSET,DISCTL,BLKCTL,APCTL,MODESET]
        for i in range(5):
            self.bus.write_byte(self.addr, buf[i])

    def clear(self):
        buf = [0x00,0x00,0x00]
        for i in range(3):
            self.bus.write_byte_data(self.addr, i*2, buf[i])  

    def display_num(self,num):
        if num >= 200 and num <0:
            return 0
        hunN = int(num/100)
        tenN = int(num/10)-hunN*10
        unitN = int(num%10)
        buf = [Table[tenN],Table[unitN]]
        if hunN>0:
            buf[0] = buf[0]+0x80
        for i in range(2):
            self.bus.write_byte_data(LCD_ADDR ,i*2,buf[i])


if __name__ == '__main__':

    lcd = LCD(LCD_ADDR,SMBUS_PORT)
    lcd.init()
    time.sleep(0.01)
    lcd.clear()
    time.sleep(0.01)
    lcd.display_num(126) 