import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt    

img = cv.imread("Resources/Photos/park.jpg")
cv.imshow("Boston", img)

# hsv 

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow("HSV", hsv)

# lab
lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
cv.imshow("LAB", lab)

img_for_matplotlib = cv.cvtColor(img, cv.COLOR_BGR2RGB)
plt.imshow(img_for_matplotlib)
plt.show()

cv.waitKey(7000)
cv.destroyAllWindows()