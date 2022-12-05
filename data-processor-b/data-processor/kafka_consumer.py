from kafka import KafkaConsumer
import sys
import os
import kafka
import time

def main():
    bootstrap_servers = ['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092']
    topicName = os.environ.get('KAFKA_TOPIC', 'test')
    debug = os.environ.get('DEBUG', 'False')

    delay = int(os.environ.get('MESSAGE_RATE_MS', 0))
    num_messages = int(os.environ.get('NUMBER_MESSAGES', 50))
    _messages_received = 0

    kafka_connection = False;
    #Connect to Kafka
    while(not kafka_connection):
        try:
            consumer = KafkaConsumer (topicName, group_id = 'group1',bootstrap_servers = bootstrap_servers,
            auto_offset_reset = 'earliest')
            kafka_connection = True
        except kafka.errors.NoBrokersAvailable:
            print ('Kafka broker not available, trying again...')
            time.sleep(1.0);
            kafka_connection = False

    #Receive messages
    try:
        for message in consumer:
            if (bool(debug)):
                print ("%s:%d:%d: value=%s" % (message.topic, message.partition,message.offset, message.value))
            _messages_received += 1
            if (delay == 0 and _messages_received == num_messages):
                sys.exit()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()