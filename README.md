# Field Session

## About

This project was made for CSCI370: Advanced Software Engineering at the Colorado School of Mines. Essentially, it is the result of research on different messaging systems: Kafka, ActiveMQ and RabbitMQ. These systems were tested for cloud deployment within Docker. In this repository there are folders for brokers and microservices, with the compose scripts to deploy them onto a Docker container. There is also an integration test suite that tests the performance metrics during deployment.

## Getting Started

### Running a Basic Messaging System

- The default messaging system is composed of three microservices: one producer and two consumers (one in python and one in java). There are also broker clusters for each messaging system under `brokers` that run alongside the microservices.

- Ensure you have Docker installed. To check version run `$ docker --version`

- To run a Kafka cluster, you first have to build the images for the microservices.
- First, from `brokers/kafka/docker-compose.yml` run `$ docker-compose up` to load the brokers into a container
- Then, from `infrastructure/docker-compose.yml` run `$ docker-compose build` to build the images for each microservice.
- Finally, run `$ docker-compose up` from `infrastructure/docker-compose.yml` to load the microservices into a container.
- Now messages should be going through!


#### Scaling Microservices

- To keep adding microservices, keep adding objects under services that use either the producer or consumer image. See `Modifying Deployment` for configuring the broker to handle scaling.

Example:

``` yml
data-processor-1:
  build:
    context: ../data-processor-a
  image: data-processor-a
  volumes:
    - "${HOME}/.m2:/root/.m2"
  depends_on:
    - kafka
    - zookeeper
  networks:
    - fieldsession
  env_file:
    - .env
data-processor-2:
  build:
    context: ../data-processor-a
  image: data-processor-a
  volumes:
    - "${HOME}/.m2:/root/.m2"
  networks:
  - fieldsession
  depends_on:
    - kafka
    - zookeeper
  env_file:
    - .env
```

- in addition, if you want a different environment variable configuration for a microservice, you can add an `environment` block to the compose file specifying what the variable should be.

### Different Broker Configurations

- In `brokers/kafka/docker-compose.yml`, the default configuration is with three brokers. To scale down to one broker, change the file to the following:

``` yml
---
version: "3.5"
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
    networks:
      - fieldsession
  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper
    networks:
      - fieldsession
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
      KAFKA_CREATE_TOPICS: "sendvehicle:2:1"
networks:
  fieldsession:
    name: field_session
```

- To run a cluster with one broker, the microservices require updated images.
- First `cd` into `data-generator/src/main/java/session/field/config` then in `DataGeneratorConfig.java`, replace line 32 with: `properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");`.
- For `data-processor-a`, in `data-processor-a/src/main/java/session/field/config/DataProcessorAConfig.java` replace line 36 with: `properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");`.
- this can also be done with `data-processor-b`. in `data-processor-b/data-processor/kafka_consumer.py` change the variable `bootstrapServers` to `['kafka:9092']`.

- Then from `infrastructure/docker-compose.yml` run `$ docker-compose build` to update the images
- Then from `brokers/docker-compose.yml` run `$ docker-compose up` to load the brokers into a container
- Finally, run `$ docker-compose up` from `infrastructure/docker-compose.yml` to load the microservices into a container.

- You can also scale the configuration up. it is possible to scale instances of zookeeper and futher instances of kafka.

### Modifying Deployment

- Deployment to docker depends heavily on environment variables. They allow changes in message rate, modification to topics and where microservices send/recieve.

#### Configuring topics

- When scaling, it is important to mind the topic to which consumers subscribe to. If there are multiple consumers that want to subscribe to the same topic, the topic needs an additional partition. This can all be done in the compose file. Under Kafka's environment variables, by changing `KAFKA_AUTO_CREATE_TOPICS_ENABLE` to `FALSE`, and adding `KAFKA_CREATE_TOPICS: "TOPIC:PARTITIONS:REPLICATION_FACTOR"` to environment where `TOPIC` is the desired topic to be created, `PARTITIONS` is the amount of consumers you want to subscribe to the topic and `REPLICATION_FACTOR` is the amount of brokers you want the topic to span. See examples in `compose_configurations.txt`.
- In addition, make sure to update the `KAFKA_TOPIC` variable for each producer and consumer in the .env file.

#### Changing Message Rate

- The producer has `NUMBER_MESSAGES` and `MESSAGE_RATE_MS` as environment variables, and editing those in the .env file allows to change the number of messages sent as well as how often they are sent in milliseconds. You can also change the `KAFKA_TOPIC` variable to modify the topic sent/subscribed to for the microservices.


## Using the Integration Test Suite

- The integration test suite tests performance of containers when running a messaging system cluster. There are different kinds of tests that can be modified based on the command line arguments that are fed to the script.
- Before running a test, change `infrastructure/.env` to:

```
NUMBER_MESSAGES=${NUMBER_MESSAGES}
MESSAGE_RATE_MS=${MESSAGE_RATE_MS}
DEBUG=${DEBUG}
KAFKA_TOPIC="sendvehicle"
```

### N Messages to Consumers
This test continuously produces messages from the generator until the set number
of messages have been sent from the producer and consumed from the processors.
To run set the number of messages by `--number-messages` and the `--broker`.

### Timed Run with Consistent Production
This test is a duration test, that has the producer consistently send messages
on a fixed delay for an amount of time. To run set the number of messages to be
sent on the interval with `--number-messages`, the delay in ms between production
with `--message-rate`, the duration of the test in seconds with `--time` and the current
broker with `--broker`

## Setup
Make sure you have your virtual environment setup correctly.

Run in the root directory to install the necessary packages.

`pip install .`

Start the correct broker in another terminal.

Run `__main__.py` with command line arguments to define a test.

Ex.

`python __main__.py --number-messages=1000 --broker=activemq --docker-compose=../../infrastructure/docker-compose.yml`

After the test completes a graph will appear in a new window of metrics from the test.

![img.png](rabbitmq_test.png)
