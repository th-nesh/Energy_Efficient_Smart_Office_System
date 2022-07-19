from Sensor import Simulated_Sensor
#from Actuator import *
from Data_Processor import *
from AI_Planner import *
from datetime import datetime
import time

#Initialize all Classes and variables
co2 = Simulated_Sensor(600, 25, 300, 1500)
dtemp = Simulated_Sensor(20, 5, 5, 45)
dhum = Simulated_Sensor(50, 10, 25, 90)
occ = Simulated_Sensor(500, 25, 300, 2500)
lux = Simulated_Sensor(30, 1, 20, 40)
sd = data_json()
ms = MQTT_Communication("Zone3")
planner = ai_planner()
interval = 2
# window = Window_Servo(18,7)
# heater = Heater_LED(6)
# ac = AC_LED(4)
# light = Light_LED(8)
# blind = Blind_LED(5)
file_path = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Zone3/Zone3_data.json"

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
        data_packet = {"Zone_3":
                {
         "time_stamp": dt,

         "Zone_Heat_Index ": heat_index_calc(dtemp.sense(),dhum.sense()),
         "Zone_Lighting"  : lux.sense(),
         "Zone_Occupancy"  : occ.BooleanRandom(),
         "Zone_CO2"  : co2.sense(),
         "Zone_Temperature" : dtemp.sense(),
         "Zone_Humidity"  : dhum.sense(),
            
        }
        }
        print(data_packet)

        action = planner.ai_planning(data_packet)
        print(action)
        # light.actuate(action[0])
        # blind.actuate(action[1])
        # window.actuate(action[2])
        # print("window actuated")
        # heater.actuate(action[3])
        # ac.actuate(action[4])
        actuation= {"Light": action [0], "Blind": action [1], "Window": action[2], "Heater": action [3], "AC" : action[4]}
        data_packet.update(actuation)
        data = json.dumps(data_packet)
        ms.mqtt_publish("Zone3_Data", data)
        sd.store_json(data_packet,file_path)
        time.sleep(interval)
        

