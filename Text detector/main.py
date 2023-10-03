import cv2 as cv
import easyocr
import matplotlib.pyplot as plt

# # Read image
image_path = 'image.png'
img = cv.imread(image_path)

# # Instance text detector
reader = easyocr.Reader(['en'])

# # Detect text on image
text_ = reader.readtext(img)
for t in text_:
    bbox, text, score = t
    print(text)
    cv.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)

plt.imshow(img)
plt.show()
