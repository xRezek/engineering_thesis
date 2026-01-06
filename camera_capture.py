import cv2 as cv
import numpy as np
import mediapipe as mp

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
  
  lookahead = np.zeros((len(frame1), len(frame1[0])*2, len(frame1[0][0])), np.uint8)

  rotated_frame1 = cv.rotate(frame1,cv.ROTATE_180)
  rotated_frame2 = cv.rotate(frame2,cv.ROTATE_180)


  font = cv.FONT_HERSHEY_SIMPLEX
  
  rotated_frame1 = cv.putText(rotated_frame1, "Prawa", (20, 40), font, 1, (255, 255, 255), 1, cv.LINE_AA, False)
  rotated_frame2 = cv.putText(rotated_frame2, "Lewa", (20, 40), font, 1, (255, 255, 255), 1, cv.LINE_AA, False)


  # cv.imshow('rotated_frame1', rotated_frame1)
  # cv.imshow('rotated_frame2', rotated_frame2)

  lookahead = cv.hconcat([rotated_frame2, rotated_frame1])

  # grey = cv.cvtColor(rotated_frame1, cv.COLOR_BGR2GRAY)
  
  hsv = cv.cvtColor(rotated_frame2, cv.COLOR_BGR2HSV)
  lower = (0, 0, 200)
  upper = (180, 40, 255)
  mask = cv.inRange(hsv, lower, upper)

  kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
  mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

  contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  c = max(contours, key=cv.contourArea)

  cv.drawContours(rotated_frame2, [c], -1, (0,255,0), 2)

  # cv.imshow('smth', frame1)
  # cv.imshow('smth2', frame2)
  cv.imshow('test', rotated_frame2)
  cv.imshow('hsv', hsv)
  cv.imshow('Podglad', lookahead)


  
  if cv.waitKey(1) == ord('q'):
    break

cap1.release()
cap2.release()
cv.destroyAllWindows()
  
