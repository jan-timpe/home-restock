package foodspy.foodspymobile;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

public class FoodListActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_food_list);
        new RetrieveDataAsync(this).execute();
    }
}
