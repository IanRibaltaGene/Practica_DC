# How to use the analytics module

### Folder structure

analitics_module/
├─ consumer.py # python script that runs the consumer
├─ Dockerfile # The file to build the docker
├─ requirements.txt # The file containing the python requirements
├─ model_trained.pkl # The previously trained model provided
├─ README.md # This readme file

### Module requirements

Inside code inside `consumer.py` will be run in the docker take a look.

The container runs the following simple steps:

1. Listens from a kafka topic `analytics`
2. Processes the message by running the model on the data provided
3. Writes the response to the topic `analytics_results`

### Message contents
The expected message must be serialized using pickle, because it allows the serialization of complex objects like datetime.
JSON serialization does not allow this type of serialization unless transformed.

The message transferred must be a python dictionary object with the following information and datatype: 
```
    {"v": <value-float>, "ts": <time-datetime>, "sensor": <sensorid-string>}
```
When creating the kafka producer and consumer, you must use the pickle serialization. 

```python
from pickle import loads, dumps
from kafka import KafkaConsumer, KafkaProducer

# producer
my_producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: dumps(x)
)
# consumer
y_consumer = KafkaConsumer(
    '<topic-to-consume>',
    bootstrap_servers=['kafka : 9092'],
    auto_offset_reset='latest',
    group_id='analytics-group',
    value_deserializer=lambda x: loads(x)
)
```