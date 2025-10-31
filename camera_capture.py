import cv2 as cv
import numpy as np

cap1 = cv.VideoCapture(0)
cap2 = cv.VideoCapture(1)

ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()
print(len(frame1))
print(frame2.shape)


while True:
  ret1, frame1 = cap1.read()
  ret2, frame2 = cap2.read()
  
  height1 = int(cap1.get(4)) 
  height2 = int(cap2.get(4)) 

  width1 = int(cap1.get(3))
  width2 = int(cap2.get(3))
  
  blank = np.zeros((len(frame1), len(frame1[0])*2, len(frame1[0][0])), np.uint8)

  rotated_frame1 = cv.rotate(frame1,cv.ROTATE_180)
  rotated_frame2 = cv.rotate(frame2,cv.ROTATE_180)


  font = cv.FONT_HERSHEY_SIMPLEX
  
  rotated_frame1 = cv.putText(rotated_frame1, "Prawa", (20, 40), font, 1, (255, 255, 255), 1, cv.LINE_AA, False)
  rotated_frame2 = cv.putText(rotated_frame2, "Lewa", (20, 40), font, 1, (255, 255, 255), 1, cv.LINE_AA, False)


  # cv.imshow('rotated_frame1', rotated_frame1)
  # cv.imshow('rotated_frame2', rotated_frame2)

  blank[:height2, :width2] = rotated_frame2
  blank[:height2, width2:] = rotated_frame1

  hsv = cv.cvtColor(rotated_frame1, cv.COLOR_BGR2HSV)
  lower_red = np.array([0, 100, 100])
  uppper_red = np.array([10, 255, 255])

  mask = cv.inRange(hsv, lower_red, uppper_red)

  result1 = cv.bitwise_or(frame1, frame1, mask=mask)

  # cv.imshow('smth', frame1)
  # cv.imshow('smth2', frame2)
  cv.imshow('Podglad', blank)
  cv.imshow('Podglad maski', mask)
  cv.imshow('Rezultat1', result1)

  
  if cv.waitKey(1) == ord('q'):
    break

cap1.release()
cap2.release()
cv.destroyAllWindows()
  
