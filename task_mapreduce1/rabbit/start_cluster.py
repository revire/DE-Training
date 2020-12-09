
import docker
import os
import logging
import json
import subprocess

logging.basicConfig(level=logging.INFO)
#
# INPUT_DIR = os.path.abspath('input_files_test')
# OUTPUT_DIR = os.path.abspath('out')

client = docker.APIClient()
logging.info('Starting')



def generate_yml(number_of_containers):
    containers_string = []
    yml = f"""
version: '3'

networks:
    net:

services:

  rabbit:
    image: rabbitmq:3-alpine
    container_name: rabbit
    # logging:
    #   driver: none
    networks:
      - net
    ports:
      - '5672:5672'


  
  sender:
    environment:
      - message=white rabbit
      - number_of_containers={number_of_containers}
    build:
      context: ./sender
      dockerfile: Dockerfile
    networks:
      - net
    volumes:
       - ./output:/output
       - ./input_files_test:/input
    # restart: always
    depends_on:
      - rabbit

                    """
    for n in range(number_of_containers):
        container = f"""
  worker{n}:
   environment:
     - file=output_file{n}
   build:
     context: ./receiver
     dockerfile: Dockerfile
   # limits:
   #   cpus:'1.0'
   #   memory:1G
   volumes:
     - ./output:/output
     - ./input_files_test:/input
   networks:
     - net
   restart: always
   depends_on:
     - rabbit
        """
        containers_string.append(container)


    for container in containers_string:
        yml = yml + container

    return(yml)





if __name__ == '__main__':
    yml = generate_yml(2)
    with open('rabbit.yml', 'w') as y:
        y.write(yml)

    yml_script = 'docker-compose -f rabbit.yml up --build'.split(' ')

    subprocess.call(yml_script)


