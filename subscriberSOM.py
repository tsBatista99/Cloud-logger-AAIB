import paho.mqtt.client as mqtt
import time
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
frames = []

def on_message(client, userdata, message):
    data = message.payload
    frames.append(data)
    

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print("Connection failed")
    
def disconnect():
    print("client is disconnecting..")
    client.disconnect()

Connected = False   #global variable for the state of the connection
mqttBroker ="test.mosquitto.org"

client = mqtt.Client("Gitpod")
client.connect(mqttBroker, port=1883) 
client.on_connect= on_connect

client.loop_start()

client.subscribe("AAIB")


client.on_message=on_message 

time.sleep(30) #colocar 10 minutos de aquisição
client.loop_stop()

with wave.open("sound1.wav", "w") as wf:
         wf.setnchannels(CHANNELS)
         wf.setsampwidth(p.get_sample_size(FORMAT))
         wf.setframerate(RATE)
         wf.writeframes(b''.join(frames))
         print("Sound file saved.")
         
disconnect()

