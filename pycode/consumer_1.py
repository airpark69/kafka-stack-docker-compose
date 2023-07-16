from kafka import KafkaConsumer
from json import loads
from time import sleep
import os

# 환경 변수 불러오기
kafka_host = os.environ.get('KAFKA_HOST')

consumer = KafkaConsumer(
   'topic_test',
   bootstrap_servers=['%s:9092' % kafka_host],
   auto_offset_reset='earliest',
   enable_auto_commit=True,
   group_id='my-group-id',
   value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for event in consumer:
   event_data = event.value
   # Do whatever you want
   print(event_data)
   sleep(1)