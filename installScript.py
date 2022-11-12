# -*- coding: utf-8 -*-
"""
Script to install packages
"""
##To install streamlit
pip3 install streamlit
##To install MQTT service
apt install -y mosquitto
apt install mosquitto-clients
service mosquitto start
service mosquitto status
##To install Paho-MQTT
pip3 install paho-mqtt
git clone https://github.com/eclipse/paho.mqtt.python.git
cd paho.mqtt.python
python setup.py install
