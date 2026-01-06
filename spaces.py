from ultralytics import YOLO
import cv2 as cv


model = YOLO("my_model.pt")  


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    results = model(frame)

    
    annotated_frame = results[0].plot()  

   
    cv.imshow("YOLOv8 Detection", annotated_frame)

    if cv.waitKey(1) & 0xFF == 27:  # ESC 
        break

cap.release()
cv.destroyAllWindows()
