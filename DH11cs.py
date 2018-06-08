import RPi.GPIO as GPIO  
import time  
  
#channel =4   
#data = []  
#j = 0  
  
class DH11DEV:
    def __init__(self):
        self.temperature = 24
        self.humidity = 50
        self.channel = 4

    def get_temp(self):
        j = 0
        data = []
        GPIO.setmode(GPIO.BCM)  
        time.sleep(1)  
        GPIO.setup(self.channel, GPIO.OUT)  
        GPIO.output(self.channel, GPIO.LOW)  
        time.sleep(0.03)  
        GPIO.output(self.channel, GPIO.HIGH)  
        GPIO.setup(self.channel, GPIO.IN)  
  
        while GPIO.input(self.channel) == GPIO.LOW:  
            continue  
        while GPIO.input(self.channel) == GPIO.HIGH:  
            continue  
  
        while j < 40:  
            k = 0  
            while GPIO.input(self.channel) == GPIO.LOW:  
                continue  
            while GPIO.input(self.channel) == GPIO.HIGH:  
                k += 1  
                if k > 100:  
                    break  
            if k < 8:  
                data.append(0)  
            else:  
                data.append(1)  
            j += 1  
  
        humidity_bit = data[0:8]  
        humidity_point_bit = data[8:16]  
        temperature_bit = data[16:24]  
        temperature_point_bit = data[24:32]  
        check_bit = data[32:40]  
        
        self.humidity = 0  
        humidity_point = 0  
        self.temperature = 0  
        temperature_point = 0  
        check = 0  
  
        for i in range(8):  
            self.humidity += humidity_bit[i] * 2 ** (7-i)  
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)  
            self.temperature += temperature_bit[i] * 2 ** (7-i)  
            temperature_point += temperature_point_bit[i] * 2 ** (7-i)  
            check += check_bit[i] * 2 ** (7-i)  
  
        tmp = self.humidity + humidity_point + self.temperature + temperature_point  
  
        if check == tmp:  
            pass
        else:  
            self.humidity = 0   
            self.temperature = 0
  
        GPIO.cleanup()  

if __name__ == "__main__":
    dh11 = DH11DEV()
    dh11.get_temp()
    print("Temperature: %d"%dh11.temperature)
    print("humidity: %d"%dh11.humidity)