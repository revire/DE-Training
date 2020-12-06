#!/usr/bin/env python
import os
import pika
import sys
import logging

logging.basicConfig(level=logging.INFO)

file = message = os.environ['file']

print(os.listdir())


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    def callback(ch, method, properties, body):
        logging.info(f" [x] Received {body}")
        with open(f'output/{file}', 'w') as f:
            f.write(body.decode('utf-8'))
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    logging.info('Started receiver')
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)