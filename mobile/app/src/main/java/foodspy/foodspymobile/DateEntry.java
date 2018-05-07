package foodspy.foodspymobile;

import android.os.Parcel;
import android.os.Parcelable;

import java.sql.Timestamp;

public class DateEntry implements Parcelable {
    public String timestamp;
    public float weight;

    DateEntry(String timestamp, float weight){
        this.timestamp = timestamp;
        this.weight = weight;
    }

    protected DateEntry(Parcel in) {
        timestamp = in.readString();
        weight = in.readFloat();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(timestamp);
        dest.writeFloat(weight);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    public static final Creator<DateEntry> CREATOR = new Creator<DateEntry>() {
        @Override
        public DateEntry createFromParcel(Parcel in) {
            return new DateEntry(in);
        }

        @Override
        public DateEntry[] newArray(int size) {
            return new DateEntry[size];
        }
    };
}
