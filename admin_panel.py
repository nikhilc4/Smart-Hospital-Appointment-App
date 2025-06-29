import tkinter as tk
from tkinter import Toplevel, messagebox
import sqlite3

# Simple login check
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def open_admin_login():
    login_win = Toplevel()
    login_win.title("Admin Login")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Admin Login", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Label(login_win, text="Username").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login_win.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login_win, text="Login", command=attempt_login, bg="#2196F3", fg="white").pack(pady=10)

def open_admin_panel():
    win = Toplevel()
    win.title("Admin Panel - All Appointments")
    win.geometry("600x600")

    frame = tk.Frame(win)
    frame.pack(pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    appointments = cursor.fetchall()

    for appointment in appointments:
        id, name, age, issue, doctor, date, time, email, status = appointment
        frame_block = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=5, pady=5)
        frame_block.pack(fill="x", pady=3, padx=5)

        info = f"ID: {id} | Name: {name} | Issue: {issue} | Doctor: {doctor} | Date: {date} | Time: {time} | Status: {status}"
        tk.Label(frame_block, text=info, wraplength=550, justify="left").pack(anchor="w")

        def make_status_updater(app_id):
            return lambda: update_status(app_id)

        def make_deleter(app_id):
            return lambda: delete_appointment(app_id, win)

        tk.Button(frame_block, text="Mark Completed", bg="#4CAF50", fg="white", command=make_status_updater(id)).pack(side="left", padx=5)
        tk.Button(frame_block, text="Delete", bg="#F44336", fg="white", command=make_deleter(id)).pack(side="left")

    conn.close()

def update_status(app_id):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET status='completed' WHERE id=?", (app_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Status Updated", "Appointment marked as completed.")
    
def delete_appointment(app_id, win):
    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this appointment?")
    if confirm:
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (app_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Appointment deleted.")
        win.destroy()
        open_admin_panel()  # Reload
