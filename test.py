import cv2
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results

# Load a model
model = YOLO('best.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")
while True:
    ret, frame = cap.read()
    res:Results = model(frame)
    results = model.predict(frame, save=False)
    results_to_save = results[0].boxes.cpu().numpy()
    print(results_to_save)
    cv2.imshow('RES', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
cap.release()
cv2.destroyAllWindows()