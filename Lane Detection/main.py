import sys

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def make_coordinates(img, line_parameters):
    slope, intercept = line_parameters
    y1 = img.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


def average_slope_intercept(img, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(img, left_fit_average)
    right_line = make_coordinates(img, right_fit_average)
    return np.array([left_line, right_line])


def canny(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    canny = cv.Canny(blur, 50, 150)
    return canny


def display_lines(img, lines):
    line_img = np.zeros_like(img)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_img


def region_of_interest(img):
    height = img.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(img)
    cv.fillPoly(mask, polygons, 255)
    masked_img = cv.bitwise_and(img, mask)
    return masked_img


# img = cv.imread('test_image.jpg')
# lane_img = np.copy(img)
# canny_img = canny(lane_img)
# cropped_img = region_of_interest(canny_img)
# lines = cv.HoughLinesP(cropped_img, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(lane_img, lines)
# line_img = display_lines(lane_img, averaged_lines)
# combo_img = cv.addWeighted(lane_img, 0.8, line_img, 1, 1)
# cv.imshow('img', line_img)
# cv.waitKey(0)

cap = cv.VideoCapture('test2.mp4')
while (cap.isOpened()):
    _, img = cap.read()
    canny_img = canny(img)
    cropped_img = region_of_interest(canny_img)
    lines = cv.HoughLinesP(cropped_img, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(img, lines)
    line_img = display_lines(img, averaged_lines)
    combo_img = cv.addWeighted(img, 0.8, line_img, 1, 1)
    cv.imshow('img', combo_img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()
cap.release()
sys.exit()
