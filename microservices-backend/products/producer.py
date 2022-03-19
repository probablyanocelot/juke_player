import pika
import json

params = pika.URLParameters(
    'amqps://kdftyeer:lPZn0W5W3DzL0scgXcXnAD8nz7ISAilj@hornet.rmq.cloudamqp.com/kdftyeer')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='tutorial-flask', body=json.dumps(body), properties=properties)
    # print(" [x] Sent %r" % body)
