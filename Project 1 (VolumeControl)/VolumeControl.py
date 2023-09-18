import sys

import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math

CamWidth, CamHeight = 640, 480

vid = cv.VideoCapture(0)
vid.set(3, CamWidth)
vid.set(4, CamHeight)

prevTime = 0
detector = htm.handDetector(detectionCon=0.7)

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-1, None)
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
volPer = 0

while 1:
    success, img = vid.read()

    detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1+y2)//2

        cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        vol = np.interp(length, [20, 150], [minVol, maxVol])
        volBar = np.interp(length, [20, 150], [400, 150])
        volPer = np.interp(length, [20, 150], [0, 100])
        print(length, vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv.circle(img, (cx, cy), 15, (255, 255, 255), cv.FILLED)
    cv.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv.FILLED)


    curTime = time.time()
    fps = 1/(curTime-prevTime)
    prevTime = curTime

    cv.putText(img, f'FPS: {int(fps)}', (40, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
    cv.putText(img, f'Volume: {int(volPer)}', (40, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv.imshow('Img', img)
    cv.waitKey(1)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
sys.exit()
