# gui.py
import tkinter as tk
from tkinter import messagebox
import subprocess


def register_student():
    subprocess.run(["python", "register.py"])


def train_model():
    subprocess.run(["python", "train_model.py"])


def start_attendance():
    subprocess.run(["python", "attendance_system.py"])


def show_dashboard():
    subprocess.run(["python", "dashboard.py"])


root = tk.Tk()
root.title("Student Attendance System")
root.geometry("400x300")

tk.Label(root, text="Attendance System", font=("Arial", 18)).pack(pady=20)

btn_register = tk.Button(root, text="Register New Student", command=register_student, width=25)
btn_register.pack(pady=5)

btn_train = tk.Button(root, text="Train Face Model", command=train_model, width=25)
btn_train.pack(pady=5)

btn_attendance = tk.Button(root, text="Start Attendance", command=start_attendance, width=25)
btn_attendance.pack(pady=5)

btn_dashboard = tk.Button(root, text="View Attendance Dashboard", command=show_dashboard, width=25)
btn_dashboard.pack(pady=5)

root.mainloop()
