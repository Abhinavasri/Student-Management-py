import smtplib
from email.message import EmailMessage

def send_email_alert(to_email, student_name):
    sender = "your_email@gmail.com"
    password = "your_app_password"  # Use Gmail App Password or SMTP creds

    msg = EmailMessage()
    msg['Subject'] = f"Attendance Alert: {student_name}"
    msg['From'] = sender
    msg['To'] = to_email
    msg.set_content(f"{student_name} has been marked present today.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
