package session.field.generator;

import session.field.datamodels.Vehicle;

import java.util.List;

public interface DataGenerator {

    List<Vehicle> generate(final int numToGenerate);
}
