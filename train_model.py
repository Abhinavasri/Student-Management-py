import cv2
import numpy as np
import os
from utils import detect_face

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    for student_name in os.listdir("data"):
        student_path = os.path.join("data", student_name)
        if not os.path.isdir(student_path):
            continue
        label_map[label_id] = student_name
        for img_name in os.listdir(student_path):
            img_path = os.path.join(student_path, img_name)
            image = cv2.imread(img_path)
            _, gray = detect_face(image)
            face = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face)
            labels.append(label_id)
        label_id += 1

    recognizer.train(faces, np.array(labels))
    recognizer.save("trainer/trainer.yml")

    # Save label map
    with open("trainer/labels.txt", "w") as f:
        for k, v in label_map.items():
            f.write(f"{k},{v}\n")

    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
