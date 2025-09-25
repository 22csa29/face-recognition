import cv2
import os
from datetime import datetime
from database import add_face, log_face

def capture_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    
    face_id = add_face()
    save_dir = f"logs/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(save_dir, exist_ok=True)
    
    print("Press 'q' to quit capturing faces.")

    captured = False
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
            if not captured:
                face_img = frame[y:y+h, x:x+w]
                file_path = os.path.join(save_dir, f"face_{face_id}_{int(datetime.now().timestamp())}.jpg")
                cv2.imwrite(file_path, face_img)
                log_face(face_id, "entry", file_path)
                captured = True  # Save only once per session
        cv2.imshow("Face Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
