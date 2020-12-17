MapReduce is a framework created for BigData evaluations. 

The task was to write a program to calculate ones and zeros in .bin archives 
using MapReduce framework without use of any Hadoop products.


In this version MapReduce is made with Docker Compose and RabbitMQ. 
Docker Compose helps to run several isolated services and that's how 
one can start a cluster of mapreduce machines:
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

The durability of the framework is guaranteed by RabbitMQ Work Queue, that allows
to create queues and keeping messages there in cases cluster goes down. 
Also the framework has monitoring system that helps user to see the processes 
between sender and receiver. 

Additional function:
- delete messages from RabbitMQ queue
```>: docker exec rabbit_monitoring_1 python3 monitoring.py purge_queue```
(in case of testing you pushed sender too many times)


_____________________________________
Also tried:

Version with just docker containers:


    This version can be found in folder only_dockers    
    To use just with python:
    - uncomment line 54 in docker_test.py 
    - comment line 51 in docker_test.py
    - run docker_test.py
    
    To use with dockers:
    - uncomment line 51 in docker_test.py 
    - comment line 54 in docker_test.py
    - run start_cluster.py 

Version with RabbitMQ RPC:

    The RPC technic allows to connect sent files with workers' feedback
    Didn't continue it because it still required durable queue 
    and round-robin proccesses distribution.



