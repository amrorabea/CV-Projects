import os
import cv2 as cv
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np


cap = cv.VideoCapture(0)

while 1:
    ret, img = cap.read()


    qr_info = decode(img)
    if len(qr_info) > 0:
        qr = qr_info[0]
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon
        print(data, type(data))
        cv.putText(img, data.decode(), (rect.left, rect.top - 15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        img = cv.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 5)
        img = cv.polylines(img, [np.array(polygon)], True, (255, 0, 0), 5)

    cv.imshow("Cam", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
