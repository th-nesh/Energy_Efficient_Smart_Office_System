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
file_path1 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone1 Data.json"
file_path2 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone2 Data.json"
file_path3 = "/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/Workstation/Zone3 Data.json"
zone1_df = pd.DataFrame()
zone2_df = pd.DataFrame()
zone3_df = pd.DataFrame()
with open(file_path1, "r") as json_file:
    for line in (json_file.readlines()[-50:]):
        for key, values in json.loads(line).items():
            print(values)
            #zone1_df = zone1_df.append(values, ignore_index= True)
# with open(file_path2, "r") as json_file:
#     for key, values in json.loads(line).items():
#         for key, values in json.loads(line).items():           
#             zone2_df = zone2_df.append(values,ignore_index= True)
# with open(file_path3, "r") as json_file:
#     for key, values in json.loads(line).items():
#         for key, values in json.loads(line).items():           
#             zone3_df = zone3_df.append(values,ignore_index= True)
            
print(zone1_df)
print(zone2_df)
print(zone3_df)
original_title = '<p style="font-family:Courier; color:White; font-size: 40px;"> Energy Efficient Smart Office</p>'
st.markdown(original_title, unsafe_allow_html=True)
zone1_df = zone2_df
# Functions for each of the pages
def data_header(df):
    st.header('Data from the Zone')
    st.write(df)

def warmup_mode(data):
    
    count = 0
    print(count)
    
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
    plot = px.area(df, x=x_axis_val, y=y_axis_val)
    st.plotly_chart(plot)


col1, col2 = st.columns(2)
col1.button("Warm-up Mode", key="212",help = "Select to activate Warm-up Mode", on_click= warmup_mode("wc"))
col2.button("Disable Warm-up Mode", key="121",help = "Select to de-activate Warm-up Mode", on_click= warmup_mode("dwc"))
col1, col2 = st.columns(2)
options = col1.selectbox('Select Zone:', ['Zone 1', 'Zone 2', 'Zone 3'])
x_axis_val = zone1_df["time_stamp"]
y_axis_val = col2.selectbox('Select the Y-axis', options=zone1_df.columns)
  
if options == "Zone 1":
    displaymetric(zone1_df)
    interactive_plot(zone1_df)
    data_header(zone1_df)
      
elif options == "Zone 2":
    displaymetric(zone2_df)
    interactive_plot(zone2_df)
    data_header(zone2_df)
else:
    displaymetric(zone3_df)
    interactive_plot(zone3_df)
    data_header(zone3_df)

    



def get_base64(bin_file): 
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

#set_background("/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/office-hintergrund-fuer-videokonferenzen_23-2148641674.webp")



