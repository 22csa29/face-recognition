from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_faces(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = box
                detections.append((int(x1), int(y1), int(x2), int(y2)))
        return detections
