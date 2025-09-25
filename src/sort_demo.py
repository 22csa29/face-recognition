import os
import sys
import cv2
import time
import sqlite3
import numpy as np
from datetime import datetime

# Add parent directory to path so sort_tracker can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sort_tracker.sort import Sort

# Video path
video_path = r"data\vedios\sample_video.mp4"

# Database path
db_path = r"faces.db"

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ensure tables exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS faces (
    face_id INTEGER PRIMARY KEY,
    timestamp TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS face_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    face_id INTEGER,
    event TEXT,
    timestamp TEXT,
    image_path TEXT
)
""")
conn.commit()

# Initialize tracker
tracker = Sort()
print(f"✅ Tracker created: {tracker}")

# Load YOLOv8-face model (assuming installed ultralytics)
from ultralytics import YOLO
model = YOLO("yolov8n-face.pt")
print("⚡ YOLOv8-face model loaded!")

# Open video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"❌ Cannot open video {video_path}")
    sys.exit(1)

print("🎥 Video opened successfully!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ End of video or cannot read the frame.")
        break

    # Run YOLO detection
    results = model(frame)[0]

    detections = []
    for box in results.boxes.xyxy:
        x1, y1, x2, y2 = map(int, box.tolist())
        detections.append([x1, y1, x2, y2, 1.0])  # confidence=1.0

    if len(detections) > 0:
        dets = np.array(detections)
        tracks = tracker.update(dets)
    else:
        tracks = []

    # Draw tracked boxes and log
    for trk in tracks:
        x1, y1, x2, y2, track_id = trk
        x1, y1, x2, y2, track_id = int(x1), int(y1), int(x2), int(y2), int(track_id)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Log to database
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT OR IGNORE INTO faces (face_id, timestamp) VALUES (?, ?)", (track_id, ts))

        face_crop = frame[y1:y2, x1:x2]
        log_folder = os.path.join("logs", "entries", datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(log_folder, exist_ok=True)
        image_path = os.path.join(log_folder, f"face_{track_id}_{int(time.time())}.jpg")
        cv2.imwrite(image_path, face_crop)
        cursor.execute("INSERT INTO face_logs (face_id, event, timestamp, image_path) VALUES (?, ?, ?, ?)",
                       (track_id, "entry", ts, image_path))

    conn.commit()

    # Display
    cv2.imshow("Face Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
print("🎬 Done!")
