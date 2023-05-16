import numpy as np


class ResultShema():
    def __init__(self, is_man_exist, frame, keypoints):
        self.is_man_exist = is_man_exist
        self.frame = frame
        self.keypoints = keypoints

    is_man_exist:bool=False
    frame:np.ndarray
    keypoints:list=[]