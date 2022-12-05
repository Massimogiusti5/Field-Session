# Field Session

## Getting Started

### Running a Basic Messaging System

- The default messaging system is composed of one producer and two consumers, one in python and one in java.

- Ensure you have Docker installed. To check version run `$ docker --version`

- To run a kafka cluster, you first have to build the images for the microservices.
- First, from `brokers/docker-compose.yml` run `$ docker-compose up` to load the brokers into a container
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

- in addition, if you want a different environment variable configuration for a microservice, you can make another .env file and reference it in the `env_file` block.

### Adding Multiple Brokers

- In `brokers/docker-compose.yml` replace current file with this 3 broker config example:

``` yml

version: "3.5"
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
    networks:
        - fieldsession
  kafka-1:
    image: wurstmeister/kafka
    depends_on:
      - zookeeper
    networks:
        - fieldsession
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka-1
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
      KAFKA_CREATE_TOPICS: "sendvehicle:5:3"
    ports:
      - "19092:19092"
  kafka-2:
    image: wurstmeister/kafka
    depends_on:
      - zookeeper
    networks:
        - fieldsession
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka-2
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
    ports:
      - "29092:29092"
  kafka-3:
    image: wurstmeister/kafka
    depends_on:
      - zookeeper
    networks:
        - fieldsession
    environment:
      KAFKA_ADVERTISED_HOST_NAME: kafka-3
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: false
    ports:
      - "39092:39092"
networks:
  fieldsession:
   name: field_session
```

- To run a cluster with multiple brokers, the microservices require updated images.
- First `cd` into `data-generator` then in `DataGeneratorConfig.java`, replace line 32 with: `properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-1:19092, kafka-2:29092, kafka-3:39092");`. This ensures that the producer connects to all three instances of Kafka.
- For `data-processor-a`, in `DataProcessorAConfig.java` replace line 36 with: `properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-1:9092, kafka-2:9092, kafka-3:9092");`. This ensures that the producer can connect to all instances of Kafka.
- this can also be done with `data-processor-b`. To connect to the three brokers, in `kafka_consumer.py` change the variable `bootstrapServers` to `['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092']`.
- Then from `infrastructure/docker-compose.yml` run `$ docker-compose build` to update the images
- Then from `brokers/docker-compose.yml` run `$ docker-compose up` to load the brokers into a container
- Finally, run `$ docker-compose up` from `infrastructure/docker-compose.yml` to load the microservices into a container.

### Modifying Deployment

- Deployment to docker depends heavily on environment variables. They allow changes in message rate, modification to topics and where microservices send/recieve.

#### Configuring topics

- When scaling, it is important to mind the topic to which consumers subscribe to. If there are multiple consumers that want to subscribe to the same topic, the topic needs an additional partition. This can all be done in the compose file. Under Kafka's environment variables, by changing `KAFKA_AUTO_CREATE_TOPICS_ENABLE` to `FALSE`, and adding `KAFKA_CREATE_TOPICS: "TOPIC:PARTITIONS:REPLICATION_FACTOR"` to environment where `TOPIC` is the desired topic to be created, `PARTITIONS` is the amount of consumers you want to subscribe to the topic and `REPLICATION_FACTOR` is the amount of brokers you want the topic to span. See examples in `compose_configurations.txt`.
- In addition, make sure to update the `KAFKA_TOPIC` variable for each producer and consumer in the .env file.

#### Changing Message Rate

- The producer has `NUMBER_MESSAGES` and `MESSAGE_RATE_MS` as environment variables, and editing those in the .env file allows to change the number of messages sent as well as how often they are sent in milliseconds.