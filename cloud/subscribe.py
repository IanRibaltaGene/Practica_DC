import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
from pickle import dumps
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

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

#Tag is the gateway id
def store_to_influxdb(tag, value):
    p = (Point("temperature_mesurement").tag("gateway", tag).field("temperature", value))
    print(f"0----------{tag} {value}")
    write_api.write(bucket=bucket, record=p, org=org)#No conecta :(
    print(f"1----------{tag} {value}")

def on_message(client, userdata, message):
    value, timestamp, sensor = dipack(message.payload)
    kafka_message = {"v": value, "ts": timestamp,"sensor": sensor}
    print("%s %s" % (message.topic, kafka_message))
    kafka_producer.send('analytics', value=kafka_message)
    #Store to influxDB
    store_to_influxdb(sensor, value)

if __name__=="__main__":
    bucket = "dc_practica"
    url = "127.0.0.1:8086"
    token = "ea612f89eb7e81633fc28bffd098897c"
    org = "practica"
    client = InfluxDBClient(url=url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    subscribe.callback(on_message, "Gateway/+/temperature", hostname="host.docker.internal")