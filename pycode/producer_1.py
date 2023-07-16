from time import sleep
from json import dumps
from kafka import KafkaProducer
import os

# 환경 변수 불러오기
kafka_host = os.environ.get('KAFKA_HOST')

producer = KafkaProducer(
   bootstrap_servers=['%s:9092' % kafka_host],
   value_serializer=lambda x: dumps(x).encode('utf-8'),
   max_block_ms=600000,
   request_timeout_ms=600000
)

for j in range(100):
   print("Iteration", j)
   data = {'counter': j}
   producer.send('topic_test', value=data)
   sleep(0.5)