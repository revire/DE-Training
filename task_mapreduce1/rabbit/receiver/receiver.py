import os
import pika
import sys
import logging
from functools import partial
from collections import Counter
import json
import gzip

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def count_bytes(file):
    bytes = {0: 0, 1: 0}
    try:
        with gzip.open(os.path.join(INPUT_DIR, file), 'rb') as input_file:
            read_block = partial(input_file.read, 256)
            counter = Counter(byte for block in iter(read_block, b"") for byte in block)
            print('Collecting bytes')
            for byte, count in counter.items():
                ones = sum(int(bit) for bit in f"{byte:08b}")
                bytes[0] += count * (8 - ones)
                bytes[1] += count * ones
    except Exception:
        print('Failed to open')
        logging.warning(f'Failed to open {file}')
    print(bytes)
    return bytes


def reduce(output_dir):
    bytes = {0: 0, 1: 0}
    output = None
    files = os.listdir(output_dir)
    for file in files:
        with open(os.path.join(output_dir, file), 'r') as f:
            try:
                output = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                pass
            bytes[0] += output['0']
            bytes[1] += output['1']
    print(bytes)
    with open(os.path.join(output_dir, 'result.txt'), 'w') as res:
        json.dump(bytes, res)


def write_bytes(ans, file):
    print(f'Writing file {file}')
    try:
        with open(os.path.join(OUTPUT_DIR, file), 'w') as output_file:
            json.dump(ans, output_file)
    except Exception:
        print('Failed to write')
        print(Exception)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit',
                                                                   heartbeat=300,
                                                                   blocked_connection_timeout=150,
                                                                   ))
    channel = connection.channel()
    channel.queue_declare(queue='och', durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        message = body.decode('utf-8')
        print(message)
        function = message.split(';')[0]
        input = message.split(';')[1]
        if function == 'map':
            output_file = f"{input.split('.bin')[0]}.txt"
            ans = count_bytes(input)
            print(f" [x] Writing {body}")
            write_bytes(ans, output_file)
            print(' [x] Counted bytes and wrote to json')
        elif function == 'reduce':
            reduce(input)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='och', on_message_callback=callback)
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





