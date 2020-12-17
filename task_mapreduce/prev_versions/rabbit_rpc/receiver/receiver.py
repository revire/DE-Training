#!/usr/bin/env python
import os
import pika
import logging
from functools import partial
from collections import Counter
import json

# logging.basicConfig(level=logging.INFO)

import gzip

logging.basicConfig(level=logging.INFO)


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'



connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=300,
                                                                   blocked_connection_timeout=150,
                                                                   ))

channel = connection.channel()

channel.queue_declare(queue='test')

def count_bytes(file):
    bytes = {0: 0, 1: 0}
    try:
        with gzip.open(os.path.join(INPUT_DIR, file), 'rb') as input_file:
            read_block = partial(input_file.read, 256)
            counter = Counter(byte for block in iter(read_block, b"") for byte in block)
            print('Collected counters')
            for byte, count in counter.items():
                print(byte, f"{byte:08b}")
                ones = sum(int(bit) for bit in f"{byte:08b}")
                bytes[0] += count * (8 - ones)
                bytes[1] += count * ones
    except Exception:
        print('Failed to open')
        logging.warning(f'Failed to open {file}')
    print(bytes)
    return bytes


def reduce(files):
    bytes = {0: 0, 1: 0}
    for file in files:
        with open(os.path.join(OUTPUT_DIR, file), 'r') as f:
            try:
                output = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                pass
            print(output['0'])
            bytes[0] += output['0']
            bytes[1] += output['1']
    print(bytes)
    with open(os.path.join(OUTPUT_DIR, '../result.txt'), 'w') as res:
        json.dump(bytes, res)


def write_bytes(ans, file):
    print(f'Writing file {file}')
    try:
        with open(os.path.join(OUTPUT_DIR, file), 'w') as output_file:
            json.dump(ans, output_file)
    except Exception:
        print('Failed to write')
        print(Exception)


def on_request(ch, method, props, body):
    file = body.decode('utf-8')

    print(f"Counting {file}")
    response = count_bytes(file)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()