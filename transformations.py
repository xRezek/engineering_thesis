import cv2 as cv
import numpy as np

img = cv.imread("Resources/Photos/park.jpg")
cv.imshow("Park", img)


def translate (img, x, y):
  transMat = np.float32([[1,0,x], [0,1,y]])
  dimensions = (img.shape[1], img.shape[0])
  return cv.warpAffine(img, transMat, dimensions)

translated = translate(img, -100,-100)
cv.imshow("Tranformation", translated)

# resize
rezized = cv.resize(img, (500, 500), interpolation=cv.INTER_CUBIC)
cv.imshow("Rezised", rezized)

#flip
flip = cv.flip(img, 1)  # 0 = vertical, 1 = horizontal, -1 = both
cv.imshow("Flipped", flip)

# Crop
cropped = img[200:400, 300:500] # y1:y2, x1:x2
cv.imshow("Cropped", cropped) 

cv.waitKey(7000)  
cv.destroyAllWindows