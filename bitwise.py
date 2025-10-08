import cv2 as cv
import numpy as np

blank = np.zeros((400, 400), dtype='uint8')


rectangle = cv.rectangle(blank.copy(), (30, 30), (370, 370), 255, -1)
circle = cv.circle(blank.copy(), (200, 200), 200, 255, -1)

cv.imshow("Rectangle", rectangle)
cv.imshow("Circle", circle)

biwise_and = cv.bitwise_and(rectangle, circle)
cv.imshow("Bitwise AND", biwise_and)

biwise_or = cv.bitwise_or(rectangle, circle)
cv.imshow("Bitwise OR", biwise_or)

biwise_xor = cv.bitwise_xor(rectangle, circle)
cv.imshow("Bitwise XOR", biwise_xor)

bitwise_nand = cv.bitwise_not(biwise_and)
cv.imshow("Bitwise NAND", bitwise_nand)

bitwise_nxor = cv.bitwise_not(biwise_xor)
cv.imshow("Bitwise NXOR", bitwise_nxor)

cv.waitKey(7000)
cv.destroyAllWindows()