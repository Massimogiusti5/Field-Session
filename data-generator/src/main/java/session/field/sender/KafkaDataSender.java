package session.field.sender;

import org.springframework.context.ApplicationContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.stereotype.Service;
import session.field.datamodels.Vehicle;
import session.field.generator.DataGenerator;
import org.springframework.kafka.core.KafkaTemplate;

import javax.annotation.PostConstruct;

@Slf4j
@Service
public class KafkaDataSender implements DataSender {

    @Autowired
    private ApplicationContext context;

    private final DataGenerator dataGenerator;
    private int sentMessages;

    @Value("${NUMBER_MESSAGES:#{50}}")
    private String numMessages;

    @Value("${MESSAGE_RATE_MS:#{0}}")
    private String messageRateMS;

    @Value("${DEBUG:#{false}}")
    private String debug_env;
    private final boolean debug;

    private String kafkaTopic = System.getenv().get("KAFKA_TOPIC");
    private String[] kafkaTopics = kafkaTopic.split(",");

    private KafkaTemplate kafkaTemplate;

    public KafkaDataSender(DataGenerator dataGenerator, KafkaTemplate kafkaTemplate){
        this.debug = Boolean.parseBoolean(this.debug_env);
        this.dataGenerator = dataGenerator;
        this.kafkaTemplate = kafkaTemplate;
        this.sentMessages = 0;
    }

    @PostConstruct
    public void sendMessages() throws InterruptedException {
        this.dataGenerator.generate(Integer.parseInt(this.numMessages)).forEach(this::send);
        int exitCode = 0;
        if (Integer.parseInt(this.messageRateMS) > 0){
            try {
                this.delayedSend();
            }
            catch (InterruptedException e) {
                System.out.println("System Interrupt");
            }
            catch (Exception e) {
                exitCode = 1;
            }
        }
        else {
            this.dataGenerator.generate(Integer.parseInt(this.numMessages)).forEach(this::send);
            if (this.sentMessages != Integer.parseInt(this.numMessages)) {
                exitCode = 1;
            }
        }

        int finalExitCode = exitCode;
        SpringApplication.exit(this.context);
        System.exit(finalExitCode);
    }


    public void delayedSend() throws InterruptedException {
         while(true) {
            this.dataGenerator.generate(Integer.parseInt(numMessages)).forEach(this::send);
            Thread.sleep(Integer.parseInt(messageRateMS));
        }
    }


    @Override
    public SendStatus send(Vehicle vehicle) {
        SendStatus status = SendStatus.FAILURE;
        try {
            for(String topic : kafkaTopics){
                this.kafkaTemplate.send(topic, vehicle.toString());
                if (this.debug) {
                    log.info("Message sent to " + topic + ": " + vehicle);
                }
                status = SendStatus.SUCCESS;
            }
            this.sentMessages += 1;
        } catch (final Exception e) {
            log.error("Something went wrong POSTing data to one of the Processors!", e);
        }
        return status;
    }
}
