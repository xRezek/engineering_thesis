import cv2 as cv
import mediapipe as mp


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,                
    min_detection_confidence=0.7,   
    min_tracking_confidence=0.5     
)


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break


    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)


    results = hands.process(rgb)


    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:

        mp_drawing.draw_landmarks(
          frame,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS
        )

    cv.imshow("MediaPipe Hands Detection", frame)

    if cv.waitKey(1) & 0xFF == 27:
      break

cap.release()
cv.destroyAllWindows()
