try:
    import tkinter as tk
    from tkinter import Toplevel
    import sqlite3

    def open_doctor_ui():
        win = Toplevel()
        win.title("Doctor Panel")
        win.geometry("500x500")

        tk.Label(win, text="Appointments for Doctor", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame = tk.Frame(win)
        frame.pack(pady=10)

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name, issue, time, date FROM patients WHERE status='waiting'")
        appointments = cursor.fetchall()

        if appointments:
            for row in appointments:
                info = f"Name: {row[0]} | Issue: {row[1]} | Time: {row[2]} | Date: {row[3]}"
                tk.Label(frame, text=info, wraplength=450, font=("Helvetica", 10)).pack(anchor="w", pady=2)
        else:
            tk.Label(frame, text="No appointments yet.", fg="gray").pack()

        conn.close()

except ModuleNotFoundError as e:
    print("Error:", e)
    print("The 'tkinter' module is not installed or available in this environment. Please install it to run this application.")
