import pika
import os
import logging

logging.basicConfig(level=logging.INFO)

# network = os.environ['networks']


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()


channel.queue_declare(queue='hello')


message = os.environ['message']

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
logging.info(f" [x] Sent {message}")


connection.close()