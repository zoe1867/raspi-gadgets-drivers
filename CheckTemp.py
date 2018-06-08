import DH11Class
import Lcd1602Class
  
if __name__ == "__main__":
    dh11 = DH11Class.DH11DEV()
    dh11.get_temp()

    lcd=Lcd1602Class.LCD1602(0x27, 1)
    lcd.init_lcd()
    str1 = "Temperature: " + str(dh11.temperature)
    str2 = "humidity:    " + str(dh11.humidity)
    print(str1)
    print(str2)  
    lcd.print_lcd(0, 0, str1)
    lcd.print_lcd(0, 1, str2)