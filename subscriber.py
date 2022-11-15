import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="test.mosquitto.org"

client = mqtt.Client("test/AAIB")
client.connect(mqttBroker, port=1883) 

client.loop_start()

client.subscribe("Number")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()