import os
import logging
from functools import partial
from collections import Counter
from time import time
import json

logging.basicConfig(level=logging.INFO)
import re
import gzip

INPUT_DIR = 'input_files_test'
OUTPUT_DIR = 'out'


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


if __name__ == '__main__':
    logging.info('Started docker')

    #uncomment if you run docker
    file = os.environ['INPUT_FILENAME']

    #uncomment if you pyhton script only
    #file = os.listdir(INPUT_DIR)[0]

    output_file = f"{file.split('.bin')[0]}.txt"
    ans = count_bytes(file)
    write_bytes(ans, output_file)
    logging.info('Bytes count written to json')
