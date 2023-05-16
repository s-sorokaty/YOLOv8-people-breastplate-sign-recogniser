import pytesseract
import numpy as np
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def recognize_at_frame(frame:np.ndarray) -> str:
    #resized_frame = cv2.resize(frame, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
    #resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    resized_frame =frame
    cv2.imwrite('test1234.jpg', resized_frame)
    return pytesseract.image_to_string(resized_frame, lang= 'rus')

print(recognize_at_frame(cv2.imread("result_haaf.jpg")))