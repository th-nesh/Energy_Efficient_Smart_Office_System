import time
import RPi.GPIO as IO  
import grovepi

class Window_Servo:
    def __init__(self,port, buzzer):
        self.buzzer =  buzzer
        self.port = port  
        self.act = Actuator()                    
        IO.setwarnings(False)          
        IO.setmode (IO.BCM)            
        IO.setup(self.port,IO.OUT)            
        self.p = IO.PWM(self.port,50)              
        self.p.start(1.5)                   
    def actuate(self, window_data):
        if window_data == "Window_Closed" :
            self.p.ChangeDutyCycle(1)          # change duty cycle for getting the servo position to 0º
            time.sleep(1)
            self.p.stop()
            self.act.buzzer_off(self.buzzer)
        elif window_data == "Window_Open" :
            self.p.ChangeDutyCycle(3)
            time.sleep(1)
            self.p.stop()  
            self.act.buzzer_on(self.buzzer)      
        elif window_data == "Window_Mid_Open" :
            self.p.ChangeDutyCycle(2.5)        # change duty cycle for getting the servo position to 22.5
            time.sleep(1)
            self.p.stop()
            self.act.buzzer_off(self.buzzer)
        elif window_data == "Window_Warmup_Mode" :
            self.p.ChangeDutyCycle(2)        # change duty cycle for getting the servo position to 22.5º
            time.sleep(1)
            self.p.stop()    
            self.act.buzzer_off(self.buzzer)                 
        else :
            self.p.ChangeDutyCycle(1.5) 
            time.sleep(1)
            self.p.stop()
            self.act.buzzer_off(self.buzzer)

        IO.cleanup()
        
class Heater_LED:
    def __init__(self,port):
        self.port = port                      
        self.act = Actuator()
        
    def actuate(self, heater_data):
        if heater_data == "Heating_High" :
            self.act.led_ON(self.port)
        elif heater_data == "Heating_Medium" :
            self.act.led_blink(self.port)
        elif heater_data == "Heating_Off" :
            self.act.led_OFF(self.port)
        elif heater_data == "Heating_Warmup_Mode" :
            self.act.led_OFF(self.port)                  
        else :
            self.act.led_OFF(self.port) 

class AC_LED:
    def __init__(self,port):
        self.port = port                      
        self.act = Actuator()
        
    def actuate(self, AC_data):
        if AC_data == "AC_ON" :
            self.act.led_ON(self.port)
        elif AC_data == "AC_OFF" :
            self.act.led_blink(self.port)                
        else :
            self.act.led_OFF(self.port)   
               
class Light_LED:
    def __init__(self,port):
        self.port = port                      
        self.act = Actuator()
        
    def actuate(self, Light_data):
        if Light_data == "AC_ON" :
            self.act.led_ON(self.port)
        elif Light_data == "AC_OFF" :
            self.act.led_blink(self.port)                
        else :
            self.act.led_OFF(self.port)     
            
class Blind_LED:
    def __init__(self,port):
        self.port = port                      
        self.act = Actuator()
        
    def actuate(self, blind_data):
        if blind_data == "Blind_Open" :
            self.act.led_ON(self.port)
        elif blind_data == "Blind_Mid_Open" :
            self.act.led_blink(self.port)
        elif blind_data == "Heating_Closed" :
            self.act.led_OFF(self.port)                 
        else :
            self.act.led_OFF(self.port) 
            
class Actuator:
    
    def led_fade(port):
        grovepi.pinMode(port,"OUTPUT")
        time.sleep(1)
        i =0
        while True:
            try:
                if i >255:
                    i = 0
                grovepi.analogWrite(port,i)
                i = i + 20
                time.sleep(0.5)
            except KeyboardInterrupt:
                grovepi.analogWrite(port,0)
                break
            except IOError:
                print ("Error")
    
    def led_blink(port):
        grovepi.pinMode(port,"OUTPUT")
        time.sleep(1)
        i =0
        while True:
            try:
                #Blink the LED
                grovepi.digitalWrite(port,1)		# Send HIGH to switch on LED
                print ("LED ON!")
                time.sleep(1)

                grovepi.igitalWrite(port,0)		# Send LOW to switch off LED
                print ("LED OFF!")
                time.sleep(1)

            except KeyboardInterrupt:	# Turn LED off before stopping
                grovepi.digitalWrite(port,0)
                break
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
    def led_ON(port):
        grovepi.pinMode(port,"OUTPUT")
        time.sleep(1)
        while True:
            try:
                #Blink the LED
                grovepi.digitalWrite(port,1)		# Send HIGH to switch on LED
                print ("LED ON!")
            except KeyboardInterrupt:	# Turn LED off before stopping
                grovepi.digitalWrite(port,0)
                break
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
    def led_OFF(port):
        grovepi.pinMode(port,"OUTPUT")
        time.sleep(1)
        while True:
            try:
                #Blink the LED
                grovepi.digitalWrite(port,0)		# Send Low to switch off LED
                print ("LED ON!")
            except KeyboardInterrupt:	# Turn LED off before stopping
                grovepi.digitalWrite(port,0)
                break
            except IOError:				# Print "Error" if communication error encountered
                print ("Error")
                          
    def buzzer_on(port):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.digitalWrite(port,0)
        while True:
            try:
                # Buzz for 1 second
                grovepi.digitalWrite(port,1)
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                grovepi.digitalWrite(port,0)
                break
            except IOError:
                print ("Error")
                
    def buzzer_off(port):
        grovepi.pinMode(port,"OUTPUT")
        grovepi.digitalWrite(port,0)
        while True:
            try:

                # Stop buzzing for 1 second and repeat
                grovepi.digitalWrite(port,0)

            except KeyboardInterrupt:
                grovepi.digitalWrite(port,0)
                break
            except IOError:
                print ("Error")

