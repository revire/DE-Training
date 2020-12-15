
import docker
import sys
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
client = docker.APIClient()
logging.info('Starting')


def generate_yml(number_of_containers):
    containers_string = []
    rabbit_yml = f"""
version: '3'

networks:
    net:

services:

  rabbit:
    image: rabbitmq:3-alpine
    container_name: rabbit
    networks:
      - net
    ports:
      - '5672:5672'

  sender:
    build:
      context: ./sender
      dockerfile: Dockerfile
    tty: true
    networks:
      - net
    volumes:
       - ./output:/output
       - ./input:/input
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
   # deploy:
   #     resources:
   #        limits:
   #          cpus:'1.0'
   #          memory:1G
   volumes:
     - ./output:/output
     - ./input:/input
   networks:
     - net
   restart: always
   depends_on:
     - rabbit
        """
        containers_string.append(container)

    for container in containers_string:
        rabbit_yml = rabbit_yml + container

    return rabbit_yml


if __name__ == '__main__':
    number_of_containers = int(sys.argv[1])
    rabbit_yml = generate_yml(number_of_containers)

    with open('rabbit.yml', 'w') as y:
        y.write(rabbit_yml)

    yml_script = 'docker-compose -f rabbit.yml up --build'.split(' ')
    subprocess.call(yml_script)


