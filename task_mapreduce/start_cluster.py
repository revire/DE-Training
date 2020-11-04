import docker
import os
import logging
logging.basicConfig(level=logging.INFO)


DIRECTORY = os.path.abspath('out')

client = docker.APIClient()
logging.info('starting')

host_config = client.create_host_config(
    binds={
        DIRECTORY: {
            'bind': '/out',
            'mode': 'rw'
        }
    },
)
container = client.create_container(
    image='docker_test',
    host_config=host_config,
)
logging.info('Building docker')
client.start(container)
logging.info('Running container')
print(client.containers())
exit_code = client.wait(container)

print("Container exited with code {}".format(exit_code))

