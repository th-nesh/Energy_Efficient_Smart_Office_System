import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
class data_json:
    def read_json(self,file_path:str) -> dict:
        with open(file_path, "r") as json_file:
            content = json.load(json_file)
        return content

    def store_json(self, data:dict, file_path:str):
        with open(file_path, "a+") as json_file:
            json.dump(data, json_file)
            json_file.write("\n")
            
class MQTT_Communication: 
    def __init__(self,name):
        self.MQTT_SERVER = "192.168.0.121"
        self.client = mqtt.Client(name)
        self.client.connect(self.MQTT_SERVER,1883,60)
        
    def mqtt_publish(self,topic,data):
        self.client.subscribe(topic)
        self.client.publish(topic = topic, payload = data)