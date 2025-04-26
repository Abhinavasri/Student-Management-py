import cv2
import os
import csv
from datetime import datetime
from utils import detect_face

# Load recognizer and label map
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

with open("trainer/labels.txt", "r") as f:
    label_map = {int(k): v.strip() for k, v in (line.strip().split(",") for line in f)}

def mark_attendance(name):
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    file_path = f"attendance/{date_str}.csv"
    if not os.path.exists("attendance"):
        os.makedirs("attendance")
    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Time"])
    with open(file_path, "r") as f:
        if name in f.read():
            return  # already marked
    with open(file_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, time_str])
        print(f"{name} marked present at {time_str}")

def start_attendance():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        faces, gray = detect_face(frame)
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(face_img)
            if conf < 50:  # Confidence threshold
                name = label_map[id_]
                mark_attendance(name)
                label = f"{name} ({round(conf,2)})"
            else:
                label = "Unknown"
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_attendance()
