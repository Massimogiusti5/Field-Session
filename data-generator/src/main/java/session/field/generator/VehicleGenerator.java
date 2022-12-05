package session.field.generator;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.springframework.stereotype.Service;
import session.field.datamodels.Vehicle;
import session.field.datamodels.VehicleType;

import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@Service
public class VehicleGenerator implements DataGenerator {

    private final GeometryFactory gf;

    private final Random random;

    private final int vehicleTypeSize;

    public VehicleGenerator(final GeometryFactory gf) {
        this.gf = gf;
        this.random = new Random();
        this.vehicleTypeSize = VehicleType.values().length;
    }

    @Override
    public List<Vehicle> generate(int numToGenerate) {
        return IntStream.range(0, numToGenerate).mapToObj(index -> this.generateVehicle()).collect(Collectors.toList());
    }

    private Vehicle generateVehicle() {
        return new Vehicle(this.getRandomVehicleType(), this.getRandomVin(), this.getRandomPoint());
    }

    private VehicleType getRandomVehicleType() {
        return VehicleType.values()[this.random.nextInt(this.vehicleTypeSize)];
    }

    private String getRandomVin() {
        return Integer.toString(this.random.nextInt(9999));
    }

    private Geometry getRandomPoint() {
        return this.gf.createPoint(new Coordinate(this.random.nextInt(180), this.random.nextInt(90)));
    }
}
