# -*- coding: utf-8 -*-
"""
Script to install packages
"""
##To install streamlit
sudo pip3 install streamlit
##To install MQTT service
sudo apt install -y mosquitto
sudo apt install mosquitto-clients
sudo service mosquitto start
sudo service mosquitto status
##To install Paho-MQTT
sudo pip3 install paho-mqtt
git clone https://github.com/eclipse/paho.mqtt.python.git
cd paho.mqtt.python
python setup.py install
