import uuid
import json
from typing import List
from person import Person

from faker import Faker
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaAdminClient
from kafka.producer import KafkaProducer
import os


def create_topic(bootstrap_servers, name, partitions, replica=1):
    client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        topic = NewTopic(
            name=name,
            num_partitions=partitions,
            replication_factor=replica)
        client.create_topics([topic])
    except TopicAlreadyExistsError as e:
        print(e)
        pass
    finally:
        client.close()


def main():
    # 환경 변수 불러오기
    kafka_host = os.environ.get('KAFKA_HOST')
    topic_name = "fake_people"
    bootstrap_servers = ["%s:9092" % kafka_host]

    # create a topic first
    create_topic(bootstrap_servers, topic_name, 4)

    # ingest some random people events
    people: List[Person] = []
    faker = Faker()
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        client_id="Fake_Person_Producer",
        
    )

    for _ in range(100):
        person = Person(id=str(uuid.uuid4()), name=faker.name(), title=faker.job().title())
        people.append(person)
        producer.send(
            topic=topic_name,
            key=person.title.lower().replace(r's+', '-').encode('utf-8'),
            value=person.model_dump_json().encode('utf-8'))

    producer.flush()

if __name__ == '__main__':
    main()