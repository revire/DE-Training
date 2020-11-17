'''Домашнее задание
предоставить 2 скрипта, выполняющие следующую работу
1) первый делает поднятие 5ти (можно больше, в идеале параметр должен быть конфигурируемым)
виртуальных машинок (докер контейнеров), объединённх в сеть. Для машинок обязательно ограничение по памяти - 1Gb
2) второй принимает в качестве аргумента путь до папки с .gz файлами.
Он должен запускать job-у с нашим самонаписанным фреймворком на поднятом в пункте 1 кластере

На кластере должен работать самонаписанный фреймворк, который посчитает количество ненулевых байт в входных данных.
Входные данные представляют из себя сжатые gzip-ом бинарные файлы разного размера

При написании map reduce велосипеда нельзя использовать:
1) существующие фреймворки
2) все продукты, содержащие в названии, описании или на сайте слово Hadoop

Рекомендуется:
1) объяснить преподавателю как работает ваше решение
2) подумать (и реализовать) хоть что-то, что обеспечит надёжность вашего решения (те самые 99.999999% SLA)

В качестве тестовых данных при написании можете использовать https://epam-my.sharepoint.com/:u:/p/sergei_krotov/EXgMWH3CdiFFuD7QTQlsXzUBh7MFyLcuZdP5s4PRrQA54Q?e=QxFJCn
'''


import docker
import os
import logging
import json
logging.basicConfig(level=logging.INFO)

INPUT_DIR = os.path.abspath('input_files_test')
OUTPUT_DIR = os.path.abspath('out')

client = docker.APIClient()
logging.info('Starting')


def get_files(dir):
    files = os.listdir(dir)
    return files

def reduce(files):
    bytes = {0: 0, 1: 0}
    for file in files:
        output = json.load(file)
        bytes[0] += output['0']
        bytes[1] += output['1']

def start_container(file):
    host_config = client.create_host_config(
        binds={
            INPUT_DIR: {
                'bind': '/input_files_test',
                'mode': 'ro'
            },
            OUTPUT_DIR: {
                'bind': '/out',
                'mode': 'rw'
            }
        },
    )
    environment = {
        'INPUT_FILENAME': f'/input_files_test/{file}'
    }
    container = client.create_container(
        image='docker_test',
        host_config=host_config,
        environment=environment
    )
    client.start(container)
    return container

if __name__ == '__main__':
    input_files = get_files(INPUT_DIR)
    # print(*input_files[0:4], sep='\n')

    containers = []
    for file in input_files[0:4]:
        print(f'/input_files_test/{file}')
        print(file)
        container = start_container(file)
        containers.append(container)

    for container in containers:
        exit_code = client.wait(container)
        print(f"Container exited with code {exit_code}")
    #
    # output_files = get_files(OUTPUT_DIR)
    # reduce(output_files)
