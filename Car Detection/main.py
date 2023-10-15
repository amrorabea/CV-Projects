import cv2 as cv
import numpy as np

cap = cv.VideoCapture('video.mp4')

algo = cv.bgsegm.createBackgroundSubtractorMOG()
count_line_pos = 550
min_width_react = 80
min_height_react = 80

while 1:
    ret, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (3, 3), 5)

    img_sub = algo.apply(blur)
    dilate = cv.dilate(img_sub, np.ones((5, 5)))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    dilatada = cv.morphologyEx(dilate, cv.MORPH_CLOSE, kernel)
    dilatada = cv.morphologyEx(dilatada, cv.MORPH_CLOSE, kernel)
    counterShape, _ = cv.findContours(dilatada, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.line(img, (25, count_line_pos), (1200, count_line_pos), (255, 127, 0), 3)

    for (i, c) in enumerate(counterShape):
        # for cnt in counterShape:
        (x, y, w, h) = cv.boundingRect(c)
            # print(cv.boundingRect(c))
        validate_counter = (w >= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue
        cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv.imshow('Vid', img)
    if cv.waitKey(1) == 13:
        break

cv.destroyAllWindows()
cap.release()
