import cv2, time
import numpy as np
from typing import Callable
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils.plotting import Annotator
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    res:Results = model(frame)
    print(res[0].masks.numpy())
    cv2.imshow('Result', res[0].masks.numpy())
    c = cv2.waitKey(1)
    if c == 27:
        break
    cap.release()
    cv2.destroyAllWindows()