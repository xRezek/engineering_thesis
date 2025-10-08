import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


img = cv.imread("Resources/Photos/cats 2.jpg")
cv.imshow("Cats", img)

blank = np.zeros((img.shape[:2]), dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)

mask = cv.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, 255, -1)
cv.imshow("Mask", mask)


gray_hist = cv.calcHist([mask], [0], None, [256], [0,256])


plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of pixels")
plt.plot(mask)
plt.xlim([0,256])
plt.show()

cv.waitKey(7000)
cv.destroyAllWindows()