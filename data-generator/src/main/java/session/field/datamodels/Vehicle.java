package session.field.datamodels;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.json.JSONException;
import org.locationtech.jts.geom.Geometry;
import org.json.JSONObject;


public class Vehicle {

    private VehicleType type;

    private String vin;

    private Geometry location;

    public Vehicle(@JsonProperty VehicleType type, @JsonProperty String vin, @JsonProperty Geometry location) {
        this.type = type;
        this.vin = vin;
        this.location = location;
    }

    public Vehicle(){
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
        JSONObject str = new JSONObject();

        try {
            str.put("vehicletype", this.getType());
            str.put("vin", this.getVin());
            str.put("location", this.getLocation());
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
        return str.toString();
    }
}
