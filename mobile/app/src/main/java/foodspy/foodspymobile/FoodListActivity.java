package foodspy.foodspymobile;

import android.app.Activity;
import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.ListView;

public class FoodListActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        final Activity activity = this;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_food_list);
        new RetrieveDataAsync(this).execute();

        ListView listView = (ListView) findViewById(R.id.list_view);
        LayoutInflater inflater = getLayoutInflater();
        ViewGroup header = (ViewGroup)inflater.inflate(R.layout.food_list_header, listView, false);;
        listView.addHeaderView(header);

        final SwipeRefreshLayout mSwipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.activity_main_swipe_refresh_layout);
        mSwipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new RetrieveDataAsync(activity).execute();
                mSwipeRefreshLayout.setRefreshing(false);
            }
        });
    }

    /**
     * Repopulates the list.
     */
    @Override
    protected void onResume() {
        super.onResume();
        new RetrieveDataAsync(this).execute();
    }

}
