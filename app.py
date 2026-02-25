import tkinter as tk
from tkinter import ttk, messagebox
from db_conn import create_connection
from marks_tab import MarksTab
#from reports_tab import ReportsTab
from dashboard_tab import DashboardTab



# ---------------------------------
# Function to show Students Page
# ---------------------------------
def show_students(content_frame):
    # Clear previous widgets in content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Title Label
    tk.Label(content_frame, text="Manage Students", fg="#0D6EFD",
             font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)

    # ----- Database Functions -----
    def fetch_students(search_term=None):
        conn = create_connection()
        cursor = conn.cursor()

        if search_term:
            query = """SELECT student_id, name, dob, gender, contact, email, class_id
                       FROM students
                       WHERE name LIKE %s OR class_id LIKE %s"""
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        else:
            cursor.execute("SELECT student_id, name, dob, gender, contact, email, class_id FROM students")

        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert_student():
        name = name_entry.get()
        dob = dob_entry.get()
        gender = gender_cb.get()
        contact = contact_entry.get()
        email = email_entry.get()
        class_id = class_entry.get()

        if not name or not dob or not class_id:
            messagebox.showerror("Error", "Name, DOB, and Class ID are required!")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, dob, gender, contact, email, class_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, dob, gender, contact, email, class_id)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        refresh_table()

    def delete_student():
        selected = student_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a student to delete")
            return

        student_id = student_table.item(selected)['values'][0]
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Student record deleted.")
        refresh_table()

    def update_student():
        selected = student_table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a student to update")
            return

        student_id = student_table.item(selected)['values'][0]
        name = name_entry.get()
        dob = dob_entry.get()
        gender = gender_cb.get()
        contact = contact_entry.get()
        email = email_entry.get()
        class_id = class_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET name=%s, dob=%s, gender=%s, contact=%s, email=%s, class_id=%s
            WHERE student_id=%s
        """, (name, dob, gender, contact, email, class_id, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", "Student record updated.")
        refresh_table()

    def on_select(event):
        selected = student_table.focus()
        if not selected:
            return
        values = student_table.item(selected)['values']
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        dob_entry.delete(0, tk.END)
        dob_entry.insert(0, values[2])
        gender_cb.set(values[3])
        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, values[4])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[5])
        class_entry.delete(0, tk.END)
        class_entry.insert(0, values[6])

    def refresh_table(search_term=None):
        for row in student_table.get_children():
            student_table.delete(row)
        for row in fetch_students(search_term):
            student_table.insert("", "end", values=row)

    def search_student():
        term = search_entry.get()
        refresh_table(term)

    # ----- Form Frame -----
    form_frame = tk.Frame(content_frame, bg="#F8F9FA", padx=10, pady=10)
    form_frame.pack(fill='x')

    tk.Label(form_frame, text="Name:", bg="#F8F9FA").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="DOB (YYYY-MM-DD):", bg="#F8F9FA").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    dob_entry = tk.Entry(form_frame, width=20)
    dob_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Gender:", bg="#F8F9FA").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    gender_cb = ttk.Combobox(form_frame, values=["Male", "Female", "Other"], width=22)
    gender_cb.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Contact:", bg="#F8F9FA").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    contact_entry = tk.Entry(form_frame, width=20)
    contact_entry.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Email:", bg="#F8F9FA").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, width=25)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Class ID:", bg="#F8F9FA").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    class_entry = tk.Entry(form_frame, width=20)
    class_entry.grid(row=2, column=3, padx=5, pady=5)

    # Buttons
    add_btn = tk.Button(form_frame, text="Add Student", bg="#0D6EFD", fg="white",
                        font=("Segoe UI", 10, "bold"), command=insert_student)
    add_btn.grid(row=3, column=0, pady=10, padx=5)

    upd_btn = tk.Button(form_frame, text="Update Student", bg="#198754", fg="white",
                        font=("Segoe UI", 10, "bold"), command=update_student)
    upd_btn.grid(row=3, column=1, pady=10, padx=5)

    del_btn = tk.Button(form_frame, text="Delete Selected", bg="#DC3545", fg="white",
                        font=("Segoe UI", 10, "bold"), command=delete_student)
    del_btn.grid(row=3, column=2, pady=10, padx=5)

    # Search bar
    search_frame = tk.Frame(content_frame, bg="white")
    search_frame.pack(fill='x', pady=5)
    tk.Label(search_frame, text="Search:", bg="white").pack(side='left', padx=10)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side='left', padx=5)
    tk.Button(search_frame, text="Go", bg="#0D6EFD", fg="white", command=search_student).pack(side='left', padx=5)
    tk.Button(search_frame, text="Show All", bg="#6C757D", fg="white", command=lambda: refresh_table()).pack(side='left', padx=5)

    # ----- Table Frame -----
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)

    cols = ("ID", "Name", "DOB", "Gender", "Contact", "Email", "Class ID")
    student_table = ttk.Treeview(table_frame, columns=cols, show="headings")
    for col in cols:
        student_table.heading(col, text=col)
        student_table.column(col, anchor="center", width=130)

    student_table.bind("<<TreeviewSelect>>", on_select)
    student_table.pack(fill='both', expand=True)

    # Load initial data
    refresh_table()


# ---------------------------------
# Main Dashboard Layout
# ---------------------------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x700")
root.config(bg="#F8F9FA")

# Header
header = tk.Frame(root, bg="#0D6EFD", height=60)
header.pack(fill='x')

title = tk.Label(header, text="🎓 Student Management System",
                 font=("Segoe UI", 20, "bold"), bg="#0D6EFD", fg="white")
title.pack(pady=10)

# Sidebar
sidebar = tk.Frame(root, bg="#E9ECEF", width=220)
sidebar.pack(fill='y', side='left')

# Content
content = tk.Frame(root, bg="white")
content.pack(fill='both', expand=True)

# Navigation
def show_message(name):
    messagebox.showinfo("Navigation", f"You clicked {name}")

def show_home(content_frame):
    # Clear current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a dedicated frame for home page
    home_frame = tk.Frame(content_frame, bg="#ADD8E6")  # light blue
    home_frame.pack(fill='both', expand=True)

    # Large title
    title_lbl = tk.Label(
        home_frame,
        text="Welcome to Student Management Dashboard",
        font=("Segoe UI", 24, "bold"),
        bg="#ADD8E6",  # match frame
        fg="#0D6EFD"  # dark blue text
    )
    title_lbl.pack(pady=100)

    # Subtitle
    subtitle_lbl = tk.Label(
        home_frame,
        text="Manage Students, Marks, and Reports Easily",
        font=("Segoe UI", 16),
        bg="#ADD8E6",
        fg="#0D6EFD"  # dark blue text
    )
    subtitle_lbl.pack()

def show_marks(content_frame):
    # Clear current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create and pack the Marks tab
    marks_tab = MarksTab(content_frame)
    marks_tab.get_frame().pack(fill='both', expand=True)

# def show_reports(content_frame):
#     for widget in content_frame.winfo_children():
#         widget.destroy()

#     reports_tab = ReportsTab(content_frame)
#     reports_tab.get_frame().pack(fill='both', expand=True)

def show_reports(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    dashboard_tab = DashboardTab(content_frame)  # <-- Dashboard instead of Reports
    dashboard_tab.get_frame().pack(fill='both', expand=True)

# Sidebar menu items
menu_buttons = [
    ("🏠 Home", lambda: show_home(content)),
    ("👩‍🎓 Students", lambda: show_students(content)),
    ("🧮 Marks", lambda: show_marks(content)),
    ("📊 Reports", lambda: show_reports(content)),
    ("🏫 Classes", lambda: show_message("Classes")),
    ("📚 Subjects", lambda: show_message("Subjects")),
    ("⚙️ Settings", lambda: show_message("Settings")),
]

for text, command in menu_buttons:
    btn = tk.Button(sidebar, text=text, font=("Segoe UI", 12), bg="#E9ECEF",
                    bd=0, relief="flat", anchor='w', padx=20, command=command)
    btn.pack(fill='x', pady=5)

# Default Content
# welcome_lbl = tk.Label(content, text="Welcome to Student Management Dashboard",
#                        font=("Segoe UI", 16), bg="white", fg="#212529")
# welcome_lbl.pack(pady=50)
show_home(content)
root.mainloop()
