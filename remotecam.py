#!/usr/bin/env python
#
#

import paho.mqtt.client as mqtt
import os

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("my/device/stillcam/command")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = str(msg.payload)
    print(msg.topic+" "+str(msg.payload))
    if cmd == "shoot":
        print "Say cheeees!"

        dummy = os.system("raspistill -w 1024 -h 768 -t 10 -o /run/shm/temp.jpg")
        dummy = os.system("mosquitto_pub -h my.broker.jp -t my/device/stillcam -f /run/shm/temp.jpg")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("my.broker.jp", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
