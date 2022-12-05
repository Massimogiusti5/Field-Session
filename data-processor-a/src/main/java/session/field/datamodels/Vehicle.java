package session.field.datamodels;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.apache.commons.lang3.builder.ReflectionToStringBuilder;
import org.locationtech.jts.geom.Geometry;

public class Vehicle {

    private VehicleType type;

    private String vin;

    private Geometry location;

    public Vehicle(@JsonProperty VehicleType type,@JsonProperty final String vin,@JsonProperty final Geometry location) {
        this.type = type;
        this.vin = vin;
        this.location = location;
    }

    public VehicleType getType() {
        return this.type;
    }

    public void setType(VehicleType type) {
        this.type = type;
    }

    public String getVin() {
        return this.vin;
    }

    public void setVin(String vin) {
        this.vin = vin;
    }

    public Geometry getLocation() {
        return this.location;
    }

    public void setLocation(Geometry location) {
        this.location = location;
    }

    @Override
    public String toString() {
        return ReflectionToStringBuilder.toString(this);
    }
}
