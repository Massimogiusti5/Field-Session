package session.field.sender;

import session.field.datamodels.Vehicle;

public interface DataSender {
    public SendStatus send(final Vehicle vehicle);
}
