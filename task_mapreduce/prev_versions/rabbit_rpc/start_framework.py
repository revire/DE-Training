import os
import subprocess
import threading
import time
import sys


def get_files(dir):
    files = os.listdir(dir)
    return files


if __name__ == '__main__':

    path_to_files = sys.argv[1]
    # files = get_files(path_to_files)
    files = ['input_file_2019-11-01T15:55:49.425673.bin.gz']

    files_to_send = ';'.join(files)

    print('Starting mapper')
    mapper_script = f'docker exec rabbit_sender_1 python sender.py map {files_to_send}'.split(' ')
    subprocess.call(mapper_script)




