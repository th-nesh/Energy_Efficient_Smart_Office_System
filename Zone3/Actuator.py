import time
import RPi.GPIO as IO  
import grovepi

class Window_Servo:
    def __init__(self,port, buzzer):
        self.buzzer =  buzzer
        self.port = port  
        grovepi.digitalWrite(self.buzzer,0)                     
        IO.setwarnings(False)          
        IO.setmode (IO.BCM)            
        IO.setup(self.port,IO.OUT)            
        self.p = IO.PWM(self.port,50)              
        self.p.start(1.5)
        #self.p.ChangeDutyCycle(3)
    def actuate(self, window_data):
        if window_data == "windows_closed" :
            self.p.ChangeDutyCycle(1)          # change duty cycle for getting the servo position to 0º
            time.sleep(1)
            print("closed")
            #self.p.stop()
            Actuator.buzzer_off(self.buzzer)
        elif window_data == "windows_open" :
            self.p.ChangeDutyCycle(3)
            time.sleep(1)
            #self.p.stop()  
            Actuator.buzzer_on(self.buzzer)      
        elif window_data == "windows_partially_open" :
            self.p.ChangeDutyCycle(2.5)        # change duty cycle for getting the servo position to 22.5
            time.sleep(1)
            print("Mid_Open")
            #self.p.stop()
            Actuator.buzzer_on(self.buzzer)
        elif window_data == "windows_warmup_mode" :
            self.p.ChangeDutyCycle(2)        # change duty cycle for getting the servo position to 22.5º
            time.sleep(1)
            #self.p.stop()    
            Actuator.buzzer_off(self.buzzer)                 
        else :
            self.p.ChangeDutyCycle(2.5) 
            time.sleep(1)
            #self.p.stop()
            Actuator.buzzer_off(self.buzzer)

        IO.cleanup()
        
class Heater_LED:
    def __init__(self,port):
        self.port = port                      
        
        
    def actuate(self, heater_data):
        if heater_data == "heating_to_high" :
            Actuator.led_ON(self.port)
        elif heater_data == "heating_to_medium" :
            Actuator.led_blink(self.port)
        elif heater_data == "heating_to_off" :
            Actuator.led_OFF(self.port)
        elif heater_data == "heating_warmup_mode" :
            Actuator.led_OFF(self.port)                  
        else :
            Actuator.led_OFF(self.port) 

class AC_LED:
    def __init__(self,port):
        self.port = port                      
        
        
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
        
    def actuate(self, Light_data):
            try:
                if Light_data == "lights_on" :
                    Actuator.led_ON(self.port)
                
                elif Light_data == "lights_off" :
                    Actuator.led_fade(self.port)
                    
                else :
                    Actuator.led_OFF(self.port)
                time.sleep(1)
                    
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
        
            
class Blind_LED:
    def __init__(self,port):
        self.port = port                      
        
        
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
    
    def led_fade(port):
        grovepi.pinMode(port,"OUTPUT")
        time.sleep(1)
        i =0
        
        try:
                if i >255:
                    i = 0
                grovepi.analogWrite(port,i)
                i = i + 20
                time.sleep(0.5)
        except KeyboardInterrupt:
                grovepi.analogWrite(port,0)
                
        except IOError:
                print ("Error")
            
    
    def led_blink(port):
        grovepi.pinMode(port,"OUTPUT")
        #time.sleep(1)
        i =0
        
        try:
                #Blink the LED
                grovepi.digitalWrite(port,1)		# Send HIGH to switch on LED
                
                time.sleep(0.1)

                grovepi.digitalWrite(port,0)		# Send LOW to switch off LED
               
                time.sleep(0.1)

        except KeyboardInterrupt:	# Turn LED off before stopping
                grovepi.digitalWrite(port,0)
                
        except IOError:				# Print "Error" if communication error encountered
                print ("Error")
    def led_ON(port):
        grovepi.pinMode(port,"OUTPUT")
        #time.sleep(1)
        try:
                #Blink the LED
            grovepi.digitalWrite(port,1)		# Send HIGH to switch on LED
                
        except KeyboardInterrupt:	# Turn LED off before stopping
            grovepi.digitalWrite(port,0)
            
        except IOError:				# Print "Error" if communication error encountered
            print ("Error")
    def led_OFF(port):
            grovepi.pinMode(port,"OUTPUT")
            try:
                #Blink the LED
                grovepi.digitalWrite(port,0)		# Send Low to switch off LED
                
            except KeyboardInterrupt:	# Turn LED off before stopping
                grovepi.digitalWrite(port,0)
                
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
            time.sleep(1)
            
    def buzzer_on(port):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.digitalWrite(port,0)
        
        try:
                # Buzz for 1 second
                grovepi.digitalWrite(port,1)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
                grovepi.digitalWrite(port,0)
                
        except IOError:
                print ("Error")
                
    def buzzer_off(port):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.digitalWrite(port,0)
        
        try:

                # Stop buzzing for 1 second and repeat
                grovepi.digitalWrite(port,0)

        except KeyboardInterrupt:
                grovepi.digitalWrite(port,0)
                
        except IOError:
                print ("Error")

