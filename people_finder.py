import ctypes
import cv2, time
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO('yolov8n-pose.pt')

def start_find_people():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    iteration = 5
    while iteration > 0:
        time.sleep(0.5)
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        res:Results = model(frame) 
        keypoints = res[0].keypoints.squeeze().tolist()
        ann = Annotator(frame)
        right_leck = []
        left_leck = []
        max_h = 720
        #TODO fix this
        iteration = iteration - 1
        print('iteration: ', iteration)
        if len(keypoints) == 17:
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
            try:
                print(max_h)
                cv2.imshow('Input',ann.result()[int(max_h)::,int(left_leck[0])-50:int(right_leck[0])+50,:])
            except:
                pass
        else:
            ctypes.windll.user32.LockWorkStation()

        c = cv2.waitKey(1)
        if c == 27:
            break
    cap.release()
    cv2.destroyAllWindows()