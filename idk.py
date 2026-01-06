import cv2 as cv

# inicjalizacja kamer
cap1 = cv.VideoCapture(0)  # kamera 1
cap2 = cv.VideoCapture(1)  # kamera 2

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    # przetwarzanie obu klatek tu
    # np. wykrywanie obiektów YOLO na obu kamerach

    # wyświetlanie obok siebie
    combined = cv.hconcat([cv.rotate(frame2, cv.ROTATE_180), cv.rotate(frame1, cv.ROTATE_180)])
    cv.imshow("Dual Camera View", combined)

    if cv.waitKey(1) & 0xFF == 27:  # ESC aby wyjść
        break

cap1.release()
cap2.release()
cv.destroyAllWindows()