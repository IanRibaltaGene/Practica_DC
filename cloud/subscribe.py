import paho.mqtt.subscribe as subscribe
from time import sleep

def on_message(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

try:
    subscribe.callback(on_message, "Gateway/+/temperature", hostname="host.docker.internal")
except: ##If not able to subscribe, wait for broker and retry
    sleep(2)
    subscribe.callback(on_message, "Gateway/+/temperature", hostname="host.docker.internal")