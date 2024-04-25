from src.db_connection import DBConnection
import pandas as pd
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer

import numpy as np

import os
import signal
import subprocess
import sys

host = 'kafka:9092'
# host = 'localhost:9092'


class MyKafkaConsumer:
    def __init__(self, topic, messages_count=-1):
        print("Starting Consumer...")
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=host,
            enable_auto_commit=True,
            auto_offset_reset='earliest',
            group_id='my-group',
            consumer_timeout_ms=100000,
        )
        self.connection = DBConnection()
        self.listen(messages_count)
        self.close()

    def listen(self, messages_count):
        print("Listening")
        while messages_count > 0:
            msg = self.consumer.poll()
            if msg is None or len(msg) == 0:
                continue
            for partition, messages in msg.items():
                print("OFFSETS: ", self.consumer.end_offsets([partition]))
                for i, message in enumerate(messages):
                    if message.offset < self.consumer.end_offsets([partition])[partition] - 1:
                        continue
                    print("Writing to db...")
                    self.connection.append_df(pd.DataFrame(data={"y_real": json.loads(message.value)}), self.topic)
                    messages_count -= 1

    def close(self):
        self.connection.close()
        self.consumer.close()


class MyKafkaProducer:
    def __init__(self):
        print("Starting Producer...")
        self.producer = KafkaProducer(
            bootstrap_servers=[host],
            value_serializer=self.serializer,
        )

    # Messages will be serialized as JSON
    def serializer(self, message):
        return json.dumps(message).encode('utf-8')

    def send(self, topic, message):
        print('Producer sending...')
        self.producer.send(topic, message)
        print('Producer sent.')

    def close(self):
        self.producer.flush()
        self.producer.close()


class KafkaSingleConnection:
    def __init__(self, topic, messages):
        code = 'import sys;from src.kafka_connection import MyKafkaConsumer; MyKafkaConsumer(str(sys.argv[1]), int(sys.argv[2]))'
        cmd = ['python', '-c', code, topic, str(messages)]
        self.p = subprocess.Popen(cmd)

        self.producer = MyKafkaProducer()
        self.topic = topic

    def send(self, message):
        self.producer.send(self.topic, message)

    def close(self, timeout_s=10):
        print("Closing")
        try:
            self.p.wait(timeout_s)
        except subprocess.TimeoutExpired:
            print("TimeoutExpired, Stopping consumer")
            self.p.kill()
        self.producer.close()


if __name__ == '__main__':
    print("STARTING")
    print(np.arange(6).tolist())
    topic = 'test' + str(np.random.randint(12304))
    messages = 5
    conn = KafkaSingleConnection(topic, messages)

    for i in range(messages):
        conn.send(np.arange(6).tolist())
    conn.close()

    connection = DBConnection()
    print(connection.get_df(topic))
    connection.close()

