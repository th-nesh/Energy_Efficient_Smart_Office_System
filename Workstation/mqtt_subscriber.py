import streamlit as st
import base64
import pandas as pd
import json
import requests 
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from streamlit_metrics import metric, metric_row
import plotly.figure_factory as ff

import paho.mqtt.client as mqtt

MQTT_SERVER = "192.168.0.121"
MQTT_PATH1 = "Zone1_Data"
MQTT_PATH2 = "Zone2_Data"
MQTT_PATH3 = "Zone3_Data"
file_path1 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone1 Data.json"
file_path2 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone2 Data.json"
file_path3 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone3 Data.json"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)
    client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH3)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "Zone1_Data":
        print(msg.topic+" "+str(msg.payload))
        receive_decode = str(msg.payload.decode("utf-8","ignore"))
            # more callbacks, etc
        receive = json.loads(receive_decode)
        
        with open(file_path1, "a+") as json_file:
            json.dump(receive,json_file)
            json_file.write("\n") 
    elif msg.topic == "Zone2_Data":
        print(msg.topic+" "+str(msg.payload))
        receive_decode = str(msg.payload.decode("utf-8","ignore"))
            # more callbacks, etc
        receive = json.loads(receive_decode)
        with open(file_path2, "a+") as json_file:
            json.dump(receive,json_file)
            json_file.write("\n") 
    elif msg.topic == "Zone3_Data":
        print(msg.topic+" "+str(msg.payload))
        receive_decode = str(msg.payload.decode("utf-8","ignore"))
            # more callbacks, etc
        receive = json.loads(receive_decode)
        
        with open(file_path3, "a+") as json_file:
            json.dump(receive,json_file)
            json_file.write("\n") 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()