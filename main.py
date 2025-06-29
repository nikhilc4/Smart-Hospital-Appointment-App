try:
    import tkinter as tk
    from tkinter import Toplevel, messagebox
    from PIL import Image, ImageTk
    from booking import open_booking_ui
    from doctor_panel import open_doctor_ui
    from admin_panel import open_admin_login  # Admin login added

    def open_main_ui():
        win = tk.Tk()
        win.title("Smart Hospital System")
        win.geometry("450x450")
        win.resizable(False, False)

        try:
            logo_img = Image.open("logo.png")
            logo_img = logo_img.resize((100, 100), Image.LANCZOS)
            logo = ImageTk.PhotoImage(logo_img)
            tk.Label(win, image=logo).pack(pady=10)
            win.logo = logo
        except:
            pass

        tk.Label(win, text="Smart Hospital", font=("Helvetica", 20, "bold")).pack(pady=5)

        tk.Button(win, text="Book Appointment", command=open_booking_ui, width=25, bg="#4CAF50", fg="white").pack(pady=15)
        tk.Button(win, text="Doctor Panel", command=open_doctor_ui, width=25, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(win, text="Admin Panel", command=open_admin_login, width=25, bg="#f57c00", fg="white").pack(pady=5)  # Admin

        win.mainloop()

    open_main_ui()

except ModuleNotFoundError as e:
    print("Error:", e)
    print("The 'tkinter' module is not installed or available in this environment. Please install it to run this application.")
