package session.field.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;


@Component
public class ShutdownController extends Thread {

    @Value("${NUMBER_MESSAGES:#{50}}")
    private String numMessages;

    @Value("${MESSAGE_RATE_MS:#{0}}")
    private String messageRateMS;

    @Autowired
    private ApplicationContext context;

    private int receivedMessages = 0;

    private boolean shutdown = false;

    private void shutdownApplication(){
        SpringApplication.exit(this.context);
        System.exit(0);
    }

    public void run() {
        while (!this.shutdown) {
            try {
                Thread.sleep(1);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
        this.shutdownApplication();
    }

    // Track all incoming messages
    public void newMessage(){
        this.receivedMessages += 1;
        if (this.receivedMessages >= Integer.parseInt(this.numMessages)
                & Integer.parseInt(this.messageRateMS) == 0){
            this.shutdown = true;
        }
    }

}
