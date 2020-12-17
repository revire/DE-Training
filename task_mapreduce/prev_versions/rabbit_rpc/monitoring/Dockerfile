FROM python:latest
WORKDIR .
COPY monitoring.py /monitoring.py
RUN pip3 install pika
#ENTRYPOINT ["python","-u", "monitoring.py"]