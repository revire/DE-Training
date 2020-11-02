import docker
import logging

logging.basicConfig(level=logging.INFO)
client = docker.from_env()
logging.info('starting')
client.images.build(path="./", tag='docker_test')
logging.info('Building docker')
var = print(client.containers.run("docker_test", ""))
print(var, type(var))
logging.info('Running container')
print(client.containers.list())