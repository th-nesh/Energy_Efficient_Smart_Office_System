import json
from datetime import datetime
from random import random
import time
import math
import requests
#import grovepi

# Simulate Carbon Dioxide sensor values
class CarbonDioxide_Sensor:
    sensorType = "temperature"
    instanceID = "32kd403ks"
    unit = "celsius"
    
    def __init__(self, averageCO2, CO2Variation, minCO2, maxCO2):
        self.averageCO2 = averageCO2
        self.CO2Variation = CO2Variation
        self.minCO2 = minCO2
        self.maxCO2 = maxCO2
        self.value = 0.0
        
    def sense(self):
        self.value = self.complexRandom()
        return self.value

    def complexRandom(self):
        value = self.averageCO2 * (1 + ((self.CO2Variation / 100) * (3 * random() - 1)))
        value = max(value, self.minCO2)
        value = min(value, self.maxCO2)
        return value 

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
                        occ_state = "Occupied"

                    # if your hold time is less than this, you might not see as many detections
                time.sleep(.2)
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

                print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
                time.sleep(.5)
                return (sensor_value)

            except IOError:
                print ("Error")
                       
# Accumulate sensor data and preprocess them
class Data_Processor:
    def __init__(self, interval):
        self.interval = interval
        self.co2 = CarbonDioxide_Sensor(500, 25, 300, 2500)
        self.dht = DHT_Sensor(4)
        self.occ = Occupancy_Sensor(5)
        self.lux = Light_Sensor(1)
        
    def heat_index_calc(self, temp , humidity):
        c1 = -8.784
        c2 = 1.611
        c3 = 2.338
        c4 = -0.146
        c5 = -0.012
        c6 = -0.016
        c7 = 2.211e-3
        c8 = 8.5282e-4
        c9 = -1.99e-6
        heat_index = c1 + (c2*temp) + (c3*humidity) + (c4*temp*humidity) + (c5 * temp**2 ) + (c6*humidity**2) + (c7*temp**2 * humidity)+ (c8 * temp *humidity**2) + (c9*temp**2 * humidity**2 )
        return heat_index
        
    def data_packet_creator(self):
        dt =  datetime.now().strftime("%d-%m-%YT%H:%M:%S") 
        data = {
         "time_stamp": dt,
         "Zone_Heat_Index ": self.heat_index_calc(self.dht.sense()[0], self.dht.sense()[1]),
         "Zone_Lighting"  : self.lux.sense(),
         "Zone_Occupancy"  : self.occ.sense(),
         "Zone_CO2"  : self.co2.sense(),
         "Zone_Temperature" : self.dht.sense()[0],
         "Zone_Humidity"  : self.dht.sense()[1],
            
        }
        return data
    
    def data_packet(self):
        while True:
            data_packet = self.data_packet_creator()
            data_json.store_json(data_packet,"/Users/thinesh/Desktop/sensor.json")
            time.sleep(self.interval)
            #return data_packet
        
            
# Read and Write data in JSON Format
class data_json:
    def read_json(self,file_path:str) -> dict:
        with open(file_path, "r") as json_file:
            content = json.load(json_file)
        return content

    def store_json(self, data:dict, file_path:str):
        with open(file_path, "a+") as json_file:
            json.dump(data, json_file)

# dp = Data_Processor(1)
# dj = data_json()

# dt =  datetime.now().strftime("%d-%m-%YT%H:%M:%S") 
# message1 =  {
#     "time_stamp": dt,
#     "temp_value" : 1,
#     "temp_unit"  : 23
    
# }

# message2 =  {
#     "time_stamp": dt,
#     "temp_value" : 1,
#     "temp_unit"  : 2
# }

# message3 = {
#     "area1 ": message1,
#     "area2": message2
# }
# dj.store_json(message3, "/Users/thinesh/Desktop/sensor.json")
# store_json(message2, "/Users/thinesh/Desktop/sensor.json")
# a = dj.read_json("/Users/thinesh/Desktop/sensor.json")

#print (a)
domainfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officedomain.pddl"
problemfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officeproblem.pddl"
data = {'domain': open(domainfile, 'r').read(),
            'problem': open(problemfile, 'r').read()}

response = requests.post('http://solver.planning.domains/solve', json=data).json()
action = []
for i in range(0,5):
   action.append(response["result"]["plan"][i].split()[0])

print(action)

#ds = Data_Processor(1)
#ds.data_packet()

