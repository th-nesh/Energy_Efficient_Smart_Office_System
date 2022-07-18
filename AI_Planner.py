import requests

class ai_planner:
        
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
        
    def context_generator(self, data):
        input = [] 
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
        
    def ai_planning(self, data):
            action = []
            input= self.context_generator(data) 
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
                        'problem': open(filename, 'r').read()}

            response = requests.post('http://solver.planning.domains/solve', json=data).json()

            
            for i in range(0,5):
                action.append(response["result"]["plan"][i])
                
            return action
        