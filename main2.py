# main2.py
import cv2
import pickle
import cvzone
import numpy as np
import json
import time

# constants for area 2
VIDEO_FILE    = 'carPark2.mp4'
POS_FILE      = 'CarParkPos1'
AREA_ID       = 2
JSON_PATH     = 'free_space_counts.json'
WIDTH_L,HEIGHT_L = 105, 45
WIDTH_P,HEIGHT_P = 45,  95
THRESH        = 900
IMG_WIDTH,IMG_HEIGHT = 864, 513

def update_space_count(area_id, count):
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[str(area_id)] = count
    with open(JSON_PATH, 'w') as f:
        json.dump(data, f)

with open(POS_FILE, 'rb') as f:
    posList = pickle.load(f)

cap = cv2.VideoCapture(VIDEO_FILE)

def checkParkingSpace(imgProc, imgDisplay):
    spacecnt = 0
    for pos in posList:
        if len(pos) == 2:
            x, y = pos; ptype = 'landscape'
        else:
            x, y, ptype = pos

        w,h = (WIDTH_L,HEIGHT_L) if ptype=='landscape' else (WIDTH_P,HEIGHT_P)
        imgCrop = imgProc[y:y+h, x:x+w]
        cnt = cv2.countNonZero(imgCrop)
        if cnt < THRESH:
            color, thickness = (0,255,0), 5
            spacecnt += 1
        else:
            color, thickness = (0,0,255), 2

        cv2.rectangle(imgDisplay, (x, y), (x + w, y + h), color, thickness)
        cvzone.putTextRect(imgDisplay, str(cnt),
                           (x + 5, y + h - 10),
                           scale=1, thickness=2,
                           offset=0, colorR=color)

    cvzone.putTextRect(imgDisplay,
                       f'Free Spaces: {spacecnt}/{len(posList)}',
                       (100, 50), scale=3, thickness=5,
                       offset=20, colorR=(0, 200, 0))
    return spacecnt

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        time.sleep(0.1)

    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    gray      = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur      = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh    = cv2.adaptiveThreshold(blur, 255,
                   cv2.ADAPTIVE_THRESH_MEAN_C,
                   cv2.THRESH_BINARY_INV, 25, 16)
    median    = cv2.medianBlur(thresh, 5)
    dilate    = cv2.dilate(median, np.ones((3, 3), np.uint8), iterations=1)

    free = checkParkingSpace(dilate, img)
    update_space_count(AREA_ID, free)

    cv2.imshow("Area 2", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
