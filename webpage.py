import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.fft import rfft, rfftfreq
import math

import paho.mqtt.client as mqtt 
#import librosa 
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def plot_senogram(data, lowcut, highcut):
    st.write('Sonogram plot')
    ax.set_xlabel("Time /s")
    ax.set_ylabel("Data")
    fs = 44100
    y = butter_bandpass_filter(data, lowcut, highcut, fs)
    ax.plot(y)
    plt.show()
    st.pyplot(fig) 

st.set_page_config(
 page_title='SoundCloud',
 layout="centered",
 page_icon='icon.png',
 initial_sidebar_state="auto",
)

mqttBroker ="test.mosquitto.org" 
client = mqtt.Client("soundcloud")
client.connect(mqttBroker, port=1883) 

def publish_status():
    client.publish("Status", st.session_state["start"])
 


#read txt from a URL

def get_data():
    with open("dados.txt","r") as f:
        last_line = f.readlines()[-1]
        return float(last_line[:-1])



st.markdown("<h1 style='text-align: center; color: white; padding:20px'>SoundCloud</h1>", unsafe_allow_html=True)

st.write('___')
      

with st.sidebar:
    st.write('___')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button('Start'):
            st.session_state["start"] = True
            publish_status()




my_file = Path("dados.txt")
if my_file.is_file() and 'start' in st.session_state:
    # file exists
   
    with st.sidebar:

        col1, col2, col3, col4 = st.columns(4)
        
        with col1: 
            if st.button('Stop'):
                st.session_state["start"] = False
                publish_status()
             
           
        with col4: 
            if st.button('RESET'):
                del st.session_state["start"]
                del st.session_state['data']
   
        
        with st.sidebar:
            if 'start' in st.session_state and st.session_state["start"] == True:
                st.success("Running")
            else:
                st.error("Stopped")
        
    radio = st.sidebar.radio("Choose method",("Real-time Plot", "Sonogram","Features"))
        
    selectbox = st.sidebar.selectbox(
    "Select operation",
    ("Stream", "Open", "Save"))
    
    if selectbox == "Save":
        if 'data' not in st.session_state:
            st.title("Please generate data")
        else:
            with st.sidebar:
                with st.spinner('Wait for it...'):
                    time.sleep(0.5)
                np.savetxt(r'C:/Users/tbati/Downloads/data.txt', st.session_state['data'].values, fmt='%f', delimiter='\t')
                
                st.success("Done!")
    
    if radio == "Real-time Plot" and 'start' in st.session_state:
        
        # Initialization
        if 'data' not in st.session_state and st.session_state["start"] == True:
                
            seconds = 0
        
            df = pd.DataFrame({"data": []})
            
            plot = st.line_chart(data=None,width=15,height=5)
               
            while st.session_state["start"] == True:
                point = pd.DataFrame({"data": [get_data()]})
                
                plot.add_rows(point)
                
                df = df.append(point,ignore_index = True)
                
                time.sleep(0.1)
                seconds += 0.1
        
                st.session_state['data'] = df
            
        else:
            
            st.line_chart(st.session_state['data'])
            

        
        is_check = st.checkbox("Display Data")
        if is_check:
            st.write(st.session_state['data'].T)
            
    
    if radio == "Sonogram" and 'start' in st.session_state and 'data' in st.session_state:
        width = st.sidebar.slider("Plot width", 1, 20, 15)
        height = st.sidebar.slider("Plot height", 1, 10, 5)
        
        fig, ax = plt.subplots(figsize=(width, height)) 
        plt.subplots(figsize=(width, height)) 
        
        ax.set_xlabel("Time")
        ax.set_ylabel("Data")
        
        ax.plot(st.session_state['data'])
        
        plt.show()
        
        st.pyplot(fig) 
    
        is_check = st.checkbox("Display Data")
        if is_check:
            st.write(st.session_state['data'].T)
    
    if radio == "Features" and 'start' in st.session_state and 'data' in st.session_state:
        my_expander = st.expander('Band Pass filter')
        my_expander.write('Choose low-cut and high-cut frequencies:')
        lowcut = my_expander.slider("Low-cut frequency", 0.01, 20000.0, 0.01)
        highcut = my_expander.slider("High-cut frequency", 0.01, 20000.0, 20000.0)
        
       # add_selectbox = st.selectbox(
        #    "Select Domain",
         #   ("Sonogram", "Time Domain", "Frequency domain"))
         
        #d = pd.DataFrame({"sonogram": [], "timedomain":[], "frequencydomain": []})
        show = st.multiselect("Select plot", ['Sonogram','Time Domain','Frequency Domain'], ['Sonogram'])
        
        width = st.sidebar.slider("Plot width", 1, 20, 15)
        height = st.sidebar.slider("Plot height", 1, 10, 5)
        
  
        fig, ax = plt.subplots(figsize=(width, height)) 
        plt.subplots(figsize=(width, height)) 
        
        if len(show) == 1:
            if show[0] == 'Sonogram':
                 plot_senogram(st.session_state['data'], lowcut, highcut)
            
            if show[0] == 'Time Domain':
                st.write('Time Domain plot')
                
            if show[0] == 'Frequency Domain':
                st.write('Frequency Domain plot')
        
        
        if len(show) == 2:
            if 'Sonogram' in show and 'Time Domain' in show:
                 plot_senogram(st.session_state['data'], lowcut, highcut)
                 
                 st.write('Time Domain plot')
                 
            if 'Sonogram' in show and 'Frequency Domain' in show:
                plot_senogram(st.session_state['data'], lowcut, highcut)
                  
                st.write('Frequency Domain plot')     
                
            if 'Time Domain' in show and 'Frequency Domain' in show:
                st.write('Time Domain plot')
                   
                st.write('Frequency Domain plot')     
                 
              
        if len(show) == 3:
            plot_senogram(st.session_state['data'], lowcut, highcut)
            
            st.write('Time Domain plot')
             
            st.write('Frequency Domain plot')
        
        
    
else:
    with st.container():
        st.info('Welcome to "SoundCloud"!')
        st.info("Please generate a new file.")
    with st.sidebar:
        st.title("About")
        st.info('This project was created as a data logger for recorded sounds that allows real-time visualization, analysis of the signal/features and to save the information to a file. All the source code can be found in https://github.com/tsBatista99/Cloud-logger-AAIB.git')
