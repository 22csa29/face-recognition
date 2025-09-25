from loguru import logger
import os
from datetime import datetime

def setup_logger():
    log_path = "logs/events.log"
    logger.add(log_path, rotation="10 MB", retention="10 days", level="INFO")
    return logger

def save_cropped_face(face_image, face_id):
    today = datetime.now().strftime("%Y-%m-%d")
    save_dir = os.path.join("logs", "entries", today)
    os.makedirs(save_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H-%M-%S-%f")
    filename = f"{face_id}_{timestamp}.jpg"
    save_path = os.path.join(save_dir, filename)
    
    # Assuming face_image is a numpy array (OpenCV format)
    import cv2
    cv2.imwrite(save_path, face_image)
    
    return save_path
