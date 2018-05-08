# Home Re:Stock

Project for Wearable and Ubiquitous Computing at the University of Arkansas. 

The project has 3 components, a Flask webserver, a Python client-script, and an Android app.

## Create a virtualenv and install requirements

Both the client and server are meant to be run on a Raspberry Pi with a USB webcam connected (to any port). Open CV needs to be [manually downloaded and compiled](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) to be compatible with an ARM architecture (huge pain), thus the client script does not use a `virtualenv`. A `virtualenv` is optional for the Flask app as well. If you opt not to use a `virtualenv`, be sure to install requirements before running the server.

```bash
virtualenv venv -p python3
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run the server
Make sure to replace `api_key` in `web/controller.py` with your own from the [Walmart Open API portal](https://developer.walmartlabs.com/)

```bash
cd web
export FLASK_APP=main.py
flask run --host=0.0.0.0
```

## Run the client
In another terminal window, at the base of the project, run:
```bash
pip -r requirements.txt
source ./venv/bin/activate
cd client
python main.py
```

## Run the app
Open the `mobile` directory in Android Studio. Replace the url in `app/src/main/java/foodspy/foodspymobile/RetrieveDataAsync.java` with the hostname/IP of your server (Flask runs on port `5000` by default).

## Adding products

Place a product on the platform in front of the Raspberry Pi and webcam (with the barcode facing the camera). Adjust to get a clear image of the barcode. Weight sensing is mocked due to buggy load cells (removes 20% of the products initial weight for every 10 frames the barcode is captured).

Products can be viewed at `http://flask-hostname:5000/products` or by refreshing the screen (pull down to refresh) in the Android app.

## Members

[Emad Siddiqui](https://github.com/eusiddiq)

[Blake Reed](https://github.com/BlakeReed19)

[Jan Timpe](https://github.com/jan-timpe)
