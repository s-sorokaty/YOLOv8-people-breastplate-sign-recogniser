import cv2
import difflib
import numpy as np
import recognise_text
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
from models import ResultSchema
from haaf_image_rotator import rotate_image
# Load a model
model = YOLO('sign_detection.pt')

def _crop_frame_by_boxes(frame:np.ndarray, boxes:list) -> np.ndarray:
    boxes = boxes[0].boxes[0]
    frame = frame[int(boxes[1]):int(boxes[3]), int(boxes[0]):int(boxes[2]),:]
    return frame

def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()

def find_sign(in_data:list[ResultSchema], names:list[str]):
    for data in in_data:
        results = model.predict(data.frame, conf=0.5, save=False)
        results_to_save = results[0].boxes.cpu().numpy()
        if results[0].boxes:
            croped_frame = _crop_frame_by_boxes(data.frame, results_to_save)
            croped_frame = rotate_image(croped_frame)
            recognized_string =  recognise_text.recognize_at_frame(croped_frame)
            print("recognized_text: ", recognized_string)
            cv2.imwrite('res.jpg', croped_frame)
            for name in names: 
                print("similar %: ", similarity(name, recognized_string))
                if similarity(name, recognized_string) > 0.7:
                    data.similiar_to_exist_name = name