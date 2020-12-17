import sys
import time
import os
import pika
import threading

QUEUE_NAME = os.environ['queue_name']

try:
    INPUT_FILES = sys.argv[2]
except IndexError:
    INPUT_FILES = ''


def get_files(dir):
    files = os.listdir(dir)
    return files


def check_output(files=INPUT_FILES):
    path_to_output_files = 'output'
    files_input = list(map(lambda x: x.split('.bin')[0], files.split(';')))
    files_output = list(map(lambda x: x.split('.txt')[0], os.listdir(path_to_output_files)))
    not_preceeded = [file for file in files_input if file not in (files_output)]
    print(not_preceeded, files_output)
    result = len(not_preceeded)
    return result



def check_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=600,
                                                                   blocked_connection_timeout=300,
                                                                   ))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    queue = channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
        passive=True
    )
    queue_len = queue.method.message_count
    connection.close()
    return queue_len




def purge_queue():
    print('Purging')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                  heartbeat=600,
                                                                  blocked_connection_timeout=300,
                                                                  ))
    channel = connection.channel()
    channel.queue_purge(QUEUE_NAME)
    channel.close()

def check_all():
    pass


if __name__ == '__main__':
    functions = {'purge_queue': purge_queue,
                 'check_queue': check_queue,
                 'check_output': check_output,
                 'check_all':check_all}
    function = functions[sys.argv[1]]
    result = function()
    print(result)


