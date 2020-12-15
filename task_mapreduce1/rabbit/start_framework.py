import subprocess
import sys

if __name__ == '__main__':

    path_to_files = sys.argv[1]
    path_script = f'docker exec rabbit_sender_1 python3 sender.py input'.split(' ')
    subprocess.call(path_script)