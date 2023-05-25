import numpy as np
from enum import Enum

class MenStatus(Enum):
    steel_in_frame:str = "steel_in_frame"
    new_in_frame:str = "new_in_frame"
    gone:str = "gone"

class ResultSchema():
    def __init__(self, is_man_exist, frame, keypoints):
        self.is_man_exist = is_man_exist
        self.frame = frame
        self.keypoints = keypoints

    is_man_exist:bool=False
    frame:np.ndarray
    keypoints:list=[]
    similiar_to_exist_name:str = ''