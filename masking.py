import cv2 as cv
import numpy as np

img = cv.imread("Resources/Photos/cats.jpg")
cv.imshow("Cats", img)

blank = np.full((img.shape[0], img.shape[1]), 255, dtype='uint8')
cv.imshow("Blank", blank)

mask = cv.circle(blank, (img.shape[1]//2, img.shape[0]//2), 50, 0, -1)
cv.imshow("Mask", mask)

masked = cv.bitwise_and(img, img, mask=mask)
cv.imshow("Masked", masked)


cv.waitKey(7000)
cv.destroyAllWindows()