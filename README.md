# food-spy

Project for Wearable and Ubiquitous Computing at the University of Arkansas

## Run the server

Make sure to replace `api_key` in `controller.py` with your own from the [Walmart Open API portal](https://developer.walmartlabs.com/)

```bash
virtualenv env -p python3
source ./env/bin/activate
pip install -r requirements.txt
export FLASK_APP=main.py
flask run
```

## Testing the server

```bash
python test.py
```

## Members

Emad Siddiqui

Blake Reed

Jan Timpe
