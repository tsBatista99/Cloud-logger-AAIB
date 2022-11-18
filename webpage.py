import time  # to simulate a real time data, time loop
from streamlit_autorefresh import st_autorefresh

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

start = st.sidebar.checkbox("Update")

if start:
    st_autorefresh(interval=1000, limit=100, key="fizzbuzzcounter")

dataset_url = "dados.txt"

#read csv from a URL

def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url,names=["Data"])

st.markdown("#### Random Data")



df = []

my_file = Path(dataset_url)
if my_file.is_file():
    # file exists
    df=get_data()
    
    # with st.sidebar:
    #     st.write("DATA LOADER")
        
    #     my_bar = st.progress(0)
        
    #     for percent_complete in range(100):
    #         time.sleep(0.01)
    #         my_bar.progress(percent_complete + 1)
            
    #     with st.spinner('Wait for it...'):
    #         time.sleep(1)
            
    #     st.success("Done!")
        
    add_radio = st.sidebar.radio("Choose method",("Fourrier", "Plot"))
        
    add_selectbox = st.sidebar.selectbox(
    "Select operation",
    ("Email", "Home phone", "Mobile phone"))
    
    width = st.sidebar.slider("plot width", 1, 20, 15)
    height = st.sidebar.slider("plot height", 1, 10, 5)
        
    fig, ax = plt.subplots(figsize=(width, height)) 
    plt.subplots(figsize=(width, height)) 
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Data")
    
    ax.plot(df)
    
    plt.show()
    
    st.pyplot(fig)   
    
    
    is_check = st.checkbox("Display Data")
    if is_check:
        st.write(df.T)
        
else:
    st.write("Please generate a new file")

