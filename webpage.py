import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import butter, lfilter
import math
import sklearn
from numpy.fft import fft

import paho.mqtt.client as mqtt 
#import librosa 
import librosa
import librosa.display

RATE = 10
fs = 44100


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter(order, [lowcut,highcut], fs=fs, btype='band')
    y = lfilter(b, a, data)
    return y


def plot_senogram(y):
    fig, ax = plt.subplots(figsize=(14, 4)) 
    st.write('Sonogram plot')
    ax.set_xlabel("Time /s")
    ax.set_ylabel("Data")
    ax.set_title("Sonogram plot", fontsize = 15)
    ax.plot(y)
    plt.show()
    st.pyplot(fig) 


def plot_fft(y, fs):
    st.write('Frequency Domain plot')
    #plot FFT
    X = fft(y)
    N = len(X)
    n = np.arange(N)
    T = N/fs
    freq = n/T 
    # Get the one-sided specturm
    n_oneside = N//2
    # get the one side frequency
    f_oneside = freq[:n_oneside]
    
    fig, ax = plt.subplots(figsize=(14, 4)) 
    plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
    plt.xlabel('Freq /Hz')
    plt.ylabel('FFT Amplitude')
    ax.set_title("Fourier transform plot", fontsize = 15)
    plt.show()
    st.pyplot(fig)
    
def plot_spetrogram(y,fs):
    st.write('Spectrogram plot')
    fig, ax = plt.subplots(1, figsize=(14, 8))
    fig.tight_layout(pad=10.0)
    ax.specgram(y, Fs=fs)
    ax.set_xlabel(xlabel='Time /sec')
    ax.set_ylabel(ylabel='Frequency Amplitude / rad/s')
    helper = [0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000]
    spec_yticks = [6.28 * i for i in helper]
    ax.set_yticks(helper)
    ax.set_yticklabels(spec_yticks)
    ax.set_title("Signal Spectrogram", fontsize = 15)
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
    client.publish("StatusWebAAIB", st.session_state["start"])
 


#read txt from a URL

def get_data():
    with open("/workspace/Cloud-logger-AAIB/dadosSOM.txt","r") as f:
    #with open("dadosSOM.txt","r") as f:
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



my_file = Path("/workspace/Cloud-logger-AAIB/dadosSOM.txt")
#my_file = Path("dadosSOM.txt")

if my_file.is_file() and 'start' in st.session_state:
    # file exists
   
    with st.sidebar:

        col1, col2, col3, col4 = st.columns(4)
        
        with col1: 
            stop = st.button('Stop')
            if stop:
                st.session_state["start"] = False
                publish_status()
                st.session_state["cancel"] = True
             
           
        with col4: 
            reset = st.button('RESET')
            st.session_state["cancel"] = False
   
        
        with st.sidebar:
            if 'start' in st.session_state and st.session_state["start"] == True:
                st.success("Running")
            else:
                st.error("Stopped")
        
    
    if reset == True:
        if 'cancel' in st.session_state and st.session_state["cancel"] == False:
            del st.session_state["start"]
            del st.session_state['data']
            del st.session_state["cancel"]
        st.warning('The data of this session was deleted. Press RESET again to continue.', icon="⚠️")
        
        
    
    selectbox = st.sidebar.selectbox(
    "Select operation",
    ("Stream", "Open", "Save"))
    
    
    if selectbox == "Open":
        st.session_state["start"] = False
        
        uploaded_file = st.file_uploader( label="Choose a file", type = "csv", help="Click the Search file button to open the csv file")
        if uploaded_file is not None:
            del st.session_state['data']
            st.session_state['data'] = pd.read_csv(uploaded_file)
        


    
    if selectbox == "Save":
        if 'data' not in st.session_state:
            st.sidebar.error("Please generate data")
        else:
            csv = st.session_state['data'].to_csv(index=False).encode('utf-8')
            
            with st.sidebar:
                with st.spinner('Wait for it...'):
                    time.sleep(1)
                
                save = st.download_button( label="Download", data = csv, file_name="dataSOM.csv" )
            selectbox = "Stream"
    
    
    radio = st.sidebar.radio("Choose method",("Real-time Plot", "Sonogram","Spectrogram","Features"))
        
    
    
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
                
                time.sleep(1/RATE)
                seconds += 1/RATE
        
                st.session_state['data'] = df
            
        else:
            
            st.line_chart(st.session_state['data'])
            

    
        is_check = st.checkbox("Display Data")
        if is_check:
            st.write(st.session_state['data'].T)
            
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Maximum Power",
                value=round(st.session_state['data'].max())
            )
            
            kpi2.metric(
                label="Average Power",
                value=round(st.session_state['data'].mean())
            )
            
    
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
    

    if radio == "Features" and 'start' in st.session_state:
        y = st.session_state['data']['data'].to_numpy()
        fs = 44100
        
        st.header("Feature extraction")
        st.subheader("Time domain")
        #amplitude envelope
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        st.write("Componente harmónica")
        fig, ax = plt.subplots(figsize=(14, 4)) 
        ax.set_xlabel("Time /s")
        ax.set_ylabel("Amplitude")
        ax.plot(y_harmonic)
        st.pyplot(fig)
        
        st.write("Componente Percurssiva")
        fig, ax = plt.subplots(figsize=(14, 4)) 
        ax.set_xlabel("Time /s")
        ax.set_ylabel("Amplitude")
        ax.plot(y_percussive)
        st.pyplot(fig)
        #root mean square energy
        
        #zero-crossing rate
        
        
        
        st.subheader('Frequency domain')
        
        st.subheader('Time-frequency domain')

        #spectrogram
        st.write("Espetrograma")
        X = librosa.stft(y)
        Xdb = librosa.amplitude_to_db(abs(X))
        fig, ax = plt.subplots(figsize=(14, 5))
        img = librosa.display.specshow(Xdb, sr=fs, x_axis='time', y_axis='hz')
        plt.colorbar(img, ax= ax)
        st.pyplot(fig)
        
        #Spectral centroid
        st.write("Spectral Centroid")
        spectral_centroids = librosa.feature.spectral_centroid(y, sr=fs)[0]
        fig, ax = plt.subplots(figsize=(14, 4)) 
        frames = range(len(spectral_centroids))
        t = librosa.frames_to_time(frames)
        # Normalising the spectral centroid for visualisation
        def normalize(y, axis=0):
            return sklearn.preprocessing.minmax_scale(y, axis=axis)
        #Plotting the Spectral Centroid along the waveform
        librosa.display.waveshow(y, sr=fs, alpha=0.4)
        ax.plot(t, normalize(spectral_centroids), color='b')
        st.pyplot(fig)
    
        #chromagram
        chroma = librosa.feature.chroma_cqt(y=y, sr=fs)
        fig, ax = plt.subplots()
        img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
        ax.set(title='Chromagram demonstration')
        fig.colorbar(img, ax=ax)
        st.pyplot(fig)
    
else:
    with st.container():
        st.info('Welcome to "SoundCloud"!')
        st.info("Click Start to generate a new file.")
    with st.sidebar:
        st.title("About")
        st.info('This project was created as a data logger for recorded sounds that allows real-time visualization, analysis of the signal/features and to save the information to a file. All the source code can be found in https://github.com/tsBatista99/Cloud-logger-AAIB.git')
