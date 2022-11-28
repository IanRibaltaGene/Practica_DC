from kafka import KafkaConsumer
from pickle import loads

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
    ##Store to influxdb
    # p = Point("measurement").tag("user", tag).field("temperature", to_store)
    # write_api.write(bucket=bucket, record=p)