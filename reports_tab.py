# reports_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db_conn import create_connection
import numpy as np

class ReportsTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.create_ui()

    def create_ui(self):
        tk.Label(self.frame, text="📊 Reports Dashboard", font=("Segoe UI", 18, "bold"), bg="white", fg="#0D6EFD").pack(pady=15)

        # Dropdown and button
        top_frame = tk.Frame(self.frame, bg="white")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Select Report:", bg="white", font=("Segoe UI", 11)).pack(side="left", padx=10)

        self.report_type = ttk.Combobox(top_frame, values=[
            "Average Marks by Subject",
            "Top 5 Students (Overall Avg)",
            "Pass vs Fail Ratio"
        ], font=("Segoe UI", 11), width=30)
        self.report_type.current(0)
        self.report_type.pack(side="left", padx=10)

        tk.Button(top_frame, text="Show Report", bg="#0D6EFD", fg="white", font=("Segoe UI", 11),
                  command=self.show_report).pack(side="left", padx=10)

        self.graph_frame = tk.Frame(self.frame, bg="white")
        self.graph_frame.pack(fill="both", expand=True, pady=20)

    # ---------------------------
    # Database Fetch Functions
    # ---------------------------
    def fetch_avg_marks(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sub.subject_name, ROUND(AVG(m.marks_obtained), 2)
            FROM marks m
            JOIN subjects sub ON m.subject_id = sub.subject_id
            GROUP BY sub.subject_name
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    def fetch_top_students(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, ROUND(AVG(m.marks_obtained), 2) as avg_marks
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            GROUP BY s.name
            ORDER BY avg_marks DESC
            LIMIT 5
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    def fetch_pass_fail(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN m.marks_obtained >= 40 THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN m.marks_obtained < 40 THEN 1 ELSE 0 END) as failed
            FROM marks m
        """)
        result = cursor.fetchone()
        conn.close()
        return result

    # ---------------------------
    # Chart Rendering
    # ---------------------------
    def show_report(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        choice = self.report_type.get()

        try:
            if choice == "Average Marks by Subject":
                data = self.fetch_avg_marks()
                subjects, averages = zip(*data)
                ax.bar(subjects, averages, color="#0D6EFD")
                ax.set_title("Average Marks by Subject")
                ax.set_ylabel("Average Marks")
                ax.set_ylim(0, 100)

            elif choice == "Top 5 Students (Overall Avg)":
                data = self.fetch_top_students()
                names, avgs = zip(*data)
                ax.barh(names, avgs, color="#198754")
                ax.set_title("Top 5 Students (Overall Average)")
                ax.invert_yaxis()

            elif choice == "Pass vs Fail Ratio":
                passed, failed = self.fetch_pass_fail()
                labels = ["Passed", "Failed"]
                ax.pie([passed, failed], labels=labels, autopct="%1.1f%%",
                       colors=["#28a745", "#dc3545"], startangle=90)
                ax.set_title("Pass vs Fail Ratio")

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report:\n{e}")

    def get_frame(self):
        return self.frame
