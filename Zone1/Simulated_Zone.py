from Sensor import *
from Actuator import *
from Data_Processor import *
from AI_Planner import *
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import time

#Initialize all Classes and variables
co2 = Simulated_Sensor(500, 25, 300, 2500)
dht = DHT_Sensor(3)
occ = Occupancy_Sensor(2)
lux = Light_Sensor(2)
sd = data_json()
ms = MQTT_Communication("Zone_1")
planner = ai_planner()
interval = 1
window = Window_Servo(18,7)
heater = Heater_LED(6)
ac = AC_LED(4)
light = Light_LED(8)
blind = Blind_LED(5)
file_path = "/home/pi/smart_office/sensor_data.json"
WC_path = "/home/pi/Desktop/smart_office/WC_Mode.json"
MQTT_SERVER = "192.168.0.121"
MQTT_PATH = "Zone_Override"

def heat_index_calc(temp ,humidity):
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

    
while True:
        dt =  datetime.now().strftime("%d-%m-%YT%H:%M:%S")
        temp,hum = dht.sense()
        
        data_packet = {"Zone_1":
                {
         "time_stamp": dt,
         "Zone_Heat_Index ": heat_index_calc(temp,hum),
         "Zone_Lighting"  : lux.sense(),
         "Zone_Occupancy"  : occ.sense(),
         "Zone_CO2"  : co2.sense(),
         "Zone_Temperature" : temp,
         "Zone_Humidity"  : hum,
            
        }
        }
        print(data_packet)
        with open(WC_path, "r") as json_file:
            for key, values in json.loads(json_file.readlines()[-1]).items():
                    a = values
        if a == "(Is_Warmup_Mode occ_val)":
                inp = [a, '', '','']
                mode = "WC"
               
        else:
                inp = planner.context_generator(data_packet)
                mode = ""
               
        action = planner.ai_planning(inp)
        if mode == "WC":
            actuation= {"Light": action [0], "Blind": action [1], "Window": action[4], "Heater": action [2],"AC" : action[3]}
        else:
            actuation= {"Light": action [0], "Blind": action [1], "Window": action[2], "Heater": action [3],"AC" : action[4]}
        data_packet["Zone_1"].update(actuation)
        data = json.dumps(data_packet)
        ms.mqtt_publish("Zone1_Data", data)
        if mode == "WC":
            light.actuate(action[0])
            blind.actuate(action[1])
            window.actuate(action[4])
            heater.actuate(action[2])
            ac.actuate(action[3])
        else:
            light.actuate(action[0])
            blind.actuate(action[1])
            window.actuate(action[2])
            heater.actuate(action[3])
            ac.actuate(action[4])
        sd.store_json(data_packet,file_path)
        
        


