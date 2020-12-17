import os
import subprocess
import threading
import time
import sys


def get_input(key):
    input('Press any key to stop: \n')
    key.append(True)


def monitoring(files):
    # files_to_send = sys.argv[1]
    files_to_send = files
    key = []
    monitoring = {'check_output': None, 'check_queue': None}
    input_thread = threading.Thread(target=get_input, args=(key,))
    input_thread.start()
    while (monitoring['check_output'] != 0 and monitoring['check_queue'] != 0) and not key:
        time.sleep(5)
        for function in monitoring.keys():
            monitor_script = f'docker exec rabbit_monitoring_1 python monitoring.py {function} {files_to_send}'.split(
                ' ')
            print(subprocess.check_output(monitor_script).decode('utf-8').strip())
            # monitoring[function] = int(subprocess.check_output(monitor_script).decode('utf-8').strip())
            # print(f'Files not found: {monitoring["check_output"]}.Messages in queue: {monitoring["check_queue"]}')


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

    monitoring(files_to_send)

    print('Starting reducer')
    output_dir = 'output'
    reducer_script = f'docker exec rabbit_sender_1 python sender.py reduce {output_dir}'.split(' ')
    subprocess.call(reducer_script)

    print('Result ready')



