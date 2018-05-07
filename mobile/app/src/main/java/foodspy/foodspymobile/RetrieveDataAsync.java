package foodspy.foodspymobile;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import cz.msebera.android.httpclient.Header;

public class RetrieveDataAsync extends AsyncTask<String, Void, ArrayList<FoodItem>> {
    private Activity mActivity;
    public RetrieveDataAsync(Activity activity){
        this.mActivity = activity;
    }
    @Override
    protected ArrayList<FoodItem> doInBackground(String... strings) {
        final ArrayList<FoodItem> foodItems = new ArrayList<>();
        Handler mainHandler = new Handler(Looper.getMainLooper());
        Runnable myRunnable = new Runnable() {
            @Override
            public void run() {
                AsyncHttpClient client = new AsyncHttpClient();
                client.get("http://192.168.0.22:5000/products/", new AsyncHttpResponseHandler() {
                    @Override
                    public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                        try {
                            JSONObject bodyJsonObject = new JSONObject(new String(responseBody));
                            JSONArray products = bodyJsonObject.getJSONArray("products");
                            for(int j = 0; j < products.length(); j++) {
                                JSONObject jsonObject = products.getJSONObject(j);
                                String url = jsonObject.getString("add_to_cart_url");
                                String name = jsonObject.getString("name");
                                boolean empty = jsonObject.getBoolean("empty");
                                JSONArray jsonArray = jsonObject.getJSONArray("history");
                                ArrayList<DateEntry> history = new ArrayList<>();
                                for (int i = 0; i < jsonArray.length(); i++) {
                                    JSONObject obj = jsonArray.getJSONObject(i);
                                    String timestamp = obj.getString("timestamp");
                                    Float weight = Float.parseFloat(obj.get("weight").toString());
                                    history.add(new DateEntry(timestamp, weight));
                                }
                                String created = jsonObject.getString("created");
                                foodItems.add(new FoodItem(url, name, empty, history, created));
                            }
                            ListViewAdapter adapter = new ListViewAdapter(mActivity, foodItems);
                            ListView listView = (ListView) mActivity.findViewById(R.id.list_view);

                            listView.setAdapter(adapter);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                    @Override
                    public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                        error.printStackTrace();
                    }
                });
            }
        };
        mainHandler.post(myRunnable);

        return foodItems;
    }
    @Override
    protected void onPostExecute(ArrayList<FoodItem> foodItems){

    }
}
