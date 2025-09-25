import requests

# URL of the YOLOv8 small model
url = "https://huggingface.co/ultralytics/yolov8/resolve/main/yolov8n.pt"

# Save the file directly as yolov8n-face.pt
with open("yolov8n-face.pt", "wb") as f:
    f.write(requests.get(url).content)

print("Download complete! File saved as yolov8n-face.pt in this folder.")
