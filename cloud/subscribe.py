import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
from pickle import dumps

kafka_producer = KafkaProducer(    
    bootstrap_servers=['kafka : 29092'],
    value_serializer=lambda x: dumps(x))

def on_message(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    kafka_producer.send('analytics', value=message.payload)
    #Store to influxDB

subscribe.callback(on_message, "Gateway/+/temperature", hostname="host.docker.internal")