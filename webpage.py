import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
from pathlib import Path


    

st.set_page_config(
 page_title='SoundCloud',
 layout="centered",
 initial_sidebar_state="auto",
)



#read txt from a URL

def get_data():
    with open("dados.txt","r") as f:
        last_line = f.readlines()[-1]
        return float(last_line[:-1])

st.markdown("<h1 style='text-align: center; color: white; padding:20px'>SoundCloud</h1>", unsafe_allow_html=True)


      

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white; padding:10px'>Sidebar</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button('Start'):
            st.session_state["start"] = True




my_file = Path("dados.txt")
if my_file.is_file() and 'start' in st.session_state:
    # file exists
   
    with st.sidebar:

        col1, col2, col3, col4 = st.columns(4)
        
        with col1: 
            if st.button('Stop'):
                st.session_state["start"] = False
           
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
        st.write("Hello")
        
        
    
else:
    with st.container():
        st.info("Please generate a new file")
 

