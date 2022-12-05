package session.field.Controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class Controller {

    @Value("${KAFKA_TOPIC:#{test}}")
    public String kafkaTopic;

    @Value("${DEBUG:#{true}}")
    private String debug_env;
    private final boolean debug;

    private final ShutdownController shutdownController;

    public Controller(final ShutdownController shutdownController){
        this.debug = Boolean.parseBoolean(this.debug_env);
        this.shutdownController = shutdownController;
        Thread shutdownThread = new Thread(this.shutdownController);
        shutdownThread.start();
    }

    @KafkaListener(topics = "#{systemEnvironment['KAFKA_TOPIC']}")
    public void listener(@Payload String str) {
        this.shutdownController.newMessage();
        log.info("Received message" + str + "from topic: " + kafkaTopic);
    }
}