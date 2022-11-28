import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
from pickle import dumps
from datetime import datetime

kafka_producer = KafkaProducer(    
    bootstrap_servers=['kafka : 29092'],
    value_serializer=lambda x: dumps(x)
)

def dipack(message):
    print(message)
    message = message.decode('utf-8')
    print(message)
    message_list = message.split("~~~~~")
    print(message_list)
    value = float(message_list[0])
    print(value)
    timestamp = datetime.strptime(message_list[1], '%Y-%m-%d %H:%M:%S.%f')
    print(timestamp)
    sensor = message_list[2]
    print(sensor)
    return value, timestamp, sensor

def on_message(client, userdata, message):
    value, timestamp, sensor = dipack(message.payload)
    kafka_message = {"v": value, "ts": timestamp,"sensor": sensor}
    print("%s %s" % (message.topic, kafka_message))
    kafka_producer.send('analytics', value=kafka_message)
    #Store to influxDB

subscribe.callback(on_message, "Gateway/+/temperature", hostname="host.docker.internal")