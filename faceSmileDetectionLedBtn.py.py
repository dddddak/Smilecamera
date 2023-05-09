from time import sleep
import RPi.GPIO as GPIO # LEDs and Button
import numpy as np
import cv2 # OpenCV

faceCascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
# Open face recognition file
smileCascade = cv2.CascadeClassifier('../haarcascades/haarcascade_smile.xml')
# Open smile recognition file
cap = cv2.VideoCapture(0) # for using video
cap.set(3,640) # set Width
cap.set(4,480) # set Height
nameDes = 'Photo' # file name to save the pictures
imgSmile_counter = 0
imgPress_counter = 0
# Count the number of the pictures taken
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT,initial=GPIO.LOW) #GREEN LED
GPIO.setup(38,GPIO.OUT,initial=GPIO.LOW) #RED LED
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Push Button

while True:
    GPIO.output(38,GPIO.HIGH)
    ret, img = cap.read()
#    img = cv2.flip(img, -1) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Change color of the video to black and white
    faces = faceCascade.detectMultiScale( # face recognition code
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        smile = smileCascade.detectMultiScale(
            # Smile recognition code in face recognition
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=15,
            minSize=(25, 25),
        )
        for i in smile:
            if len(smile)>1: # if the camera detect smiling face
                GPIO.output(38,GPIO.LOW) # turn off Red LED
                GPIO.output(40,GPIO.HIGH) # turn on Green LED
                sleep(2) # wait 2 seconds with the Green LED on
                GPIO.output(40,GPIO.LOW) # turn off Green LED
                GPIO.output(38,GPIO.HIGH) # turn on Red LED
#cv2.putText(img, "Smiling", (x,y-30), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3,cv2.LINE_AA)
                img_name = "../Desktop/"+ nameDes +"/imageSmile_{}.jpg".format(imgSmile_counter)
                # file path and file name to save photo when automated detection is working
                cv2.imwrite(img_name, img)
                print("{} written!".format(img_name))
                # display on the console so that user know the photo is taken
                imgSmile_counter += 1
#		sleep(0.1)

        for (xx, yy, ww, hh) in smile:
            cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)

    cv2.imshow('video',img) # video
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        GPIO.output(38,GPIO.LOW)
        break
    if k == 32 or GPIO.input(32) == GPIO.LOW : # press 'SPACE' or pushbutton to take a photo
        GPIO.output(38,GPIO.LOW) # Turn off Red LED
        GPIO.output(40,GPIO.HIGH) # Turn on Green LED
        sleep(2) # wait 2 seconds
        GPIO.output(40,GPIO.LOW) # Turn off Green LED
        sleep(1)
        GPIO.output(38,GPIO.HIGH) # Turn on Red LED
        img_name = "../Desktop/"+ nameDes +"/imagePress_{}.jpg".format(imgPress_counter)
        # file path and file name to save photos when user press pushbutton maually
        cv2.imwrite(img_name, img)
        print("{} written!".format(img_name)) # Display on the console so that know the photo is taken
        imgPress_counter += 1


cap.release()
cv2.destroyAllWindows()

