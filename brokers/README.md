# Messaging Brokers
This repo contains the Dockerfiles and other necessary files to starting one of the defined messaging services.

## Start ActiveMQ Container
Enter `active-mq/` and run

`$ docker-compose build`

`$ docker-compose up`

## Start RabbitMQ Container
Enter `rabbit-mq/` and run

`$ docker-compose build`

`$ docker-compose up`

## Start an instance of Kafka

- The images for zookeeper and kafka are both online, so the only thing to do is compose with those existing images.
- `$ cd kafka`
- `$ docker-compose up`