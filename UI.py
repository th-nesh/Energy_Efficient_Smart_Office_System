import streamlit as st
import pandas as pd
import json
import requests 
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from streamlit_metrics import metric, metric_row
import plotly.figure_factory as ff


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
original_title = '<p style="font-family:Courier; color:Black; font-size: 40px;"> Energy Efficient Smart Office</p>'
st.markdown(original_title, unsafe_allow_html=True)
zone1_df = zone2_df
col1, col2, col3 = st.columns(3)
col1.metric(label="Temperature", value=(str(round(zone1_df.iloc[-1]["Zone_Temperature"],1)) + "°C"), delta= str(round((zone1_df.iloc[-1]["Zone_Temperature"] - zone1_df.iloc[-2]["Zone_Temperature"]),1))+ "°C")
col2.metric(label="Humidity", value=(str(round(zone1_df.iloc[-1]["Zone_Humidity"],1)) + "%"), delta= str(round((zone1_df.iloc[-1]["Zone_Humidity"] - zone1_df.iloc[-2]["Zone_Humidity"]),1))+ "%")

# Functions for each of the pages
def home(uploaded_file):
    if uploaded_file:
        st.header('Begin exploring the data using the menu on the left')
    else:
        st.header('To begin please upload a file')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(zone2_df.describe())

def data_header():
    st.header('Header of Dataframe')
    st.write(zone2_df.head())

def displayplot():
    st.header('Plot of Data')
    
    fig, ax = plt.subplots(1,1)
    ax.scatter(x=df['Depth'], y=df['Magnitude'])
    ax.set_xlabel('Depth')
    ax.set_ylabel('Magnitude')
    
    st.pyplot(fig)
    
def interactive_plot():
    col1, col2 = st.columns(2)
    
    x_axis_val = zone2_df["time_stamp"]
    y_axis_val = col2.selectbox('Select the Y-axis', options=zone2_df.columns)

    plot = px.area(zone2_df, x=x_axis_val, y=y_axis_val)
    plot.add_scatter(x=x_axis_val, y=zone2_df["Zone_CO2"])
    st.plotly_chart(plot, use_container_width=True)

    
interactive_plot()
st.sidebar.title('Zone Data')
#Sidebar navigation
st.sidebar.header('Select the Zone to analyze')
options = st.sidebar.radio('Select Zone:', ['Office','Zone 1', 'Zone 2', 'Zone 3'])

import base64
import streamlit as st


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

set_background("/Users/thinesh/Desktop/University/3. Summer 2022/Smart Cities and IoT/Project/Smart_Cities Code/office-hintergrund-fuer-videokonferenzen_23-2148641674.webp")


