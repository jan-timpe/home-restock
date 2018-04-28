import cv2, requests, sys, time
from hx711 import HX711
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO

# consts

POLL_RATE = 10 # seconds
BUFFER_SIZE = 10 # records
ITEM_REMOVED_TIME = 60 # seconds
CAMERA_PORT = 0
RAMP_FRAMES = 30 # throw out frames while camera focuses

items = []
weights = []
images = []
item_weights = []

##


# init weight sensors

def clean_and_exit():
    print('Cleaning')
    GPIO.cleanup()
    print('Done!')
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format('LSB', 'MSB')
hx.set_reference_unit(92)

hx.reset()
hx.tare()

##

# init camera

camera = cv2.VideoCapture(CAMERA_PORT)

##

# functions

def get_image():
    retval, img = camera.read()
    return img

def read_barcodes(img):
    # img = cv2.imread(img_path)
    barcodes = decode(img)

    items = []
    for code in barcodes:
        # append upc code
        items.append(code.data.decode()[1:])
    
    return items


def items_difference(prev, curr):
    shared = []
    missing = []
    new = []

    for item in prev:
        if item in curr:
            shared.append(item)
        else:
            missing.append(item)
    
    for item in curr:
        if item not in prev:
            new.append(item)

    return shared, missing, new


# try to determine item weights]
# only really works for a single item at a time
def calculate_item_weights(shared, missing, new, prev_weight, curr_weight, item_weights):
    needs_update = []
    if len(new) == 1 and len(missing) == 0:
        new_weight = curr_weight - prev_weight
        if not new[0] in item_weights or item_weights[new[0]] != new_weight:
            needs_update.append(new[0])
        item_weights[new[0]] = new_weight

    elif len(new) == 0 and len(missing) == 1:
        missing_weight = prev_weight - curr_weight
        if not missing[0] in item_weights or item_weights[missing[0]] != missing_weight:
            needs_update.append(missing[0])
        item_weights[missing[0]] = missing_weight

    return item_weights, needs_update


def update_server_state(items, item_weights):
    for item in items:
        url = 'http://localhost:5000/update/' + str(item) + '/'
        r = requests.post(url, data={
            'weight': item_weights[item]
        })


def update_empty_items_server_state(items):
    for item in items:
        url = 'http://localhost:5000/update/' + str(item) + '/'
        r = requests.post(url, data={
            'empty': True
        })


def empty_items(items):
    empty = []
    all_items = [item for item in item_set for item_set in items[1:]]
    if len(items) > 1:
        start = items[0]
        for item in start:
            if item not in all_items:
                empty.append(items)

    return empty

##

# run

if __name__ == '__main__':

    for i in range(RAMP_FRAMES):
        temp = get_image()

    while True:
        try:
            weight = hx.get_weight(5)
            hx.power_down()
            hx.power_up()

            image = get_image()

            weights.append(weight)
            # images.append(image)
            items.append(read_barcodes(image))

            print(weight)
            print(items)

            if len(weights) > BUFFER_SIZE:
                weights.pop(0)

            # if len(images) > BUFFER_SIZE:
            #     images.pop(0)

            if len(items) > BUFFER_SIZE:
                empty = empty_items(items)
                update_empty_items_server_state(empty) 
                items.pop(0)

            if len(items) > 1:
                prev = items[-2]
                curr = items[-1]
                prev_weight = weights[-2]
                curr_weight = weights[-1]

                shared, missing, new = items_difference(prev, curr)

                item_weights, needs_update = calculate_item_weights(
                    shared,
                    missing,
                    new,
                    prev_weight,
                    curr_weight,
                    item_weights
                )

                update_server_state(needs_update, item_weights)

            time.sleep(POLL_RATE)
        except (KeyboardInterrupt, SystemExit):
            clean_and_exit()
            del(camera)