import cv2 as cv
import numpy as np

img = cv.imread("./Resources/Photos/cat.jpg")
blank = np.zeros((500,500,3), dtype="uint8")
cv.imshow("Cat", img)
cv.imshow("dark", blank)

blank[200:300, 300:400] = 0,0,255
cv.imshow("red", blank)

cv.rectangle(blank, (0,0), (blank.shape[1]//2,blank.shape[0]//2), (0,255,0), thickness=cv.FILLED)
cv.imshow("rectangle", blank)


#koło

cv.circle(blank, (blank.shape[1]//2,blank.shape[0]//2), 40,(255,0,255), thickness=-1)
cv.imshow("circle", blank)

#linia

cv.line(blank, (0,0), (blank.shape[1]//2,blank.shape[0]//2), (255,0,0), thickness=2)
cv.imshow("line", blank)

#tekst

cv.putText(blank,"siema", (255,255), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
cv.imshow("text", blank)

cv.waitKey(5000)
cv.destroyAllWindows