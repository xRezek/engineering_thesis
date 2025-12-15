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
  lower_red1 = np.array([0, 40, 120])
  upper_red1 = np.array([10, 255, 255]) 

  lower_red2 = np.array([170, 40, 120])
  uppper_red = np.array([180, 255, 255])

  mask_red1 = cv.inRange(hsv, lower_red1, upper_red1)
  mask_red2 = cv.inRange(hsv, lower_red2, uppper_red)

  lower_green = np.array([40, 100, 100])
  upper_green = np.array([70, 255, 255])
  
  lower_yellow = np.array([20, 100, 100])
  upper_yellow = np.array([30, 255, 255])

  mask_red = cv.bitwise_or(mask_red1, mask_red2)
  mask_green = cv.inRange(hsv, lower_green, upper_green)
  mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)

  result1 = cv.bitwise_or(frame1, frame1, mask=mask_red)

  # cv.imshow('smth', frame1)
  # cv.imshow('smth2', frame2)
  cv.imshow('Podglad', blank)
  cv.imshow('Podglad maski czerwonej', mask_red)
  cv.imshow('Podglad maski zielonej', mask_green)
  cv.imshow('Podglad maski kanarkowej', mask_yellow)
  cv.imshow('Rezultat1', result1)

  
  if cv.waitKey(1) == ord('q'):
    break

cap1.release()
cap2.release()
cv.destroyAllWindows()
  
