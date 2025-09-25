import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "faces.db")

# Connect to the database (will create if not exists)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS faces")
cursor.execute("DROP TABLE IF EXISTS face_logs")

# Create faces table with timestamp column
cursor.execute("""
CREATE TABLE faces (
    face_id TEXT PRIMARY KEY,
    timestamp TEXT
)
""")

# Create face_logs table with all necessary fields
cursor.execute("""
CREATE TABLE face_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    face_id TEXT,
    event_type TEXT,
    timestamp TEXT,
    image_path TEXT,
    FOREIGN KEY(face_id) REFERENCES faces(face_id)
)
""")

conn.commit()
conn.close()

print("✅ Database 'faces.db' created with tables: faces, face_logs")
