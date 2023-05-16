import cv2
import numpy as np
import recognise_text
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
from models import ResultShema

# Load a model
model = YOLO('sign_detection.pt')

def _crop_frame_by_boxes(frame:np.ndarray, boxes:list) -> np.ndarray:
    boxes = boxes[0].boxes[0]
    print('HERE', [int(boxes[0]),int(boxes[2]),int(boxes[1]),int(boxes[3])], boxes.shape)
    print('frame info: ', frame.shape)
    frame = frame[int(boxes[1]):int(boxes[3]), int(boxes[0]):int(boxes[2]),:]
    print('frame info: ', frame.shape)
    return frame

def find_sign(in_data:list[ResultShema]):
    for data in in_data:
        results = model.predict(data.frame, save=False)
        results_to_save = results[0].boxes.cpu().numpy()
        if results[0].boxes:
            croped_frame = _crop_frame_by_boxes(data.frame, results_to_save)
            print("recognized_text: ", recognise_text.recognize_at_frame(croped_frame))
            cv2.imwrite('res.jpg', croped_frame)
            #cv2.imshow('RES', croped_frame)

#frame = cv2.imread('t6.PNG')
#results = model.predict(frame, save=False)
#results_to_save = results[0].boxes.cpu().numpy()
#if results[0].boxes:
#    croped_frame = _crop_frame_by_boxes(frame, results_to_save)
#    print("recognized_text: ", recognise_text.recognize_at_frame(croped_frame))
#    cv2.imwrite('res.jpg', croped_frame)