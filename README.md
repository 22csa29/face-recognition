# Intelligent Face Tracker with Auto-Registration and Visitor Counting

This project is an intelligent face tracking system that automatically registers new faces and counts unique visitors from a video stream.

## Architecture

```
[Video Source (File/RTSP)] -> [Frame Pre-processing]
                                     |
                                     v
                            +--------------------+
                            |   Face Detection   |
                            | (YOLOv8)           |
                            +--------------------+
                                     |
                                     v
                            +--------------------+
                            | Face Recognition   |
                            | (InsightFace)      |
                            +--------------------+
                                     |
                                     v
                            +--------------------+
                            |   Face Tracking    |
                            | (ByteTrack)        |
                            +--------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                                  SYSTEM                                 |
|-------------------------------------------------------------------------|
| - If new face -> Register (DB)                                          |
| - If known face -> Track                                                |
| - Log entry/exit events (DB, logs/events.log, logs/entries/)            |
| - Count unique visitors                                                 |
+-------------------------------------------------------------------------+

```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download models:**
   - YOLOv8 face model: [https://github.com/derronqi/yolov8-face](https://github.com/derronqi/yolov8-face)
   - InsightFace models will be downloaded automatically on first run.

4. **Configure `config.json`:**
   - Set `video_source` to your video file or `rtsp_stream` to your RTSP stream URL.

## How to Run

1. **With a sample video:**
   ```bash
   python main.py
   ```

2. **With an RTSP stream:**
   - In `config.json`, update the `rtsp_stream` URL.
   - In `main.py`, change the video source to use the RTSP stream.
   ```bash
   python main.py
   ```

## Sample `config.json`

```json
{
    "video_source": "data/sample.mp4",
    "rtsp_stream": "rtsp://your_rtsp_stream_url",
    "skip_frames": 5,
    "yolo_model": "yolov8n-face.pt",
    "insightface_model": "buffalo_l",
    "database": {
        "type": "sqlite",
        "path": "logs/database.db"
    },
    "tracker": "bytetrack"
}
```

## Database Schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    face_id TEXT NOT NULL UNIQUE,
    embedding BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    face_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- "entry" or "exit"
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_path TEXT,
    FOREIGN KEY (face_id) REFERENCES faces (face_id)
);
```

## Logging Format (`events.log`)

```
2025-09-23 10:00:00.123 | INFO     | __main__:main:50 - System started
2025-09-23 10:00:05.456 | INFO     | __main__:main:75 - DETECTED: 2 faces
2025-09-23 10:00:05.500 | SUCCESS  | __main__:main:80 - REGISTERED: new face with ID face_1
2025-09-23 10:00:10.200 | INFO     | __main__:main:90 - TRACKING: face_1
2025-09-23 10:05:00.000 | WARNING  | __main__:main:100 - EXIT: face_1
```

# Face Detection, Recognition & Tracking System

## Overview
This project implements a **real-time face detection, recognition, and tracking pipeline** using Python. It is designed for high accuracy in production-grade scenarios, integrating YOLO-based face detection, state-of-the-art face recognition (InsightFace), and tracking with OpenCV/DeepSort.  

The system automatically registers new faces, tracks them across frames, and maintains a unique visitor count, storing all metadata in a database with structured logs.

---

## Features

1. **Face Detection, Recognition & Tracking**
   - Real-time detection using YOLOv8.
   - Facial embeddings generated via **InsightFace** for high-accuracy recognition.
   - Automatic registration of new faces with unique IDs.
   - Detection + tracking logic to follow faces across frames.
   - Configurable frame skipping to optimize performance (`config.json`).

2. **Logging System**
   - Each face generates **one entry per frame** for entry and exit.
   - Logs include:
     - Cropped face image
     - Timestamp
     - Event type (entry/exit)
     - Face ID
   - Images stored in structured directories:  
     ```
     logs/entries/YYYY-MM-DD/
     logs/exits/YYYY-MM-DD/
     ```
   - All metadata stored in **SQLite database** (`face_log.db`).
   - `events.log` tracks all critical system events:
     - Face entry, recognition, tracking, exit
     - Embedding generation and registration

3. **Unique Visitor Counting**
   - Maintains an accurate count of unique faces.
   - Re-identification of a face does **not increment** the count.
   - Count retrievable from database or derived from logs.

---

## Tech Stack

| Module                | Technology                                   |
|-----------------------|---------------------------------------------|
| Face Detection        | YOLOv8                                      |
| Face Recognition      | InsightFace / ArcFace                        |
| Tracking              | OpenCV / DeepSort / ByteTrack                |
| Backend & Processing  | Python                                       |
| Database              | SQLite (or MongoDB/PostgreSQL optional)     |
| Configuration         | JSON (`config.json`)                         |
| Logging               | Log file + Local image store + Database      |
| Input                 | Video file / RTSP camera stream              |

---

## Project Structure

[2025-09-26 14:30:12] New face registered: F001
[2025-09-26 14:30:15] Face F001 entered frame
[2025-09-26 14:30:20] Face F002 entered frame
[2025-09-26 14:31:00] Face F001 exited frame


This project is a part of a hackathon run by https://katomaran.com
