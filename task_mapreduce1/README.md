MapReduce is a framework created for BigData evaluations. 

The task was to write a program to calculate ones and zeros in .bin archives 
using MapReduce framework without use of any Hadoop products.

Ver.1

In this version MapReduce is made with docker-compose and RabbitMQ. 
Docker-compose helps to run several isolated services and that's how onw can start a cluster
of mapreduce machines:
```
>: cd rabbit
>:rabbit$ python3 start_cluster.py N
```
`where N is a number of machines to use for calculations`

To start calculation print:
```
>:rabbit$ python3 start_framework.py input
```
The result is saved in output/result.txt

Ver.2

This version makes computation:

- simply with python 
- in docker

To use just with python:
- uncomment line 54 in docker_test.py 
- comment line 51 in docker_test.py
- run docker_test.py

To use with dockers:
- uncomment line 51 in docker_test.py 
- comment line 54 in docker_test.py
- run start_cluster.py 



