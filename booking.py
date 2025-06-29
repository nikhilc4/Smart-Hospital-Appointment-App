try:
    import tkinter as tk
    from tkinter import Toplevel, messagebox
    import sqlite3
    from db import create_tables
    from email.mime.text import MIMEText
    import smtplib

    def send_email(to_email, patient_name, issue, doctor):
        try:
            sender_email = "nikhilchelkala@gmail.com"
            sender_password = "spda gtao zadd zuja"

            subject = "Appointment Confirmation - Smart Hospital"
            body = f"""
Hello {patient_name},

Your appointment with Dr. {doctor} has been successfully booked.
Issue: {issue}
Status: Waiting

Thank you,
Smart Hospital Appointment System
"""

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = to_email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()

            print("Email sent.")

        except Exception as e:
            print("Email failed:", e)

    def open_booking_ui():
        create_tables()
        win = Toplevel()
        win.title("Book Appointment")
        win.geometry("400x500")

        fields = {
            "Name": None,
            "Age": None,
            "Issue": None,
            "Doctor": None,
            "Date (YYYY-MM-DD)": None,
            "Time (HH:MM)": None,
            "Email": None
        }

        tk.Label(win, text="Appointment Booking", font=("Helvetica", 16, "bold")).pack(pady=10)

        entries = {}
        for label in fields:
            tk.Label(win, text=label).pack(pady=2)
            entry = tk.Entry(win, width=30)
            entry.pack(pady=2)
            entries[label] = entry

        def submit():
            conn = sqlite3.connect("hospital.db")
            cursor = conn.cursor()

            values = [entry.get() for entry in entries.values()]
            name, age, issue, doctor, date, time, email = values

            cursor.execute('''INSERT INTO patients (name, age, issue, doctor, date, time, email)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (name, age, issue, doctor, date, time, email))

            conn.commit()
            conn.close()

            send_email(email, name, issue, doctor)
            tk.Label(win, text="Appointment Booked!", fg="green").pack(pady=5)

        tk.Button(win, text="Book Now", command=submit, bg="#4CAF50", fg="white").pack(pady=10)

except ModuleNotFoundError as e:
    print("Error:", e)
    print("The 'tkinter' module is not installed or available in this environment. Please install it to run this application.")
