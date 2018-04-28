import cv2, requests, sys, time, zbar
import RPi.GPIO as GPIO
from PIL import Image

camera = cv2.VideoCapture(0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

items = []

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
            if not symbol.data in items:
                items.append(symbol.data)

        # show the frame and record if the user presses a key
        cv2.imshow("Barcode Detection", frame)
            
        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        time.sleep(1)