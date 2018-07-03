#!/usr/bin/env python
# coding=utf-8
# author:ksc
 
import RPi.GPIO as GPIO
import time
import os,sys
import signal
import Lcd1602_Pcf8574
 
GPIO.setmode(GPIO.BCM)
 
#define GPIO pin
pin_btn=7
pin_led=17
 
GPIO.setup(pin_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_led, GPIO.OUT, initial=GPIO.LOW)
 
press_time=0
count_down=10
 
def cleanup():
    print("clean up")
    GPIO.cleanup()
 
def handleSIGTERM(signum, frame):
    #cleanup()
    sys.exit()#raise an exception of type SystemExit
 
def onPress(channel):
    global press_time,count_down
    print("pressed")
    press_time+=1
    if press_time >3:
        press_time=1
    if press_time==1:
        GPIO.output(pin_led, 1)
        print("system will restart in %s"%(count_down))
        str1 = "restart in "+str(count_down)
        lcd.display_string(0,1,str1)
    elif press_time==2:
        print("system will halt in %s"%(count_down))
        str1 = "halt in "+str(count_down)
    elif press_time==3:
        GPIO.output(pin_led, 0)
        print("cancel")
        lcd.display_string(0,1,"cancel")
        count_down=10
 
GPIO.add_event_detect(pin_btn, GPIO.FALLING, callback= onPress,bouncetime=500)
 
try:
    lcd = Lcd1602_Pcf8574.LCD(0x27, 1)
    lcd.init()
    lcd.display_string(0,0,"Raspberry Pi~~")
    while True:
        if press_time==1:
            if count_down==0:
                print("start restart")
                lcd.display_string(0,1,"start restart")
                os.system("shutdown -r -t 5 now")
                sys.exit()
        if press_time==2 and count_down==0:
            print("start shutdown")
            lcd.display_string(0,1,"start shutdown")
            os.system("shutdown  -t 5 now")
            sys.exit()
 
        if press_time==1 or press_time==2:
            count_down-=1
            print("%s second"%(count_down))
        time.sleep(1)
except KeyboardInterrupt:
    print("User press Ctrl+c ,exit;")
finally:
    cleanup(pin_btn)
    cleanup(pin_led)