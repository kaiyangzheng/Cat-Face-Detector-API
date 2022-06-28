"""
Returns binary image with detected faces drawn
"""
import cv2 as cv
import numpy as np

def detect_faces(image_data):
    # convert binary string to numpy array for opencv
    np_arr = np.fromstring(image_data, np.uint8)
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)

    # convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # read in haar cascade classifier
    haar_cascade = cv.CascadeClassifier('haarcascade_frontalcatface.xml')

    # detect faces
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)
    faces_found = len(faces_rect)
    print(f"Faces found: {len(faces_rect)}")

    # draw face rectangles on image
    for (x,y,w,h) in faces_rect:
        cv.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

    # convert numpy array to string
    img_str = cv.imencode('.jpg', img)[1].tostring()

    # np_arr = np.fromstring(img_str, np.uint8)
    # img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    # cv.imwrite('result.jpg', img)

    return img_str, faces_found