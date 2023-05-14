import cv2, time
import pytesseract
import numpy as np
from typing import Callable
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO('yolov8n.yaml')
model = YOLO('yolov8n-pose.pt')
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class ResultShema():
    def __init__(self, is_man_exist, frame, keypoints):
        self.is_man_exist = is_man_exist
        self.frame = frame
        self.keypoints = keypoints

    is_man_exist:bool=False
    frame:np.ndarray
    keypoints:list=[]
    
def _clear_keypoints(keypoints:list):
    new_keypoints = []
    for kp in enumerate(keypoints):
        if kp[-1]>0.5:
            new_keypoints.append(kp)

def _clear_frame_by_keypoints(ann:Annotator, keypoints:list) -> np.ndarray:
    right_leck = []
    left_leck = []
    max_h = 720
    for i, kp in enumerate(keypoints):
        if kp[-1] >0.5:
            x = int(kp[0])
            y = int(kp[1])
            ann.text((x, y), str(i))
        if i == 5: right_leck = kp
        if i == 6: left_leck = kp
    if int(left_leck[1])> int(right_leck[1]):
        max_h = left_leck[1]-50
    else:
        max_h = right_leck[1]-50
    return ann.result()[int(max_h)::,int(left_leck[0])-50:int(right_leck[0])+50,:]

def predict_by_yolo(frame:np.ndarray) -> Results:
    return model(frame)

def start_find_people(iteration:int, on_unrecognize_callback:Callable) -> list[ResultShema]:
    result:list[ResultShema] = []
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while iteration > 0:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        res = predict_by_yolo(frame)
        keypoints:list = res[0].keypoints.squeeze().tolist()
        ann = Annotator(frame)
        #TODO fix this 
        #TODO 1+ man in frame
        iteration -= 1
        print('iteration: ', iteration)
        if len(keypoints) == 17:
            new_frame = _clear_frame_by_keypoints(ann, keypoints)
            try:
                result.append(ResultShema(True, new_frame, keypoints))
                cv2.imshow('Result', new_frame)
                print(pytesseract.image_to_string(frame, lang= 'rus'))
            except KeyError:
                result.append(ResultShema(False, ann.result(), []))
            
        else:
            result.append(ResultShema(False, ann.result(), []))
            on_unrecognize_callback()
        c = cv2.waitKey(1)
        if c == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return result