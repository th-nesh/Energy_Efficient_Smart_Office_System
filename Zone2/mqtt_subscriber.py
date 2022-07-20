import paho.mqtt.client as mqtt
import json
import time
MQTT_SERVER = "192.168.0.121"
#MQTT_PATH = "test_channel"
MQTT_PATH = "Zone_Override"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    #a = msg.payload.decode('utf-8')
    #print(a)
    
    a=str(msg.payload)
    print(msg.topic+" "+a)
    
    # decoding json string to dictionary
    receive_decode = str(msg.payload.decode("utf-8","ignore"))
    receive = json.loads(receive_decode)
    file_path = "/home/pi/Desktop/smart_office/Zone2/WC_Mode.json"
    with open(file_path, "a+") as json_file:
            json.dump(receive, json_file)
            json_file.write("\n")
    
    
    
    #printing a specific key and its value from dictionary
    #print(type(receive))
    #print ("content:",receive)
    # more callbacks, etc
time.sleep(2)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
