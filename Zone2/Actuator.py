import time
import RPi.GPIO as IO  
import grovepi

class Window_Servo:
    def __init__(self,port):
        
        self.port = port  
                            
        IO.setwarnings(False)          
        IO.setmode (IO.BCM)            
        IO.setup(self.port,IO.OUT)            
        self.p = IO.PWM(self.port,50)              
        self.p.start(1.5)
    def actuate(self, window_data):
        if window_data == "windows_closed" :
            self.p.ChangeDutyCycle(1)          # change duty cycle for getting the servo position to 0º
            
            
        elif window_data == "windows_open" :
            self.p.ChangeDutyCycle(3) 
            
            
        elif window_data == "windows_partially_open" :
            self.p.ChangeDutyCycle(2.5)        # change duty cycle for getting the servo position to 22.5
            
            
        elif window_data == "windows_warmup_mode" :
            self.p.ChangeDutyCycle(2)        # change duty cycle for getting the servo position to 22.5º
            
            
        else :
            self.p.ChangeDutyCycle(2.5) 
            
        
class Heater_LED:
    def __init__(self,port):
        self.port = port
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(port,IO.OUT) # Output Mode
        IO.output(port,IO.LOW)
        
        
    def actuate(self, heater_data):
        if heater_data == "heating_to_high" :
            Actuator.led_ON(self.port)
        elif heater_data == "heating_to_medium" :
            Actuator.led_blink(self.port)
        elif heater_data == "heating_to_off" :
            Actuator.led_OFF(self.port)
        elif heater_data == "heating_warmup_mode" :
            Actuator.led_blink(self.port)                  
        else :
            Actuator.led_OFF(self.port) 

class AC_LED:
    def __init__(self,port):
        self.port = port
        IO.setwarnings(False)
        IO.setup(port,IO.OUT) # Output Mode
        IO.output(port,IO.LOW)
        
        
    def actuate(self, AC_data):
        if AC_data == "ac_switched_on" :
            Actuator.led_ON(self.port)
        elif AC_data == "ac_switched_off" :
            Actuator.led_blink(self.port)                
        else :
            Actuator.led_OFF(self.port)   
               
class Light_LED:
    def __init__(self,port):
        self.port = port
        IO.setwarnings(False)
        IO.setup(port,IO.OUT) # Output Mode
        IO.output(port,IO.LOW)
        
        
    def actuate(self, Light_data):
            try:
                if Light_data == "lights_on" :
                    Actuator.led_ON(self.port)
                
                elif Light_data == "lights_off" :
                    Actuator.led_blink(self.port)
                    
                else :
                    Actuator.led_OFF(self.port)
                    
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
        
            
class Blind_LED:
    def __init__(self,port):
        self.port = port
        IO.setwarnings(False)
        IO.setup(port,IO.OUT) # Output Mode
        IO.output(port,IO.LOW)
        
        
    def actuate(self, blind_data):
        if blind_data == "blinds_open" :
            Actuator.led_ON(self.port)
        elif blind_data == "blinds_mid_open" :
            Actuator.led_blink(self.port)
        elif blind_data == "blinds_closed" :
            Actuator.led_OFF(self.port)                 
        else :
            Actuator.led_OFF(self.port) 
            
class Actuator:

    def led_ON(port):
        
        IO.output(port,IO.HIGH)		# Send HIGH to switch on LED
                
    def led_OFF(port):
        
        IO.output(port,IO.LOW)		# Send Low to switch off LED
        
    def led_blink(port):
    
        try:
            IO.output(port,IO.HIGH)		# Send HIGH to switch on LED
            time.sleep(0.1)
            IO.output(port,IO.LOW)		# Send LOW to switch off LED
            time.sleep(0.1)
                
        except IOError:				# Print "Error" if communication error encountered
                print ("Error")
        

                
            
            
    
                
                
    

        


