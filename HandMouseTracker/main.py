import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

###########################
wCam, hCam = 640, 480
frameR = 100
smoothening = 10
###########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
clicked = False

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

while 1:
    _, frame = cap.read()
    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        xchk, ychk = lmList[7][1:]

        fingers = detector.fingersUp()
        cv.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        length, frame, lineInfo = detector.findDistance(4, 5, frame)
        if length < 40:
            cv.circle(frame, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv.FILLED)
            if not clicked:
                if x1 == xchk and y1 == ychk:
                    print('.')
                else:
                    pyautogui.leftClick()
                    clicked = True
        else:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX)
            clocY = plocY + (y3 - plocY)

            pyautogui.moveTo(wScr - clocX, clocY)
            cv.circle(frame, (x1, y1), 15, (255, 0, 255), cv.FILLED)
            plocX, plocY = clocX, clocY
            clicked = False

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(frame, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv.imshow("Camera", frame)
    cv.waitKey(1)
