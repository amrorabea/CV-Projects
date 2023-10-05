import os
import cv2 as cv
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import numpy as np

input_dir = 'qrs'

for j in sorted(os.listdir(input_dir)):

    img = cv.imread(os.path.join(input_dir, j))
    qr_info = decode(img)

    # print(qr_info)
    for qr in qr_info:
        print(qr.data)
        rect = qr.rect
        polygon = qr.polygon
        img = cv.rectangle(img, (rect.left, rect.top), (rect.left+rect.width, rect.top+rect.height), (0, 255, 0), 5)
        img = cv.polylines(img, [np.array(polygon)], True, (255, 0, 0), 5)

        plt.figure()
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.show()

        # print(j, len(qr_info))  # shows how much qrs in the picture
