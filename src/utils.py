import cv2
import numpy as np

def draw_bounding_box(frame, box, label, color):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

def crop_face(frame, box):
    x1, y1, x2, y2 = box
    return frame[y1:y2, x1:x2]
