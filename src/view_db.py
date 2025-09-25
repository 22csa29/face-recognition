from database import view_faces

faces, logs = view_faces()

print("=== Faces Table ===")
for f in faces:
    print(f)

print("\n=== Face Logs Table ===")
for l in logs:
    print(l)
