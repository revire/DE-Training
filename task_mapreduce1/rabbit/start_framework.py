
import docker
import os
import logging
import json
import subprocess
import sys

if __name__ == '__main__':

    n_of_containers=5
    for n in range(n_of_containers):
        add_path_script = f'docker cp worker{n}:{sys.argv[0]} input_test_files|-'.split(' ')
        subprocess.call(add_path_script)