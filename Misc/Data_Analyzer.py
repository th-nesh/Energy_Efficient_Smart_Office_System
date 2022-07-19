import json
from datetime import datetime
from random import random, uniform
import time
import math
import requests
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pandas as pd

file_path = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/sensor_data.json"
zone1_df = pd.DataFrame()
zone2_df = pd.DataFrame()
with open(file_path, "r") as json_file:
    for line in json_file.readlines():
        for key, values in json.loads(line).items():
            if key == "Zone1":
                zone1_df = zone1_df.append(values, ignore_index= True)
            else:
                zone2_df = zone2_df.append(values,ignore_index= True)

class ai_planner:
    def __init__(self,zones):
        self.zones =zones
        
    def CO2_parser(self,x):
        if x>2000:
            return "(Is_CO2_critical c_val)"
        elif x>1000 and x<2000:
            return "Sub_Critical"
        else:
            return "(Is_CO2_normal c_val)"
    def Lighting_parser(self,x):
        if x>500:
            return "(Is_Light_Bright l_val)"
        elif x>250 and x<500:
            return "(Is_Light_Normal l_val)"
        else:
            return "(Is_Light_Gloomy l_val)"

    def Heat_Index_parser(self,x):
        if x>30:
                return "(Is_Temp_High temp_val)"
        elif x>10 and x<30:
            return "(Is_Temp_Ideal temp_val)"
        else:
            return "(Is_Temp_Low temp_val)"

    def Occupancy_parser(self,x):
        if x == "Occupied":
                return "(Is_Occupied occ_val)"
        else:
            return "(Is_Un_Occupied occ_val)"   
        
    def context_generator(self):
        input = [] 
        data = zone2_df[-1:].to_dict("list")

       
        for key, value in data.items():
            if key == "Zone_CO2":
                input.append(self.CO2_parser(value[0]))
            if key == "Zone_Heat_Index ":
                input.append(self.Heat_Index_parser(value[0]))
            elif key == "Zone_Lighting":
                input.append(self.Lighting_parser(value[0]))
            elif key == "Zone_Occupancy":
                input.append(self.Occupancy_parser(value[0]))
            else:
                pass
    


        return input
            
        
       
    # def context_parser(self):
        
    def ai_planning(self):
            self.action = []
            input= self.context_generator() 
            print(input)
            print(len(input))
            out = """(define (problem tempsense) (:domain covisstorage)

        (:objects 
        occ_val temp_val ac_val heat_val light_val blind_val w_val c_val l_val)
        
        
        """
        
            out+="""(:init"""
            out+= input[0]
            out+= input[1]
            out+= input[2]
            out+= input[3]

            out+=""")"""
            out+="""(:goal (and(or"""
            out+= "(Heating_Off heat_val)"
            out+= "(Heating_High heat_val)"
            out+= "(Heating_Medium heat_val)"
            out+= "(or (AC_On ac_val)"
            out+= "(AC_Off ac_val))"
            out+= "(or (Window_Closed w_val)"
            out+= "(Window_Open w_val)"
            out+= "(Window_Mid_Open w_val))"
            out+= "(or (Blind_Closed blind_val)"
            out+= "(Blind_Open blind_val))"
            out+= "(or (Lights_On l_val)"
            out+= "(Lights_Off l_val))))"
            out+= """       """

            filename = "office_problem"
            with open(filename, "w") as f:
                f.write(out)
                
            domainfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officedomain.pddl"
            problemfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officeproblem.pddl"
            data = {'domain': open(domainfile, 'r').read(),
                        'problem': open(problemfile, 'r').read()}

            response = requests.post('http://solver.planning.domains/solve', json=data).json()

            
            for i in range(0,5):
                self.action.append(response["result"]["plan"][i])
                
            print(self.action)
        
    def context_parser(self):
       action = self.action
       for i in range(len(action)):
           print(type(action[i]))


        
            

m =ai_planner(2)
m.ai_planning()




