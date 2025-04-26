# dashboard.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog


def generate_dashboard():
    attendance_dir = 'attendance'
    if not os.path.exists(attendance_dir):
        print("No attendance records found.")
        return

    all_records = pd.DataFrame()
    for file in os.listdir(attendance_dir):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(attendance_dir, file))
            all_records = pd.concat([all_records, df], ignore_index=True)

    if all_records.empty:
        print("No attendance data to visualize.")
        return

    summary = all_records['Name'].value_counts()

    # Bar chart
    summary.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Attendance Count per Student')
    plt.xlabel('Student Name')
    plt.ylabel('Attendance Days')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    generate_dashboard()
