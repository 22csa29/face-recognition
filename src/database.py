import sqlite3
from datetime import datetime

DB_PATH = "faces.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id INTEGER,
            action TEXT,
            timestamp TEXT,
            file_path TEXT,
            FOREIGN KEY(face_id) REFERENCES faces(id)
        )
    """)
    conn.commit()
    conn.close()

def add_face():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO faces (created_at) VALUES (?)", (now,))
    face_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return face_id

def log_face(face_id, action, file_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO face_logs (face_id, action, timestamp, file_path) VALUES (?, ?, ?, ?)",
        (face_id, action, now, file_path)
    )
    conn.commit()
    conn.close()

def view_faces():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faces")
    faces = cursor.fetchall()
    cursor.execute("SELECT * FROM face_logs")
    logs = cursor.fetchall()
    conn.close()
    return faces, logs
