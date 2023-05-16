import cv2
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results

# Load a model
model = YOLO('best.pt')


frame = cv2.imread('test3.jpeg')
frame = cv2.imread('test3.jpeg')
res:Results = model(frame)
results = model.predict(frame, save=False)
results_to_save = results[0].boxes.cpu().numpy()
print(results_to_save)