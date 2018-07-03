#!/usr/bin/env python3
# -*- coding: utf-8-*-
# author: Tiger

import DH11
import Lcd1602_Pcf8574
import RPi.GPIO as GPIO  
  
if __name__ == "__main__":

    try:    
        dh11 = DH11.DH11()
        dh11.init()
        dh11.get_temp()

        lcd=Lcd1602_Pcf8574.LCD(0x27, 1)
        lcd.init()
        str1 = "Temperature: " + str(dh11.temperature)
        str2 = "humidity:    " + str(dh11.humidity)
        print(str1)
        print(str2)  
        lcd.display_string(0, 0, str1)
        lcd.display_string(0, 1, str2)
    finally:
        dh11.close()

