from datetime import datetime
from random import random,uniform
import time
import math
#import grovepi

# Simulate Carbon Dioxide sensor values
class Simulated_Sensor:
    
    def __init__(self, average, Variation, min, max):
        self.average = average
        self.Variation = Variation
        self.min = min
        self.max = max
        self.value = 0.0
        
    def sense(self):
        self.value = self.complexRandom()
        return self.value

    def complexRandom(self):
        value = self.average * (1 + ((self.Variation / 100) * (3 * random() - 1)))
        value = max(value, self.min)
        value = min(value, self.max)
        return value 
    
    def BooleanRandom(self):
        value =  uniform(0.0,1.0)
        if value < 0.8:
            return "Occupied"
        else:
            return "Unoccupied"
#Fetch Digital temperature Humidity Sensor Values
class DHT_Sensor:
    
    def __init__(self,port):
        self.port = port
    
    def sense(self):
        blue = 0    # The Blue colored sensor.
        white = 1   # The White colored sensor.

        while True:
            try:
                # This example uses the blue colored sensor. 
                # The first parameter is the port, the second parameter is the type of sensor.
                [temp,humidity] = grovepi.dht(self.port,blue)  
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    return(temp, humidity)
            except IOError:
                print ("Error")
                
#Fetch Occupancy Sensor Values
class Occupancy_Sensor:
    
    def __init__(self,port):
        self.port = port
    
    def sense(self):
        motion=0
        grovepi.pinMode(self.port,"INPUT")

        while True:
            try:
                # Sense motion, usually human, within the target range
                motion=grovepi.digitalRead(self.port)
                if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
                    if motion==1:
                        occ_state = "Occupied"
                    else:
                        occ_state = "Un_Occupied"

                    # if your hold time is less than this, you might not see as many detections
                time.sleep(1)
                return(occ_state)

            except IOError:
                print ("Error")

#Fetch Light Intensity Sensor Values
class Light_Sensor:
        
    def __init__(self,port):
        self.port = port
    
    def sense(self):
       # SIG,NC,VCC,GND
        self.port = 0
        
        # Turn on LED once sensor exceeds threshold resistance
        threshold = 10

        grovepi.pinMode(self.port,"INPUT")
        
        while True:
            try:
                # Get sensor value
                sensor_value = grovepi.analogRead(self.port)

                # Calculate resistance of sensor in K
                resistance = (float)(1023 - sensor_value) * 10 / sensor_value

                #print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
                time.sleep(1)
                return (sensor_value)

            except IOError:
                print ("Error")
                       