import tkinter as tk
from tkinter import ttk, messagebox
from db_conn import create_connection

class MarksTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.frame, text="Manage Marks", fg="#0D6EFD", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)

        # --- Filter variables ---
        self.subject_var = tk.StringVar(value="All")
        self.exam_var = tk.StringVar(value="All")
        self.sort_var = tk.StringVar(value="ASC")
        self.search_var = tk.StringVar(value="")

        # --- DB function ---
        def fetch_marks(subject_filter=None, exam_filter=None, order="ASC", search_keyword=None):
            conn = create_connection()
            cursor = conn.cursor()
            query = """
                SELECT m.marks_id, s.name, sub.subject_name, e.exam_name, m.marks_obtained
                FROM marks m
                JOIN students s ON m.student_id = s.student_id
                JOIN subjects sub ON m.subject_id = sub.subject_id
                JOIN exams e ON m.exam_id = e.exam_id
            """
            filters = []
            values = []

            if subject_filter and subject_filter != "All":
                filters.append("sub.subject_name = %s")
                values.append(subject_filter)
            if exam_filter and exam_filter != "All":
                filters.append("e.exam_name = %s")
                values.append(exam_filter)
            if search_keyword:
                filters.append("(s.name LIKE %s OR s.student_id LIKE %s)")
                values.extend([f"%{search_keyword}%", f"%{search_keyword}%"])

            if filters:
                query += " WHERE " + " AND ".join(filters)

            query += f" ORDER BY m.marks_obtained {order}"
            cursor.execute(query, values)
            data = cursor.fetchall()
            conn.close()
            return data

        # --- Refresh table ---
        def refresh_table(event=None):
            rows = fetch_marks(
                subject_filter=self.subject_var.get(),
                exam_filter=self.exam_var.get(),
                order=self.sort_var.get(),
                search_keyword=self.search_var.get()
            )
            marks_table.delete(*marks_table.get_children())
            for r in rows:
                marks_table.insert("", "end", values=r)

        # --- Filter frame ---
        filter_frame = tk.Frame(self.frame, bg="white")
        filter_frame.pack(fill='x', pady=10)

        tk.Label(filter_frame, text="Filter by Subject:", bg="white").pack(side="left", padx=5)
        subject_cb = ttk.Combobox(filter_frame, values=["All", "DBMS", "OS", "PP", "DFS"], width=15, textvariable=self.subject_var, state="readonly")
        subject_cb.pack(side="left", padx=5)
        subject_cb.bind("<<ComboboxSelected>>", refresh_table)

        tk.Label(filter_frame, text="Exam:", bg="white").pack(side="left", padx=5)
        exam_cb = ttk.Combobox(filter_frame, values=["All", "Midterm", "Final"], width=15, textvariable=self.exam_var, state="readonly")
        exam_cb.pack(side="left", padx=5)
        exam_cb.bind("<<ComboboxSelected>>", refresh_table)

        # --- Sort frame ---
        sort_frame = tk.Frame(self.frame, bg="white")
        sort_frame.pack(fill='x', pady=(0,5), anchor='e')

        tk.Label(sort_frame, text="Sort by Marks:", bg="white").pack(side="left", padx=5)
        sort_order_cb = ttk.Combobox(sort_frame, values=["ASC", "DESC"], width=7, textvariable=self.sort_var, state="readonly")
        sort_order_cb.pack(side="left")
        sort_order_cb.bind("<<ComboboxSelected>>", refresh_table)

        # --- Search bar ---
        search_frame = tk.Frame(self.frame, bg="white")
        search_frame.pack(fill='x', pady=5)
        tk.Label(search_frame, text="Search:", bg="white").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, width=25, textvariable=self.search_var)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Go", command=refresh_table, bg="#0D6EFD", fg="white").pack(side="left", padx=5)

        # --- Marks table ---
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID", "Student", "Subject", "Exam", "Marks")
        marks_table = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            marks_table.heading(col, text=col)
            marks_table.column(col, anchor="center", width=150)
        marks_table.pack(fill="both", expand=True)

        # --- Load initial data ---
        refresh_table()

    def get_frame(self):
        return self.frame
