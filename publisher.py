import paho.mqtt.client as mqtt 
from random import uniform
import time

mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("test/AAIB")
client.connect(mqttBroker, port=1883) 

randNumber = uniform(20.0, 21.0)
client.publish("Number", randNumber)
print("Just published " + str(randNumber) + " to topic Random")
time.sleep(1)