import pandas as pd
import matplotlib.pyplot as plt


class CreatePlots:
    def __init__(self, rabbitmq: str, activemq: str, kafka: str, size, left_cut: int = 200, right_cut: int = -1):
        rabbit_df = pd.read_csv(f'./data_visualization/clean_data/{rabbitmq}')
        active_df = pd.read_csv(f'./data_visualization/clean_data/{activemq}')
        kafka_df = pd.read_csv(f'./data_visualization/clean_data/{kafka}')
        self.rabbit_group = rabbit_df[left_cut:right_cut].groupby('Name')
        self.active_group = active_df[left_cut:right_cut].groupby('Name')
        self.kafka_group = kafka_df[left_cut:right_cut].groupby('Name')
        self.i = 0
        self.size = size
        self.fig, self.axs = plt.subplots(size, 2)

    def plot(self):
        plt.show()

    def create_generator_plots(self):
        if self.i == self.size:
            print('Plot too big')
            return
        self.rabbit_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='RabbitMQ',
                                                                                  legend=True)
        self.active_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='ActiveMQ',
                                                                                  legend=True)
        self.kafka_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='Kafka',
                                                                                 legend=True)
        self.axs[self.i, 0].set_title("CPU Percentage Data Generator")

        self.rabbit_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='RabbitMQ',
                                                                                  legend=True)
        self.active_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='ActiveMQ',
                                                                                  legend=True)
        self.kafka_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='Kafka',
                                                                                 legend=True)
        self.axs[self.i, 1].set_title("Memory Percentage Data Generator")

        self.i += 1

    def create_processor_plots_java(self):
        if self.i == self.size:
            print('Plot too big')
            return
        self.rabbit_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='RabbitMQ Java',
                                                                                    legend=True)
        self.active_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='ActiveMQ Java',
                                                                                    legend=True)
        self.kafka_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='Kafka Java',
                                                                                   legend=True)
        self.axs[self.i, 0].set_title("CPU Percentage Data Processors Java")

        self.rabbit_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='RabbitMQ Java',
                                                                                    legend=True)
        self.active_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='ActiveMQ Java',
                                                                                    legend=True)
        self.kafka_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='Kafka Java',
                                                                                   legend=True)
        self.axs[self.i, 1].set_title("Memory Percentage Data Processors Java")

        self.i += 1

    def create_processor_plots_python(self):
        if self.i == self.size:
            print('Plot too big')
            return
        self.rabbit_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=self.axs[self.i, 0],
                                                                                    label='RabbitMQ Python',
                                                                                    legend=True)
        self.active_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=self.axs[self.i, 0],
                                                                                    label='ActiveMQ Python',
                                                                                    legend=True)
        self.kafka_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='Kafka Python',
                                                                                   legend=True)
        self.axs[self.i, 0].set_title("CPU Percentage Data Processors Python")

        self.rabbit_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=self.axs[self.i, 1],
                                                                                    label='RabbitMQ Python',
                                                                                    legend=True)
        self.active_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=self.axs[self.i, 1],
                                                                                    label='ActiveMQ Python',
                                                                                    legend=True)
        self.kafka_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='Kafka Python',
                                                                                   legend=True)
        self.axs[self.i, 1].set_title("Memory Percentage Data Processors Python")
        self.i += 1

    def create_broker_plots(self):
        if self.i == self.size:
            print('Plot too big')
            return
        self.rabbit_group.get_group('rabbit-mq-rabbitmq-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='RabbitMQ', legend=True)
        self.active_group.get_group('active-mq-activemq-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='ActiveMQ', legend=True)
        self.kafka_group.get_group('kafka-kafka-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='Kafka', legend=True)
        self.kafka_group.get_group('kafka-zookeeper-1')['CPUPerc'].plot(ax=self.axs[self.i, 0], label='Zookeeper', legend=True)
        self.axs[self.i, 0].set_title("CPU Percentage Broker")

        self.rabbit_group.get_group('rabbit-mq-rabbitmq-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='RabbitMQ', legend=True)
        self.active_group.get_group('active-mq-activemq-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='ActiveMQ', legend=True)
        self.kafka_group.get_group('kafka-kafka-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='Kafka', legend=True)
        self.kafka_group.get_group('kafka-zookeeper-1')['MemPerc'].plot(ax=self.axs[self.i, 1], label='Zookeeper', legend=True)
        self.axs[self.i, 1].set_title("Memory Percentage Broker")
        self.i += 1


def create_run_plot(rabbitmq: str, activemq: str, kafka: str):
    rabbit_df = pd.read_csv(f'./data_visualization/clean_data/{rabbitmq}')
    active_df = pd.read_csv(f'./data_visualization/clean_data/{activemq}')
    kafka_df = pd.read_csv(f'./data_visualization/clean_data/{kafka}')
    fig, axs = plt.subplots(4, 2)

    rabbit_group = rabbit_df[200:].groupby('Name')
    active_group = active_df[200:].groupby('Name')
    kafka_group = kafka_df[200:].groupby('Name')

    rabbit_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=axs[0, 0], label='RabbitMQ', legend=True)
    active_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=axs[0, 0], label='ActiveMQ', legend=True)
    kafka_group.get_group('infrastructure-data-generator-1')['CPUPerc'].plot(ax=axs[0, 0], label='Kafka', legend=True)
    axs[0, 0].set_title("CPU Percentage Data Generator")

    rabbit_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=axs[0, 1], label='RabbitMQ', legend=True)
    active_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=axs[0, 1], label='ActiveMQ', legend=True)
    kafka_group.get_group('infrastructure-data-generator-1')['MemPerc'].plot(ax=axs[0, 1], label='Kafka', legend=True)
    axs[0, 1].set_title("Memory Percentage Data Generator")

    rabbit_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=axs[1, 0], label='RabbitMQ Java', legend=True)
    active_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=axs[1, 0], label='ActiveMQ Java', legend=True)
    kafka_group.get_group('infrastructure-data-processor-a-1')['CPUPerc'].plot(ax=axs[1, 0], label='Kafka Java', legend=True)
    axs[1, 0].set_title("CPU Percentage Data Processors Java")

    rabbit_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=axs[2, 0], label='RabbitMQ Python', legend=True)
    active_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=axs[2, 0], label='ActiveMQ Python', legend=True)
    kafka_group.get_group('infrastructure-data-processor-b-1')['CPUPerc'].plot(ax=axs[2, 0], label='Kafka Python', legend=True)
    axs[2, 0].set_title("CPU Percentage Data Processors Python")

    rabbit_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=axs[1, 1], label='RabbitMQ Java', legend=True)
    active_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=axs[1, 1], label='ActiveMQ Java', legend=True)
    kafka_group.get_group('infrastructure-data-processor-a-1')['MemPerc'].plot(ax=axs[1, 1], label='Kafka Java', legend=True)
    axs[1, 1].set_title("Memory Percentage Data Processors Java")

    rabbit_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=axs[2, 1], label='RabbitMQ Python', legend=True)
    active_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=axs[2, 1], label='ActiveMQ Python', legend=True)
    kafka_group.get_group('infrastructure-data-processor-b-1')['MemPerc'].plot(ax=axs[2, 1], label='Kafka Python', legend=True)
    axs[2, 1].set_title("Memory Percentage Data Processors Python")

    rabbit_group.get_group('rabbit-mq-rabbitmq-1')['CPUPerc'].plot(ax=axs[3, 0], label='RabbitMQ', legend=True)
    active_group.get_group('active-mq-activemq-1')['CPUPerc'].plot(ax=axs[3, 0], label='ActiveMQ', legend=True)
    kafka_group.get_group('kafka-kafka-1')['CPUPerc'].plot(ax=axs[3, 0], label='Kafka', legend=True)
    kafka_group.get_group('kafka-zookeeper-1')['CPUPerc'].plot(ax=axs[3, 0], label='Zookeeper', legend=True)
    axs[3, 0].set_title("CPU Percentage Broker")

    rabbit_group.get_group('rabbit-mq-rabbitmq-1')['MemPerc'].plot(ax=axs[3, 1], label='RabbitMQ', legend=True)
    active_group.get_group('active-mq-activemq-1')['MemPerc'].plot(ax=axs[3, 1], label='ActiveMQ', legend=True)
    kafka_group.get_group('kafka-kafka-1')['MemPerc'].plot(ax=axs[3, 1], label='Kafka', legend=True)
    kafka_group.get_group('kafka-zookeeper-1')['MemPerc'].plot(ax=axs[3, 1], label='Zookeeper', legend=True)
    axs[3, 1].set_title("Memory Percentage Broker")

    plt.show()


if __name__ == '__main__':
    plots = CreatePlots('RabbitMQ-1000-messages--metrics-11-20-2022-20:11:34.txt',
                        'ActiveMQ-1000-messages--metrics-11-20-2022-20:38:50.txt',
                        'Kafka-1000-messages--metrics-11-19-2022-09:54:32.txt', 2, right_cut=1400)
    plots.create_generator_plots()
    plots.create_broker_plots()
    plots.plot()
