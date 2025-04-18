import cv2
import pickle
import cvzone
import numpy as np
from cv2.gapi import kernel

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgProc):
    spacecnt = 0

    for pos in posList:
        x,y = pos

        imgCrop = imgProc[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)

        cnt = cv2.countNonZero(imgCrop) #count pixel
        # cvzone.putTextRect(img, str(cnt), (x,y+height-3), scale=1, thickness=2,
        #                    offset=0)

        if cnt < 1200:
            color = (0,255,0)
            thickness = 5
            spacecnt += 1
        else:
            color = (0,0,255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0]+width,pos[1]+height), color, thickness)
        cvzone.putTextRect(img, str(cnt), (x, y + height - 3), scale=1, thickness=2,
                           offset=0, colorR=color)


    cvzone.putTextRect(img, f'Free Spaces: {spacecnt}/{len(posList)}', (100, 50), scale=3, thickness=5,
                       offset=20, colorR=(0,200,0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): #current pos == total no of frame in video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY_INV, 25,16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)  #differentiate empty spaces
    kernel = np.ones((3,3), np.uint8)  # thicken lines
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)


    checkParkingSpace(imgDilate)
    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0]+width,pos[1]+height),(255,0,255),2)

    cv2.imshow("Image", img)
    # cv2.imshow("Image", imgBlur)
    # cv2.imshow("ImageT", imgThreshold)
    # cv2.imshow("ImageM", imgMedian)
    # cv2.imshow("ImageD", imgDilate)
    cv2.waitKey(10)