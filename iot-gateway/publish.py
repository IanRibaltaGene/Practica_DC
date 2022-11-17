import paho.mqtt.publish as publish
from time import sleep
import pandas as pd
import socket

# Read the csv file
data = pd.read_csv('data.csv')
topic = "Gateway/{hostmachine}/temperature".format(hostmachine=socket.gethostname())
i=0
while True:
    publish.single(topic,
                   data.iloc[i%len(data),0],
                   hostname="host.docker.internal")
    sleep(10)
    i+=1
