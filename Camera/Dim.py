from picamera import PiCamera
import cv2
import numpy as np
import RPi.GPIO as GPIO 
from  picamera.array  import PiRGBArray
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 

GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18,GPIO.LOW) # Initial "Ok" low to inactive 
GPIO.output(13,GPIO.LOW)

F = 0

#scaling factor 
scaleA =26.10/484.368145113 
scaleB=26.10/484.368145113
cx= 0.00  #- offset x
cy= 0.09 #- offset y
#capture zone
capturemode=0 #0  No capture, 1 Capture



#Resolution zone
pixelblur0=11 #for Median Blur & Gausian Blur
pixelblur1=pixelblur0 #for Gausian Blur
edgesize=90  #for edge size
blurmethod=1 #0 Gausian, 1 Median,2 Bilateral Blur  5
def midpoint(ptA, ptB):
            return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

a=0

while (1):
    if (a==0):
        if (GPIO.input(21)==GPIO.HIGH):
            print("Initial for test")
            a=1
            okng=0 
        continue
   
    if (a==1):
        if (GPIO.input(21)==GPIO.LOW):
            print("Go Capturing")
            a=2
            s=0
        continue

    if(a==2):

        with PiCamera() as camera:
            resolution = (2592,1944)
            rawCapture = PiRGBArray(camera, size=(2592, 1944))
            camera.shutter_speed= 10000
            camera.iso=800
            camera.capture('/home/pi/Desktop/ngokcap00'+'.jpg')
            print("Capture")
            pass

        image0=cv2.imread("/home/pi/Desktop/ngokcap00.jpg")
        img0=image0
        image=img0

        gray=cv2.cvtColor(image0,cv2.COLOR_BGR2GRAY)

        if (blurmethod==0):
	        gray=cv2.GaussianBlur(gray, (pixelblur0,pixelblur1), cv2.BORDER_DEFAULT)
        if (blurmethod==1):
	        gray=cv2.medianBlur(gray,pixelblur0)
        canny = cv2.Canny(gray,5,300)
        dilate = cv2.dilate(canny,(1,1), iterations=2)

        edged = cv2.Canny(gray, edgesize,edgesize)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        edged3 = cv2.cvtColor(dilate, cv2.COLOR_GRAY2BGR)
        cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,
		      cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

            
        q=0
        for c in cnts:
            if cv2.contourArea(c) < 200:
                continue
         
            orig = image0.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
                
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (0, 0, 255), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (0, 0, 255), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (0, 0, 255), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (0, 0, 255), -1)
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			    (0, 255, 0), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			    (0, 255, 0), 2)
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            dimA = dA *scaleA + cx
            dimB = dB *scaleB + cy

            cv2.putText(orig, "X {:.2f} mm.".format(dimA),
                (int(20), int(60)), cv2.FONT_HERSHEY_SIMPLEX,
				2, (0, 255, 0), 4)

            cv2.putText(orig, "Y {:.2f} mm.".format(dimB),
                (int(20), int(140)), cv2.FONT_HERSHEY_SIMPLEX,
				2, (0, 255, 0), 4)

            cv2.putText(orig,"OK:" + str(F),
                (int(900), int(600)), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (0, 255, 0), 2)
        cv2.imshow("image",orig)
        cv2.waitKey(1000)
        piccount=piccount+1