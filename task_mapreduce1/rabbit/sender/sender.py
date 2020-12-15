import pika
import os
import sys
import time



def get_files(dir):
    files = os.listdir(dir)
    return files

def main(path_to_files):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=600,
                                                                   blocked_connection_timeout=300,
                                                                   ))
    channel = connection.channel()
    files = get_files(path_to_files)

    for file in files:
        channel.basic_publish(exchange='',
                              routing_key='och',
                              body=file,
                              properties=pika.BasicProperties(delivery_mode = 2,),
                              )
        print(f" [x] Sent file {file}")

    connection.close()


if __name__ == '__main__':
    print(' [x] Starting Sender')
    path_to_files = sys.argv[1]
    # print(path_to_files)
    # os.listdir()
    main(path_to_files)





