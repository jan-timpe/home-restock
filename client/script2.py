import cv2, requests, sys, time
# from hx711 import HX711
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO




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



if __name__ == '__main__':
    while True:
        img = get_image()
        codes = read_barcodes(img)

        print(codes)

        time.sleep(1)