import requests

input= ["(Is_Un_Occupied occ_val)","(Is_Temp_High temp_val)","(Is_CO2_critical c_val)","(Is_Light_Bright l_val)"]
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
out+= """"

"""
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
out+= "(Lights_Off l_val))))))"
out+= """       """

filename = "office_problem"
with open(filename, "w") as f:
       f.write(out)
        
domainfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officedomain.pddl"
problemfile = r"/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/officeproblem.pddl"
data = {'domain': open(domainfile, 'r').read(),
                'problem': open(filename, 'r').read()}

response = requests.post('http://solver.planning.domains/solve', json=data).json()
    #print(response)
action = []
for i in range(0,5):
        action.append(response["result"]["plan"][i])
print(action)
    #input.append(action)
    #print(input)
    
        

