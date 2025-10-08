import cv2 as cv

img = cv.imread("Resources/Photos/park.jpg")
cv.imshow("Park", img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)


#blur

blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
cv.imshow("blur", blur)

#wykrywanie krawędzi

canny = cv.Canny(blur, 125, 175)
cv.imshow("canny edges",canny)

#rozszerzanie obrazu

dilated = cv.dilate(canny, (3,3), iterations=7)
cv.imshow("dilated", dilated)

#?erozja

eroded = cv.erode(dilated, (3,3), iterations=1)
cv.imshow("eroded", eroded)

#przycinanie
cropped = img[20:300, 200:400]
cv.imshow("cropped", cropped)



cv.waitKey(7000)
cv.destroyAllWindows