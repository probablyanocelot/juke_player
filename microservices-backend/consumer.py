import pika
# from dotenv import load_dotenv
import os

params = pika.URLParameters(
    'amqps://kdftyeer:lPZn0W5W3DzL0scgXcXnAD8nz7ISAilj@hornet.rmq.cloudamqp.com/kdftyeer?heartbeat=0')

# params = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=pika.credentials.PlainCredentials(
#     MQ_USER, MQ_PASSWD), heartbeat_interval=0)
# conn = pika.BlockingConnection(parameters=params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='tutorial')


def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)


channel.basic_consume(
    queue='tutorial', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
