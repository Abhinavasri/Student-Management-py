import cv2
import os
from utils import detect_face

def register_student(name):
    cam = cv2.VideoCapture(0)
    count = 0
    save_path = os.path.join("data", name)
    os.makedirs(save_path, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        faces, gray = detect_face(frame)
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{save_path}/{name}_{count}.jpg", face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Registering...", frame)
        if cv2.waitKey(1) == 27 or count >= 30:  # ESC to stop or 30 samples
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"Registered {count} face samples for {name}")

if __name__ == "__main__":
    student_name = input("Enter student name: ")
    register_student(student_name)
