import cv2 as cv
import mediapipe as mp


def process_img(img, face_detection):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)
    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box
            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
            x1 = int(x1 * W) - 30
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)
            # cv.rectangle(img, (x1, y1), (x1+w, y1+h), (0,255,0), 10)
            # # Blur the face
            img[y1:y1 + h, x1:x1 + w] = cv.blur(img[y1:y1 + h, x1:x1 + w], (30, 30))

    return img


cap = cv.VideoCapture(0)
W, H = 720, 480
cap.set(3, W)
cap.set(4, H)

while 1:
    # # Read Image
    ret, img = cap.read()

    # # Detect faces
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=0) as face_detection:
        img = process_img(img=img, face_detection=face_detection)

    cv.imshow('Image', img)
    cv.waitKey(25)
