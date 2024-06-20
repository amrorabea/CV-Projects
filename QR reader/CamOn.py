import cv2 as cv
from pyzbar.pyzbar import decode

cap = cv.VideoCapture(0)
results = []

while 1:
    _, frame = cap.read()
    qrs = decode(frame)

    if len(qrs) > 0:

        # Extract text from each qr appearing
        for qr in qrs:
            text_data = qr.data.decode("utf-8")  # Decode bytes to string
            if text_data not in results:
                results.append(text_data)
                print(text_data)
            data = qr.data
            rect = qr.rect

            # Drawings
            cv.putText(frame, data.decode(), (rect.left, rect.top - 15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            frame = cv.rectangle(frame, (rect.left, rect.top),
                                 (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 5)

    cv.imshow("Cam", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
