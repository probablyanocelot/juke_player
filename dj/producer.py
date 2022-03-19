import pika
import json
import os
from dotenv import load_dotenv
load_dotenv('.env')

MQ_HOST = os.getenv('MQ_HOST')
connection_params = pika.ConnectionParameters(heartbeat=10)
params = pika.URLParameters(MQ_HOST)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body, service='player'):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key=service, body=json.dumps(body), properties=properties)
    # print(" [x] Sent %r" % body)
