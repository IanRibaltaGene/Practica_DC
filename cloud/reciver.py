from kafka import KafkaConsumer
from pickle import loads
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "dc_practica"
url = "http://database:8086"
token = "ea612f89eb7e81633fc28bffd098897c"
org = "practica"

from influxdb_client.domain.write_precision import WritePrecision
def store_to_influxdb(value, write_api, timestamp):
    tag = value["sensor"]

    p_yhat = Point("analytic").tag("gateway", tag).field("yhat", value["yhat"]).time(timestamp,WritePrecision.MS)
    p_yhat_lower = Point("analytic").tag("gateway", tag).field("yhat_lower", value["yhat_lower"]).time(timestamp,WritePrecision.MS)
    p_yhat_upper = Point("analytic").tag("gateway", tag).field("yhat_upper", value["yhat_upper"]).time(timestamp,WritePrecision.MS)

    write_api.write(bucket=bucket, record=[p_yhat, p_yhat_lower, p_yhat_upper])
    print(f"gateway={tag} stored={value} on bucket={bucket}")

def create_client():
    clientInflux = InfluxDBClient(url=url, token=token, org=org)
    print("Client created")
    write_api = clientInflux.write_api(write_options=SYNCHRONOUS)
    return write_api, clientInflux

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
    to_store=data.value[0]
    print(f"{to_store}")
    ##Store to influxdb
    write_api, client_influx = create_client()
    store_to_influxdb(to_store, write_api, data.timestamp)
    client_influx.close()
    print("client closed")