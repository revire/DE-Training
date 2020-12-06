
import docker
import os
import logging
import json
import subprocess

logging.basicConfig(level=logging.INFO)

INPUT_DIR = os.path.abspath('input_files_test')
OUTPUT_DIR = os.path.abspath('out')

client = docker.APIClient()
logging.info('Starting')


def generate_yml(number_of_containers):
    containers_string = []
    for n in range(number_of_containers):
        container = f"""
            hello{n}:
                environment:
                  - file=hello{n}
                build:
                  context: .
                  dockerfile: Dockerfile
                volumes:
                  - ./output:/output
        """
        containers_string.append(container)
    yml = f"""
        version: '3'
        services:
            """

    for container in containers_string:
        yml = yml + container

    return(yml)

if __name__ == '__main__':
    # yml = generate_yml(2)
    # with open('rabbit.yml', 'w') as y:
    #     y.write(yml)
    sender_script = 'docker build --tag sender_docker ./sender'.split(' ')
    receiver_script = 'docker build --tag receiver_docker ./receiver'.split(' ')
    yml_script = 'docker-compose -f rabbit.yml up --build'.split(' ')
    # subprocess.call(sender_script)
    # subprocess.call(receiver_script)
    subprocess.call(yml_script)


