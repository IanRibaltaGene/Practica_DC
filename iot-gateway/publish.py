import paho.mqtt.publish as publish
from time import sleep
import pandas as pd

# Read the csv file
data = pd.read_csv('data.csv')
i=0
while True:
    publish.single(f"Gateway/temperature",
                   data.iloc[i%len(data),0],
                   hostname="host.docker.internal")
    sleep(10)
    i+=1
