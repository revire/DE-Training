FROM python:latest
WORKDIR .
COPY receiver.py /receiver.py
RUN pip3 install pika
ENTRYPOINT ["python", "receiver.py"]