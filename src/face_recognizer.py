import insightface
from insightface.app import FaceAnalysis
import numpy as np

class FaceRecognizer:
    def __init__(self, model_name='buffalo_l'):
        self.app = FaceAnalysis(name=model_name)
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def get_embedding(self, face_image):
        faces = self.app.get(face_image)
        if faces:
            return faces[0].normed_embedding
        return None

    def compare_faces(self, emb1, emb2, threshold=0.6):
        # Cosine similarity
        sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return sim > threshold
