import paho.mqtt.client as mqtt 
import time
import pyaudio

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

client = mqtt.Client("test/AAIB")
client.connect(mqttBroker, port=1883) 
client.on_connect= on_connect


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20 #Tempo de aquisição


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    client.publish("AAIB", data)
    #print("Just published " + str(data) + " to topic AAIB")
    time.sleep(1/RATE)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
disconnect()