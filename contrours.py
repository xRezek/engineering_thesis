import cv2 as cv
import numpy as np

img = cv.imread("Resources/Photos/cats.jpg")
cv.imshow("Cats", img)

grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Grey", grey)

# blur
blur = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)
cv.imshow("Blur", blur)

#canny
canny = cv.Canny(blur, 125, 175)
cv.imshow("Canny", canny)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f"Number of contours found: {len(contours)}")


cv.waitKey(7000)
cv.destroyAllWindows()