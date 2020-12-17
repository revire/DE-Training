import pika
import os
import sys

QUEUE_NAME = os.environ['queue_name']


def send_to_workers(function, files, queue_name=QUEUE_NAME):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=600,
                                                                   blocked_connection_timeout=300,
                                                                   ))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue=queue_name, durable=True)

    for file in files:
        message = ';'.join([function, file])
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message,
                              properties=pika.BasicProperties(delivery_mode = 2,),
                              )
        print(f" [x] Sent file {file}")
    connection.close()


if __name__ == '__main__':
    print(' [x] Starting Sender')
    function = sys.argv[1]
    files_got = sys.argv[2]
    files = files_got.split(';')
    send_to_workers(function, files)








