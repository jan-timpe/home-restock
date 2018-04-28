package foodspy.foodspymobile;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;


public class ListViewAdapter extends ArrayAdapter<FoodItem> {
    public ListViewAdapter(@NonNull Context context, ArrayList<FoodItem> foodItems) {
        super(context, 0, foodItems);
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        final FoodItem foodItem = getItem(i);

        if(view == null){
            view = LayoutInflater.from(getContext()).inflate(R.layout.food_list_content, viewGroup, false);
        }
        TextView tvName = (TextView) view.findViewById(R.id.tvName);
        TextView tvWeight = (TextView) view.findViewById(R.id.tvWeight);
        Button button = (Button) view.findViewById(R.id.buttonUrl);

        tvName.setText(foodItem.name);

        Float weight = foodItem.history.get(foodItem.history.size()-1).weight;
        tvWeight.setText(weight.toString() + "lbs");

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(foodItem.url));
                getContext().startActivity(i);
            }
        });
        return view;
    }
}
