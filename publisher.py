import paho.mqtt.client as mqtt 
from random import uniform
import time


mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("test/AAIB")
client.connect(mqttBroker, port=1883) 

while True:
    randNumber = uniform(0, 10)
    client.publish("NumberAAIB", randNumber)
    print("Just published " + str(randNumber) + " to topic NumberAAIB")
    time.sleep(0.1)