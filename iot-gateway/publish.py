import paho.mqtt.publish as publish
from time import sleep
import pandas as pd
import socket
from datetime import datetime

# Read the csv file
data = pd.read_csv('data.csv')
hostmachine=socket.gethostname()
topic = "Gateway/{hostmachine}/temperature".format(hostmachine=hostmachine)
i=0
while True:
    publish.single(topic=topic,
                   payload= f"{float(data.iloc[i%len(data),0])}~~~~~{datetime.now()}~~~~~{hostmachine}",
                   hostname="host.docker.internal")
    sleep(10)
    i+=1
