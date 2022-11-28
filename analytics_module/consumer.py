from pickle import loads, load, dumps
from kafka import KafkaConsumer, KafkaProducer
import pandas as pd

my_consumer = KafkaConsumer(
    'analytics',
    bootstrap_servers=['kafka : 29092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='analytics-group',
    value_deserializer=lambda x: loads(x)
)
my_producer = KafkaProducer(
    bootstrap_servers=['kafka:29092'],
    value_serializer=lambda x: dumps(x)
    )
m = load(open("model_trained.pkl", "rb"))
print("starting")
for message in my_consumer:
    print(f"{message} is being processed")
    message = message.value
    df_pred = pd.DataFrame.from_records([{"ds": message['ts']}])
    forecast = m.predict(df_pred)
    forecast['sensor'] = message['sensor']
    my_producer.send('analytics_results',
                     value=forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'sensor']].to_dict(orient="records"))
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'sensor']])
