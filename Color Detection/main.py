import cv2 as cv
from PIL import Image
from util import get_limits

cap = cv.VideoCapture(0)
yellow = [0, 255, 255]

while 1:
    ret, img = cap.read()

    hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower, upper = get_limits(color=yellow)

    mask = cv.inRange(hsvImg, lower, upper)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv.imshow("Image", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
