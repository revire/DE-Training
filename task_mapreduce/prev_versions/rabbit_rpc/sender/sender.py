import pika
import os
import sys
import logging
import uuid

QUEUE_NAME = os.environ['queue_name']

def get_files(dir):
    files = os.listdir(dir)
    return files

class Sender(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=300,
                                                                   blocked_connection_timeout=150,
                                                                   ))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, file):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=file)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == '__main__':
    print(' [x] Starting Sender')
    files_got = sys.argv[1]
    files = files_got.split(';')
    sender = Sender()
    for file in files:
        response = sender.call(file)