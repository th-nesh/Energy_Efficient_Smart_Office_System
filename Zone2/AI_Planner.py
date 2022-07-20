import requests

class ai_planner:
        
    def CO2_parser(self,x):
        if x>1000:
            return "(Is_CO2_critical c_val)"
        elif x>850 and x<1000:
            return "(Is_CO2_sub_critical c_val)"
        else:
            return "(Is_CO2_normal c_val)"
    def Lighting_parser(self,x):
        if x>200:
            return "(Is_Light_Bright light_val)"
        elif x>150 and x<200:
            return "(Is_Light_Normal light_val)"
        else:
            return "(Is_Light_Gloomy light_val)"

    def Heat_Index_parser(self,x):
        if x>35:
                return "(Is_Temp_High temp_val)"
        elif x>15 and x<35:
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
        data_x = data["Zone_2"]
        print(data_x)
        for key, value in data_x.items():
            
            if key == "Zone_CO2":
                input.append(self.CO2_parser(value))
            if key == "Zone_Heat_Index ":
                input.append(self.Heat_Index_parser(value))
            elif key == "Zone_Lighting":
                input.append(self.Lighting_parser(value))
            elif key == "Zone_Occupancy":
                input.append(self.Occupancy_parser(value))
            else:
                pass
            
        return input
            
    # def context_parser(self):
        
    def ai_planning(self,input):
            action = []
            
            print(input)
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
            out+= """

                    """

            out+= """(:goal (and(or 
                    (Heating_Off heat_val)
                    (Heating_High heat_val)
                    (Heating_Medium heat_val)
                    (Heating_Warmup heat_val))
                    (or
                    (AC_On ac_val)
                    (AC_Off ac_val)
                    (AC_Warmup ac_val))
                    (or
                    (Window_Closed w_val)
                    (Window_Open w_val)
                    (Window_Mid_Open w_val)
                    (Window_Warmup w_val)
                    )
                    (or
                    (Blind_Closed blind_val)
                    (Blind_Open blind_val)
                    (Blind_Partially_Open blind_val)
                    (Blind_Warmup blind_val))
                    (or
                    (Lights_On l_val)
                    (Lights_Off l_val)
                    (Lighting_Warmup l_val))
                )

                )
                )"""
            
            

            filename = "office_problem"
            with open(filename, "w") as f:
                f.write(out)
                
            domainfile = r"/home/pi/smart_office/Zone2/officedomain.pddl"
            problemfile = r"/home/pi/smart_office/officeproblem.pddl"
            data = {'domain': open(domainfile, 'r').read(),
                        'problem': open(filename, 'r').read()}

            response = requests.post('http://solver.planning.domains/solve', json=data).json()
            
            for i in range(5):
                action.append(response["result"]["plan"][i]["name"].split()[0][1:])
                
            return action
        