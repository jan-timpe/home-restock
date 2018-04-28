import cv2, requests, sys, time, zbar
import RPi.GPIO as GPIO
from PIL import Image

camera = cv2.VideoCapture(0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

items = []
item_weights = {}


def update_server_state(item, weight):
    url = 'http://localhost:5000/update/' + str(item) + '/'
    r = requests.post(url, data={
        'weight': weight
    })

def update_empty_items_server_state(item):
    url = 'http://localhost:5000/update/' + str(item) + '/'
    r = requests.post(url, data={
        'empty': True
    })




number_of_times_counted = {}
def get_updated_item_weight(item, weight):
    if not item in number_of_times_counted:
        number_of_times_counted[item] = 0
    elif number_of_times_counted[item] % 5 == 0:
        new = weight - weight*.2

        if new <= 0:
            new = 0
            update_empty_items_server_state(item)

        return new

    return weight




if __name__ == '__main__':
    print 'go'
    while True:
        (grabbed, frame) = camera.read()

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
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            barcode = symbol.data
            if not barcode in items:
                items.append(barcode)
                item_weights[barcode] = 200
                update_server_state(barcode, item_weights[barcode])
            else:
                new_weight = get_updated_item_weight(barcode, item_weights[barcode])

                if new_weight != item_weights[barcode]:
                    item_weights[barcode] = new_weight
                    update_server_state(barcode, item_weights[barcode])


        # show the frame and record if the user presses a key
        cv2.imshow("Barcode Detection", frame)
            
        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # time.sleep(1)