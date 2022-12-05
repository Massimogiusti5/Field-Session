FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN git config --global http.sslverify false

RUN python -m pip install --upgrade pip

RUN pip install kafka-python

ADD data-processor ./data-processor

CMD ["python", "./data-processor/kafka_consumer.py"]