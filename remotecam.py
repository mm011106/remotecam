#!/usr/bin/env python
#  remotecam.py
#     subscribe command topic and take a picture by a command
#     send (publish) the picture data via mqtt
#
#     ver1.0  2015.02.22 Masakazu Miyamoto mqtt.and@gmail.com

import paho.mqtt.client as mqtt
import os

#
#  Parameters
#
topic_root="ET/TEST/DEVICE"
topic_command="/command"
topic_pub="/PICTURE"

broker="localhost"
mqtt_port="22883"

shoot_command="shoot"


#
#
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe(topic_root+topic_command)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = str(msg.payload)
#   print(msg.topic+" "+str(msg.payload))
    if cmd == shoot_command :
        print "Say cheeees!"

	dummy = os.system("fswebcam -r 800x600 --quiet /run/shm/temp.jpg")
#        dummy = os.system("raspistill -w 1024 -h 768 -t 10 -o /run/shm/temp.jpg")
        dummy = os.system("mosquitto_pub -p "+mqtt_port+" -h "+broker+" -t "+topic_root+topic_pub+" -f /run/shm/temp.jpg")
        print(" picture was published....")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect( broker , mqtt_port , 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
