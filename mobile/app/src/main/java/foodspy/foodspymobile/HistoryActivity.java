package foodspy.foodspymobile;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.format.DateUtils;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.LabelFormatter;
import com.jjoe64.graphview.Viewport;
import com.jjoe64.graphview.helper.DateAsXAxisLabelFormatter;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

public class HistoryActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        Spinner spinner = (Spinner) findViewById(R.id.spinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.options, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        spinner.setAdapter(adapter);
        spinner.setOnItemSelectedListener(new OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                Object item = adapterView.getItemAtPosition(i);
                if(item.toString().equals("Daily")){
                    setGraph('d');
                } else if(item.toString().equals("Weekly")){
                    setGraph('w');
                } else if(item.toString().equals("Monthly")){
                    setGraph('m');
                } else if(item.toString().equals("Yearly")){
                    setGraph('y');
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView){
                setGraph('d');
            }
        });

        //setGraph('d');
    }

    private void setGraph(char mode){
        Intent intent = getIntent();
        ArrayList<DateEntry> history = intent.getParcelableArrayListExtra("history");

        DataPoint[] dataPoints = new DataPoint[history.size()];

        ArrayList<Date> dates = new ArrayList<>();
        for(int i = 0; i < history.size(); i++){
            String date = history.get(i).timestamp.substring(0, history.get(i).timestamp.length()-4);
            SimpleDateFormat formatter=new SimpleDateFormat("E, dd MMM yyyy HH:mm:ss");
            try {
                dates.add(formatter.parse(date));
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }

        for(int i = 0; i < history.size(); i++){
            dataPoints[i] = new DataPoint(dates.get(i), history.get(i).weight);
        }

        GraphView graph = (GraphView) findViewById(R.id.graph);
        graph.removeAllSeries();

        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(dataPoints);

        graph.addSeries(series);

        ArrayList<Date> filterredDates = new ArrayList<>();
        if(mode== 'd'){
            for(int i = 0; i < dates.size(); i++){
                if(DateUtils.isToday(dates.get(i).getTime())){
                    filterredDates.add(dates.get(i));
                }
            }
            final SimpleDateFormat sdf = new SimpleDateFormat("hh:mm:ss");
            // set date label formatter
            //graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(getApplicationContext()));
            graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if(isValueX){
                        return sdf.format(new Date((long) value));
                    }
                    return super.formatLabel(value, isValueX);
                }
            });
        }
        else if(mode == 'w'){
            Calendar calendar = Calendar.getInstance();
            calendar.add(Calendar.DAY_OF_YEAR, -7);

            for(int i = 0; i < dates.size(); i++){
                if(dates.get(i).getTime() > calendar.getTimeInMillis()){
                    filterredDates.add(dates.get(i));
                }
            }
            final SimpleDateFormat sdf = new SimpleDateFormat("E hh:mm");
            // set date label formatter
            //graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(getApplicationContext()));
            graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if(isValueX){
                        return sdf.format(new Date((long) value));
                    }
                    return super.formatLabel(value, isValueX);
                }
            });
        }
        else if(mode == 'm'){
            Calendar calendar = Calendar.getInstance();
            calendar.add(Calendar.DAY_OF_YEAR, -30);

            for(int i = 0; i < dates.size(); i++){
                if(dates.get(i).getTime() > calendar.getTimeInMillis()){
                    filterredDates.add(dates.get(i));
                }
            }
            final SimpleDateFormat sdf = new SimpleDateFormat("MMM dd");
            // set date label formatter
            //graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(getApplicationContext()));
            graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if(isValueX){
                        return sdf.format(new Date((long) value));
                    }
                    return super.formatLabel(value, isValueX);
                }
            });
        }
        else if(mode == 'y'){
            Calendar calendar = Calendar.getInstance();
            calendar.add(Calendar.DAY_OF_YEAR, -365);

            for(int i = 0; i < dates.size(); i++){
                if(dates.get(i).getTime() > calendar.getTimeInMillis()){
                    filterredDates.add(dates.get(i));
                }
            }
            final SimpleDateFormat sdf = new SimpleDateFormat("dd/MMM/yy");
            // set date label formatter
            //graph.getGridLabelRenderer().setLabelFormatter(new DateAsXAxisLabelFormatter(getApplicationContext()));
            graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
                @Override
                public String formatLabel(double value, boolean isValueX) {
                    if(isValueX){
                        return sdf.format(new Date((long) value));
                    }
                    return super.formatLabel(value, isValueX);
                }
            });
        }
        graph.getGridLabelRenderer().setNumHorizontalLabels(4);

        if(filterredDates.size() > 0){
            // set manual x bounds to have nice steps
            graph.getViewport().setMinX(filterredDates.get(0).getTime());
            graph.getViewport().setMaxX(filterredDates.get(filterredDates.size()-1).getTime());
            graph.getViewport().setXAxisBoundsManual(true);
        }
        else{
            // set manual x bounds to have nice steps
            graph.getViewport().setMinX(dates.get(0).getTime());
            graph.getViewport().setMaxX(dates.get(dates.size()-1).getTime());
            graph.getViewport().setXAxisBoundsManual(true);

        }

        // as we use dates as labels, the human rounding to nice readable numbers
        // is not necessary
        graph.getGridLabelRenderer().setHumanRounding(false);
    }
}
