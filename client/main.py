import cv2, requests, numpy, sys, time, zbar
# import RPi.GPIO as GPIO
from PIL import Image
from random import randint

camera = cv2.VideoCapture(0)
scanner = zbar.Scanner()
scanner.parse_config('enable')

items = {}
item_weights = {}


def update_server_state(barcode, weight):
    url = 'http://localhost:5000/update/' + str(barcode) + '/'
    r = requests.post(url, data={
        'weight': weight
    })

    if r.status_code == 200:
        return r.json()

    return None


def update_empty_items_server_state(barcode):
    url = 'http://localhost:5000/update/' + str(barcode) + '/'
    r = requests.post(url, data={
        'empty': True
    })

    if r.status_code == 200:
        return r.json()
    
    return None




### mocking the scale weight functionality
number_of_times_counted = {}
def get_updated_item_weight(barcode, weight):
    if not barcode in number_of_times_counted:
        number_of_times_counted[barcode] = 0

    number_of_times_counted[barcode] += 1

    if number_of_times_counted[barcode] % 10 == 0:
        new = weight - (items[barcode]['weight'] * .2)

        if new/items[barcode]['weight'] <= .15 and not items[barcode]['empty']:
            update_empty_items_server_state(barcode)

        return new

    return weight
###



if __name__ == '__main__':
    while True:
        grabbed, frame = camera.read()

        # raw detection code
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()

        # create a reader
        image = zbar.Image(width, height, 'Y800', raw)
        scanner.scan(image)

        # extract results

        for symbol in image:
            # do something useful with results
            barcode = symbol.data.decode('ascii')
            print(barcode)

            if not barcode in items:
                weight = None
                item = update_server_state(barcode, weight)

                if not 'weight' in item:
                    continue
            
                weight = item['weight']
                update_server_state(barcode, weight)

                item_weights[barcode] = weight
                items[barcode] = item

            else:
                if items[barcode]['empty']:
                    print('empty!!')
                    continue

                new_weight = get_updated_item_weight(barcode, item_weights[barcode])

                if new_weight != item_weights[barcode]:
                    item_weights[barcode] = new_weight
                    items[barcode] = update_server_state(barcode, item_weights[barcode])



        # show the frame and record if the user presses a key
        cv2.imshow("Barcode Detection", frame)
            
        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # time.sleep(1)