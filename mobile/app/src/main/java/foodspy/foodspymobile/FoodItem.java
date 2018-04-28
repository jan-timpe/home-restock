package foodspy.foodspymobile;

import java.util.ArrayList;

public class FoodItem {
    public String url;
    public String name;
    public boolean empty;
    public ArrayList<DateEntry> history;
    public String created;

    public FoodItem(String url, String name, boolean empty, ArrayList<DateEntry> history, String created){
        this.url = url;
        this.name = name;
        this.empty = empty;
        this.history = history;
        this.created = created;
    }
}
