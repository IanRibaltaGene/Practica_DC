from kafka import KafkaConsumer
from pickle import loads
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "dc_practica"
url = "127.0.0.1:8086"
token = "ea612f89eb7e81633fc28bffd098897c"
org = "practica"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def store_to_influxdb(tag, value):
    p = Point("analytic").tag("gateway", tag).field("temperature", value)
    write_api.write(bucket=bucket, record=p)

kafka_consumer = KafkaConsumer(
    'analytics_results',
    bootstrap_servers=['kafka : 29092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='cloud-group',
    value_deserializer=lambda x: loads(x)
    )

for data in kafka_consumer:
    print(f"{data} is being stored")
    to_store=data.value
    print(f"{to_store}")
    ##Store to influxdb
    # store_to_influxdb(to_store)
    # p = Point("measurement").tag("user", tag).field("temperature", to_store)
    # write_api.write(bucket=bucket, record=p)