import pika
import os
import sys
import logging
import time

logging.basicConfig(level=logging.WARN)

INPUT_DIR = 'input'

def get_files(dir):
    files = os.listdir(dir)
    return files

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=600,
                                                                   blocked_connection_timeout=300,
                                                                   ))
    channel = connection.channel()

    channel.queue_declare(queue='bytes',
                          # durable=True
                          )


    message = os.environ['message']
    number_of_containers = os.environ['number_of_containers']

    files = get_files(INPUT_DIR)

    for file in files:
        channel.basic_publish(exchange='',
                              routing_key='bytes',
                              body=file,
                              # properties=pika.BasicProperties(delivery_mode = 2,),
                              )
        print(f" [x] Sent file {file}")
    # print(' [*] Waiting for messages to sent. To exit press CTRL+C')
    connection.close()


# if __name__ == '__main__':
#     print(' [x] Waiting for a start 3 s')
#     time.sleep(3)
#     logging.info(' [x] Starting Sender')
#
#
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)



print(' [x] Waiting for a start 3 s')
time.sleep(15)
main()