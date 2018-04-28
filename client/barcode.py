import numpy as np
import cv2
import time
import sys
import zbar
from PIL import Image

def detect(image):
	# convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction
	gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
	gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
 
	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)
 
	# blur and threshold the image
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
 
	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
 
	# perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations = 4)
	closed = cv2.dilate(closed, None, iterations = 4)
 
	# find the contours in the thresholded image
	(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	# if no contours were found, return None
	if len(cnts) == 0:
		return np.int0([]);
 
	# otherwise, sort the contours by area and compute the rotated
	# bounding box of the largest contour
	c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	rect = cv2.minAreaRect(c)
	box = np.int0(cv2.boxPoints(rect))
 
	# return the bounding box of the barcode
	return box

camera = cv2.VideoCapture(0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

# keep looping over the frames
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
        
        # detect the barcode in the image
        box = detect(frame)
        
        if box.size > 0:
            # if a barcode was found, draw a bounding box on the frame
            cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        
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
        
	# show the frame and record if the user presses a key
	cv2.imshow("Barcode Detection", frame)
        
	# if the 'q' key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()