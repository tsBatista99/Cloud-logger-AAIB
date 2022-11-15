import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("Random")
client.connect(mqttBroker) 

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("Number", randNumber)
    print("Just published " + str(randNumber) + " to topic Random")
    time.sleep(1)