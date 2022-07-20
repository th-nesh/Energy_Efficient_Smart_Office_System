import streamlit as st
import base64
import pandas as pd
import json
from Data_Processor import *
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from streamlit_metrics import metric, metric_row
import plotly.figure_factory as ff
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=2000, limit=1000, key="fizzbuzzcounter")
file_path1 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone1 Data.json"
file_path2 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone2 Data.json"
file_path3 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone3 Data.json"
zone1_df = pd.DataFrame()
zone2_df = pd.DataFrame()
zone3_df = pd.DataFrame()
with open(file_path1, "r") as json_file:
    for line in (json_file.readlines()[-50:]):
        for key, values in json.loads(line).items():
            zone1_df = zone1_df.append(values, ignore_index= True)
with open(file_path2, "r") as json_file:
    for line in (json_file.readlines()[-50:]):
        for key, values in json.loads(line).items():           
            zone2_df = zone2_df.append(values,ignore_index= True)
with open(file_path3, "r") as json_file:
    for line in (json_file.readlines()[-50:]):
        for key, values in json.loads(line).items():           
            zone3_df = zone3_df.append(values,ignore_index= True)
            
original_title = '<p style="font-family:Courier; color:White; font-size: 40px;"> Energy Efficient Smart Office</p>'
st.markdown(original_title, unsafe_allow_html=True)
# Functions for each of the pages
def data_header(df):
    st.header('Data from the Zone')
    st.write(df)

    
def displaymetric(df):
    st.header('Zone Metrics')
    col1, col2, col3,col4, col5 = st.columns(5)
    col1.metric(label="Temperature", value=(str(round(df.iloc[-1]["Zone_Temperature"],1)) + "°C"), delta= str(round((df.iloc[-1]["Zone_Temperature"] - df.iloc[-2]["Zone_Temperature"]),1))+ "°C")
    col2.metric(label="Humidity", value=(str(round(df.iloc[-1]["Zone_Humidity"],1)) + "%"), delta= str(round((df.iloc[-1]["Zone_Humidity"] - df.iloc[-2]["Zone_Humidity"]),1))+ "%")
    col3.metric(label="CO2", value=(str(round(df.iloc[-1]["Zone_CO2"],1)) + "ppm"), delta= str(round((df.iloc[-1]["Zone_CO2"] - df.iloc[-2]["Zone_CO2"]),1))+ "ppm")
    col4.metric(label="Light Intensity", value=(str(round(df.iloc[-1]["Zone_Lighting"],1))), delta= str(round((df.iloc[-1]["Zone_Lighting"] - df.iloc[-2]["Zone_Lighting"]),1)))
    col5.metric(label="Occupancy State", value=(str(df.iloc[-1]["Zone_Occupancy"]) + "%"))
    
def interactive_plot(df):
    st.header('Data visualization')
    col1, col2 = st.columns(2)
    with col1:
        st.header('Actuator')
        plot = px.area(df, x=x_axis_val, y=y_axis_act_val)
        st.plotly_chart(plot)
    with col2:
        st.header('Sensor')
        plot = px.area(df, x=x_axis_val, y=y_axis_sense_val)
        st.plotly_chart(plot)

col1, col2 = st.columns(2)
st.header('Zone Data Analysis')
wc_mode = col1.selectbox('Warm-up Mode:', ['Disable', 'Enable'])
ms = MQTT_Communication("UI")
try :
    if wc_mode == "Enable":
        data_packet = {"WC_Mode" : "(Is_Warmup_Mode occ_val)"}
        data = json.dumps(data_packet)
        ms.mqtt_publish("Zone_Override", data = data)
    elif wc_mode =="Disable":
        data_packet = {"WC_Mode" : "null"}
        data = json.dumps(data_packet)
        ms.mqtt_publish("Zone_Override", data = data)
except ValueError:
    print("error")

#col2.button("Disable Warm-up Mode", key="121",help = "Select to de-activate Warm-up Mode", on_click= warmup_mode("dwc"))
col1, col2,col3 = st.columns(3)
options = col1.selectbox('Select Zone:', ['Zone 1', 'Zone 2', 'Zone 3'])
x_axis_val = zone1_df["time_stamp"]
y_axis_act_val = col2.selectbox('Select the actuator', options=zone1_df.columns[0:4])
y_axis_sense_val = col3.selectbox('Select the sensor', options=zone1_df.columns[5:])
if options == "Zone 1":
    displaymetric(zone1_df)
    interactive_plot(zone1_df)
    data_header(zone1_df[::-1])
      
elif options == "Zone 2":
    displaymetric(zone2_df)
    interactive_plot(zone2_df)
    data_header(zone2_df[::-1])
else:
    displaymetric(zone3_df)
    interactive_plot(zone3_df)
    data_header(zone3_df[::-1])
    


