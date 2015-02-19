#!/usr/bin/env python
#
#sub_camdata.py
#  subscribe photo data from a broker
#  2015/02/19 Masakazu Miyamoto
#

import paho.mqtt.client as mqtt
import datetime

#  the topic where the picture data sent to
topic_of_data="my/device/sitllcam"

#  the path to where the subscribed data is stored
path_to_storage="/home/me/image/"

# Parameters for connecting broker 
my_broker="my_broker.jp"
mqtt_port="1883"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe( topic_of_data )

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # print(msg.topic+" "+str(msg.payload))
    # filename is generated based on the time of receiveing
    # the file type is expected to be .JPG
    filename = path_to_storage + datetime.datetime.today().strftime("%H%M%S%f") + ".jpg"
    outfile = open( filename , 'w')
    outfile.write(msg.payload)
    print "subscribe: " + filename
    outfile.close

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect( my_broker , mqtt_port , 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
