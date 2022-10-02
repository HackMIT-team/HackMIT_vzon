import numpy as np
import cv2 as cv

cam = cv.VideoCapture(0)
while True:
    _, frame = cam.read()

    cv.imshow('window', frame)

    lap = cv.Laplacian(frame, cv.CV_16S)
    lap = np.uint8(lap)

    cv.imshow('Laplacian', lap)
    
  
    edges = cv.Canny(frame, 180, 200)
    cv.imshow('Canny', edges)
    if cv.waitKey(5) ==  ord('x'):
        break

cam.release()
cv.destroyAllWindows()