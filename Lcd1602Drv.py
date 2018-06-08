#!/usr/bin/python

import time
import smbus

BUS = smbus.SMBus(1)
LCD_ADDR = 0x27
bl = 0x08 #0x08 enable backlight, 0x00 disable.
#LCD_ADDR = 0x3F sudo i2cdetect -y -a 0

def send_command(comm):
    # Send bit7-4 firstly
    buf = comm & 0xF0
    buf |= bl 
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    BUS.write_byte(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    BUS.write_byte(LCD_ADDR ,buf)
        
    # Send bit3-0 secondly
    buf = (comm & 0x0F) << 4
    buf |= bl
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    BUS.write_byte(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    BUS.write_byte(LCD_ADDR ,buf)

def send_data(data):
    # Send bit7-4 firstly
    buf = data & 0xF0
    buf |= bl
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    BUS.write_byte(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    BUS.write_byte(LCD_ADDR ,buf)
        
    # Send bit3-0 secondly
    buf = (data & 0x0F) << 4
    buf |= bl
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    BUS.write_byte(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    BUS.write_byte(LCD_ADDR ,buf)

def init_lcd():
    try:
        send_command(0x33) # Must initialize to 8-line mode at first
        time.sleep(0.005)
        send_command(0x32) # Then initialize to 4-line mode
        time.sleep(0.005)
        send_command(0x28) # 2 Lines & 5*7 dots
        time.sleep(0.005)
        send_command(0x0C) # Enable display without cursor
        time.sleep(0.005)
        send_command(0x01) # Clear Screen
    except:
        return False
    else:
        return True

def clear_lcd():
        send_command(0x01) # Clear Screen

def lcd_black(en):
    global bl
    if en == 0:
        bl = 0x00
    elif en == 1:
        bl = 0x08

def print_lcd(x, y, str):
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
    send_command(addr)
    
    for chr in str:
        send_data(ord(chr))

if __name__ == '__main__':
    init_lcd()
    
    print_lcd(0, 0, 'Hello, world!')
    print_lcd(0, 1, 'ucat.taobao.com')
