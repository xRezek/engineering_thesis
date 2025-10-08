import cv2 as cv

img = cv.imread("Resources//Photos//cat_large.jpg")

cv.imshow("Kot", img)


def rescaleFrame(frame, scale=0.75):
  width = int(frame.shape[1] * 0.75)
  height = int(frame.shape[0] * 0.75)
  dimesnsions = (width, height)

  return cv.resize(frame, dimesnsions, interpolation=cv.INTER_AREA)

def changeResolution(width, height):
  vid.set(3, width)
  vid.set(4, height)

vid = cv.VideoCapture("Resources/Videos/dog.mp4")

while True:
  isTrue, frame = vid.read()

  frameResized = rescaleFrame(frame)

  cv.imshow("video", frame)
  cv.imshow("videoResized", frameResized)

  if cv.waitKey(20) & 0xff == ord('d'):
    break

vid.release()
cv.destroyAllWindows()

