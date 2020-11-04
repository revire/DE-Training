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
import sys


def create_image(client):
    pass

def start_cluster():
    pass

def split_data():
    pass

def map_data(splits):
    for line in splits:
        for token in line.strip().split(' '):
            if token: print (token + '\t1')

def reduce_data(maps):
    (lastKey, sum) = (None, 0)
    for line in maps:
        (key, value) = line.strip().split('\t')
        if lastKey and lastKey != key:
            print (lastKey + '\t' + str(sum))
            (lastKey, sum) = (key, int(value))
        else:
            (lastKey, sum) = (key, sum + int(value))
    if lastKey: print (lastKey + '\t' + str(sum))

def count_bytes():
    pass

def job(path_gz):
     dockers = start_cluster()
     splits = split_data(path_gz)
     result = reduce_data(map_data(dockers, splits, count_bytes))
     return result

def main(program):
    programs = ['start_cluster', 'start_job']
    if program in programs:
        program()









