#!/usr/bin/env python
import os
import pika
import sys
import logging
from functools import partial
from collections import Counter
import json

# logging.basicConfig(level=logging.INFO)
import re
import gzip

# logging.basicConfig(level=logging.INFO)

# file = message = os.environ['file']

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def count_bytes(file):
    bytes = {0: 0, 1: 0}
    try:
        with gzip.open(os.path.join(INPUT_DIR, file), 'rb') as input_file:
            read_block = partial(input_file.read, 256)
            # start = time()
            counter = Counter(byte for block in iter(read_block, b"") for byte in block)
            print('Collected counters')
            for byte, count in counter.items():
                print(byte, f"{byte:08b}")
                ones = sum(int(bit) for bit in f"{byte:08b}")
                bytes[0] += count * (8 - ones)
                bytes[1] += count * ones
            # delta = time() - start
    except Exception:
        print('Failed to open')
        logging.warning(f'Failed to open {file}')
    print(bytes)
    # print(delta)
    return bytes

def write_bytes(ans, file):
    print(file)
    try:
        with open(os.path.join(OUTPUT_DIR, file), 'w') as output_file:
            json.dump(ans, output_file)
    except Exception:
        print('Failed to write')
        logging.warning(f'Failed to write')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='count_bytes')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        file = body.decode('utf-8')

        output_file = f"{file.split('.bin')[0]}.txt"
        print(f" [x] Starting {body}")
        ans = count_bytes(file)
        print(f" [x] Writing {body}")
        write_bytes(ans, output_file)
        print(' [x] Counted bytes and wrote to json')


    channel.basic_consume(queue='count_bytes', on_message_callback=callback, auto_ack=True)
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

