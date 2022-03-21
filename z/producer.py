import pika
import json
from dotenv import load_dotenv
load_dotenv('.env')

MQ_HOST = os.getenv('MQ_HOST')

params = pika.URLParameters(MQ_HOST)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='tutorial-flask', body=json.dumps(body), properties=properties)
    # print(" [x] Sent %r" % body)
