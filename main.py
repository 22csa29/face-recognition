import cv2
import face_recognition
import os
import sqlite3
from datetime import datetime

# -------- Database Setup --------
DB_NAME = "face_log.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id TEXT,
            timestamp TEXT,
            type TEXT,
            file_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_face():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (face_id, timestamp, type, file_path) VALUES (?, ?, ?, ?)",
                   ("temp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "entry", ""))
    face_id = cursor.lastrowid
    cursor.execute("UPDATE faces SET face_id = ? WHERE id = ?", (f"F{face_id:03}", face_id))
    conn.commit()
    conn.close()
    return f"F{face_id:03}"

def log_face(face_id, type, file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE faces SET type = ?, file_path = ?, timestamp = ? WHERE face_id = ?",
                   (type, file_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), face_id))
    conn.commit()
    conn.close()

# -------- Video Processing --------
def process_video(video_path):
    save_dir = f"logs/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(save_dir, exist_ok=True)

    known_encodings = []
    known_ids = []

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    frame_count = 0
    print("Processing video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        # Optionally, process every Nth frame to speed up
        if frame_count % 5 != 0:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            if True not in matches:
                # New unique face
                face_id = add_face()
                face_img = frame[top:bottom, left:right]
                file_path = os.path.join(save_dir, f"{face_id}_{int(datetime.now().timestamp())}.jpg")
                cv2.imwrite(file_path, face_img)
                log_face(face_id, "entry", file_path)
                known_encodings.append(face_encoding)
                known_ids.append(face_id)
                print(f"Captured unique face: {file_path}")

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Optional: Show video with rectangles
        # cv2.imshow("Video", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processing completed. {len(known_ids)} unique faces found.")

if __name__ == "__main__":
    init_db()
    video_file_path = "your_video.mp4"  # replace with your video file path
    process_video(video_file_path)
