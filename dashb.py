# dashboard_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
from db_conn import create_connection
import pandas as pd
import warnings

sns.set_theme(style="whitegrid")

PASS_MARK = 40
MAX_MARKS = 100

# Suppress pandas UserWarning for non-SQLAlchemy connections
warnings.simplefilter(action='ignore', category=UserWarning)

class DashboardTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.create_ui()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="📊 Student Performance Dashboard",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#0D6EFD"
        ).pack(pady=15)

        # -------------------------
        # Filters
        # -------------------------
        filter_frame = tk.Frame(self.frame, bg="white")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Class:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=0, padx=5)
        self.class_filter = ttk.Combobox(filter_frame, width=15, font=("Segoe UI", 11))
        self.class_filter.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Subject:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=2, padx=5)
        self.subject_filter = ttk.Combobox(filter_frame, width=15, font=("Segoe UI", 11))
        self.subject_filter.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Exam:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=4, padx=5)
        self.exam_filter = ttk.Combobox(filter_frame, width=15, font=("Segoe UI", 11))
        self.exam_filter.grid(row=0, column=5, padx=5)

        tk.Button(
            filter_frame,
            text="Update Dashboard",
            bg="#0D6EFD",
            fg="white",
            font=("Segoe UI", 11),
            command=self.update_dashboard
        ).grid(row=0, column=6, padx=10)

        # -------------------------
        # Scrollable Graph Frame
        # -------------------------
        container = tk.Frame(self.frame, bg="white")
        container.pack(fill="both", expand=True, pady=20)

        self.canvas = tk.Canvas(container, bg="white")
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)

        self.graph_frame = tk.Frame(self.canvas, bg="white")
        self.graph_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.graph_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        self.load_filters()
        self.update_dashboard()

    # ---------------------------
    # Load filter options
    # ---------------------------
    def load_filters(self):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT CONCAT(class_name, ' ', section) FROM classes")
        classes = [row[0] for row in cursor.fetchall()]
        self.class_filter['values'] = ["All"] + classes
        self.class_filter.current(0)

        cursor.execute("SELECT subject_name FROM subjects")
        subjects = [row[0] for row in cursor.fetchall()]
        self.subject_filter['values'] = ["All"] + subjects
        self.subject_filter.current(0)

        cursor.execute("SELECT exam_name FROM exams")
        exams = [row[0] for row in cursor.fetchall()]
        self.exam_filter['values'] = ["All"] + exams
        self.exam_filter.current(0)

        conn.close()

    # ---------------------------
    # Fetch data from DB using original connection
    # ---------------------------
    def fetch_data(self):
        conn = create_connection()
        query = """
            SELECT s.student_id, s.name, c.class_name, c.section,
                   sub.subject_name, e.exam_name, m.marks_obtained
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            JOIN classes c ON s.class_id = c.class_id
            JOIN subjects sub ON m.subject_id = sub.subject_id
            JOIN exams e ON m.exam_id = e.exam_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    # ---------------------------
    # Update dashboard charts
    # ---------------------------
    def update_dashboard(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        df = self.fetch_data()
        if df.empty:
            messagebox.showinfo("No Data", "No data available.")
            return

        # ---------------------------
        # Apply Filters
        # ---------------------------
        cls = self.class_filter.get()
        sub = self.subject_filter.get()
        ex = self.exam_filter.get()

        if cls != "All":
            try:
                parts = cls.rsplit(' ', 1)
                class_name, section = parts[0], parts[1]
                df = df[(df['class_name'] == class_name) & (df['section'] == section)]
            except Exception:
                pass
        if sub != "All":
            df = df[df['subject_name'] == sub]
        if ex != "All":
            df = df[df['exam_name'] == ex]

        if df.empty:
            messagebox.showinfo("No Data", "No data available for selected filters.")
            return

        # ---------------------------
        # Figure size
        # ---------------------------
        fig_height = 7          # smaller height
        fig_width = 14          # smaller width
        fig, axs = plt.subplots(2, 3, figsize=(fig_width, fig_height))
        fig.subplots_adjust(hspace=0.5, wspace=0.3, bottom=0.1)

        # ---------------------------
        # 1. Average Marks by Subject
        # ---------------------------
        avg_subject = df.groupby('subject_name')['marks_obtained'].mean().reset_index()
        sns.barplot(
            x='subject_name', y='marks_obtained', data=avg_subject,
            ax=axs[0, 0],
            hue='subject_name', dodge=False,
            palette=sns.color_palette("Blues_d", len(avg_subject)),
            legend=False
        )
        axs[0, 0].set_title("Average Marks by Subject")
        axs[0, 0].set_ylabel("Avg Marks")
        axs[0, 0].set_ylim(0, MAX_MARKS)
        axs[0, 0].tick_params(axis='x', rotation=30)

        # ---------------------------
        # 2. Top 5 Students
        # ---------------------------
        top_students = df.groupby('name')['marks_obtained'].mean().nlargest(5).reset_index()
        sns.barplot(
            y='name', x='marks_obtained', data=top_students,
            ax=axs[0, 1],
            hue='name', dodge=False,
            palette=sns.color_palette("Greens_d", len(top_students)),
            legend=False
        )
        axs[0, 1].set_title("Top 5 Students")
        axs[0, 1].set_xlabel("Avg Marks")

        # ---------------------------
        # 3. Pass vs Fail Ratio
        # ---------------------------
        pass_count = df[df['marks_obtained'] >= PASS_MARK].shape[0]
        fail_count = df[df['marks_obtained'] < PASS_MARK].shape[0]
        axs[0, 2].pie(
            [pass_count, fail_count], labels=["Passed", "Failed"],
            autopct="%1.1f%%", colors=["#28a745", "#dc3545"], startangle=90
        )
        axs[0, 2].set_title("Pass vs Fail Ratio")

        # ---------------------------
        # 4. Exam-wise Average
        # ---------------------------
        exam_avg = df.groupby('exam_name')['marks_obtained'].mean().reset_index()
        sns.lineplot(
            x='exam_name', y='marks_obtained', data=exam_avg,
            marker="o", ax=axs[1, 0], color="#0D6EFD"
        )
        axs[1, 0].set_title("Average Marks by Exam")
        axs[1, 0].set_ylabel("Avg Marks")
        axs[1, 0].set_ylim(0, MAX_MARKS)
        axs[1, 0].tick_params(axis='x', rotation=30)

        # ---------------------------
        # 5. Marks Distribution
        # ---------------------------
        sns.histplot(
            df['marks_obtained'], bins=10, kde=True,
            ax=axs[1, 1], color="#6f42c1"
        )
        axs[1, 1].set_title("Marks Distribution")
        axs[1, 1].set_xlabel("Marks")
        axs[1, 1].set_ylabel("Number of Students")
        axs[1, 1].set_xlim(0, MAX_MARKS)

        # ---------------------------
        # 6. Subject-wise Avg per Class / All
        # ---------------------------
        sub_avg = df.groupby('subject_name')['marks_obtained'].mean().reset_index()
        sns.barplot(
            x='subject_name', y='marks_obtained', data=sub_avg,
            ax=axs[1, 2],
            hue='subject_name', dodge=False,
            palette=sns.color_palette("Oranges_d", len(sub_avg)),
            legend=False
        )
        axs[1, 2].set_title("Subject-wise Avg (All Classes)" if cls=="All" else "Subject-wise Avg for Class")
        axs[1, 2].set_ylabel("Avg Marks")
        axs[1, 2].set_ylim(0, MAX_MARKS)
        axs[1, 2].tick_params(axis='x', rotation=30)

        # ---------------------------
        # Render canvas
        # ---------------------------
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def get_frame(self):
        return self.frame
