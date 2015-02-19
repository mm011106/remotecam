#!/usr/bin/env python
#
#
#

import paho.mqtt.client as mqtt
import datetime

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("my/device/stillcam")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # print(msg.topic+" "+str(msg.payload))
    filename = "./image/" + datetime.datetime.today().strftime("%H%M%S%f") + ".jpg"
    outfile=open( filename , 'w')
    outfile.write(msg.payload)
    print "subscribe: " + filename
    outfile.close

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("my.broker.jp", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
