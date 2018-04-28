package foodspy.foodspymobile;

import java.sql.Timestamp;

public class DateEntry {
    public String timestamp;
    public float weight;

    DateEntry(String timestamp, float weight){
        this.timestamp = timestamp;
        this.weight = weight;
    }
}
