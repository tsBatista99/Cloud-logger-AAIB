import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
from pathlib import Path


    

st.set_page_config(
 page_title='Random Data',
 layout="centered",
 initial_sidebar_state="auto",
)

#read txt from a URL

def get_data():
    with open("dados.txt","r") as f:
        last_line = f.readlines()[-1]
        return float(last_line[:-1])

st.markdown("<h1 style='text-align: center; color: white; padding:20px'>SoundCloud</h1>", unsafe_allow_html=True)



my_file = Path("dados.txt")
if my_file.is_file():
    # file exists

    
    # with st.sidebar:
    #     st.write("DATA LOADER")
        
    #     my_bar = st.progress(0)
        
    #     for percent_complete in range(100):
    #         time.sleep(0.01)
    #         my_bar.progress(percent_complete + 1)
            
    #     with st.spinner('Wait for it...'):
    #         time.sleep(1)
            
    #     st.success("Done!")
        
    radio = st.sidebar.radio("Choose method",("Real-time Plot", "Sonogram","Features"))
        
    selectbox = st.sidebar.selectbox(
    "Select operation",
    ("Stream", "Open", "Save"))
    
    if selectbox == "Save":
        if 'data' not in st.session_state:
            st.write("Please generate data")
        else:
            with st.sidebar:
                with st.spinner('Wait for it...'):
                    time.sleep(0.5)
                np.savetxt(r'C:/Users/tbati/Downloads/data.txt', st.session_state['data'].values, fmt='%f', delimiter='\t')
                
                st.success("Done!")
    
    if radio == "Real-time Plot":
        col1, col2, col3, col4, col5,col6 = st.columns(6)
        with col1:
            if st.button('Start'):
                start = True
        with col2: 
            if st.button('Stop'):
                start = False
                #del st.session_state['data']
        
        
        # Initialization
        if 'data' not in st.session_state:
                
            seconds = 0
        
            df = pd.DataFrame({"data": []})
            
            plot = st.line_chart(data=None,width=15,height=5)
               
            for seconds in range(50):
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
    
    if radio == "Sonogram":
        width = st.sidebar.slider("plot width", 1, 20, 15)
        height = st.sidebar.slider("plot height", 1, 10, 5)
        
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
    
    if radio == "Fourrier":
        st.write("Hello")
        
        
    
else:
    st.write("Please generate a new file")

