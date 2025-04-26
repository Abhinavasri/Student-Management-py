import cv2
import numpy as np
import os
from datetime import datetime
import pandas as pd

def mark_attendance(name):
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"attendance/{date_str}.csv"
    time_str = datetime.now().strftime('%H:%M:%S')

    if not os.path.exists("attendance"):
        os.makedirs("attendance")

    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if name in df['Name'].values:
            return
    else:
        df = pd.DataFrame(columns=['Name', 'Time', 'Date'])

    new_row = {'Name': name, 'Time': time_str, 'Date': date_str}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filename, index=False)

def recognize_faces():
    # Ensure necessary folders exist
    for folder in ['dataset', 'trainer', 'attendance']:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Load recognizer and trained data
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_path = 'trainer/trainer.yml'

    if not os.path.exists(model_path):
        print("[ERROR] Trained model not found. Run train_model.py first.")
        return

    recognizer.read(model_path)

    # Load Haar cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Build label → name map based on dataset filenames
    names = {}
    label_id = 1
    seen_names = set()
    for file in os.listdir('dataset'):
        if file.endswith('.jpg'):
            name = file.split('.')[0]
            if name not in seen_names:
                names[label_id] = name
                seen_names.add(name)
                label_id += 1

    print("[INFO] Starting face recognition. Press 'Q' to quit.")

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(face)

            if confidence < 50:
                name = names.get(id_, "Unknown")
                mark_attendance(name)
                label = f"{name} ({round(confidence, 2)}%)"
            else:
                label = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), font, 0.8, (255, 255, 255), 2)

        cv2.imshow('Attendance - Press Q to quit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("[INFO] Attendance session ended.")

if __name__ == '__main__':
    recognize_faces()
