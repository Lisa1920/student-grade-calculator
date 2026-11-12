import tkinter as tk
from tkinter import messagebox, ttk

from data_module import (
    add_student,
    create_sample_data,
    delete_student,
    read_students,
    search_students,
    update_student,
)


BACKGROUND = "#dff3ff"
PINK = "#f8b4d9"
LIGHT_GREEN = "#b7efc5"
DARK_TEXT = "#16324f"
SOFT_WHITE = "#f8fcff"


class StudentGradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Calculator")
        self.root.geometry("900x560")
        self.root.configure(bg=BACKGROUND)

        create_sample_data()
        self.selected_student = None
        self.setup_styles()

        self.show_main_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=SOFT_WHITE,
            fieldbackground=SOFT_WHITE,
            foreground=DARK_TEXT,
            rowheight=26,
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=LIGHT_GREEN,
            foreground=DARK_TEXT,
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", PINK)])

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()

        title = tk.Label(
            self.root,
            text="Student Grade Calculator",
            font=("Arial", 22, "bold"),
            bg=BACKGROUND,
            fg=DARK_TEXT,
        )
        title.pack(pady=35)

        button_frame = tk.Frame(self.root, bg=BACKGROUND)
        button_frame.pack(pady=10)

        buttons = [
            ("Capture Student Marks", self.show_capture_window),
            ("View / Delete Student Records", self.show_view_window),
            ("Search / Update Records", self.show_search_window),
            ("Close Program", self.root.destroy),
        ]

        for index, (text, command) in enumerate(buttons):
            button_colour = PINK if index % 2 == 0 else LIGHT_GREEN
            tk.Button(
                button_frame,
                text=text,
                command=command,
                width=34,
                height=2,
                font=("Arial", 12),
                bg=button_colour,
                fg=DARK_TEXT,
                activebackground=LIGHT_GREEN if button_colour == PINK else PINK,
                activeforeground=DARK_TEXT,
            ).pack(pady=8)

    def make_form(self, parent, values=None):
        values = values or {}
        fields = [
            ("student_id", "Student ID"),
            ("student_name", "Student Name"),
            ("module_code", "Module Code"),
            ("module_name", "Module Name"),
            ("quiz", "Quiz Mark"),
            ("project", "Project Mark"),
            ("final_exam", "Final Exam Mark"),
            ("practical", "Practical Mark"),
        ]

        entries = {}
        form_frame = tk.Frame(parent, bg=BACKGROUND)
        form_frame.pack(pady=12)

        for row_number, (field, label_text) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text,
                width=18,
                anchor="w",
                bg=BACKGROUND,
                fg=DARK_TEXT,
                font=("Arial", 11),
            ).grid(row=row_number, column=0, padx=8, pady=6)

            entry = tk.Entry(form_frame, width=34, font=("Arial", 11), bg=SOFT_WHITE, fg=DARK_TEXT)
            entry.grid(row=row_number, column=1, padx=8, pady=6)
            entry.insert(0, values.get(field, ""))
            entries[field] = entry

        return entries

    def get_form_values(self, entries):
        return {field: entry.get().strip() for field, entry in entries.items()}

    def show_capture_window(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Capture Student Marks",
            font=("Arial", 18, "bold"),
            bg=BACKGROUND,
            fg=DARK_TEXT,
        ).pack(pady=18)

        entries = self.make_form(self.root)

        def save_record():
            try:
                add_student(self.get_form_values(entries))
                messagebox.showinfo("Saved", "Student record was saved successfully.")
                self.show_main_menu()
            except ValueError as error:
                messagebox.showerror("Invalid Data", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Record could not be saved: {error}")

        tk.Button(self.root, text="Save Record", command=save_record, width=18, bg=LIGHT_GREEN, fg=DARK_TEXT).pack(pady=8)
        tk.Button(self.root, text="Back to Menu", command=self.show_main_menu, width=18, bg=PINK, fg=DARK_TEXT).pack(pady=4)

    def setup_tree(self, parent):
        columns = (
            "student_id",
            "student_name",
            "module_code",
            "module_name",
            "quiz",
            "project",
            "final_exam",
            "practical",
            "final_grade",
            "performance",
        )

        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        headings = {
            "student_id": "Student ID",
            "student_name": "Name",
            "module_code": "Module",
            "module_name": "Module Name",
            "quiz": "Quiz",
            "project": "Project",
            "final_exam": "Exam",
            "practical": "Practical",
            "final_grade": "Final %",
            "performance": "Performance",
        }

        widths = {
            "student_id": 85,
            "student_name": 130,
            "module_code": 80,
            "module_name": 140,
            "quiz": 55,
            "project": 65,
            "final_exam": 65,
            "practical": 75,
            "final_grade": 70,
            "performance": 95,
        }

        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, width=widths[column], anchor="center")

        tree.pack(padx=14, pady=10, fill="both", expand=True)
        return tree

    def load_tree_data(self, tree, records):
        for row in tree.get_children():
            tree.delete(row)

        for record in records:
            tree.insert(
                "",
                "end",
                values=(
                    record.get("student_id", ""),
                    record.get("student_name", ""),
                    record.get("module_code", ""),
                    record.get("module_name", ""),
                    record.get("quiz", ""),
                    record.get("project", ""),
                    record.get("final_exam", ""),
                    record.get("practical", ""),
                    record.get("final_grade", ""),
                    record.get("performance", ""),
                ),
            )

    def show_view_window(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="View and Delete Student Records",
            font=("Arial", 18, "bold"),
            bg=BACKGROUND,
            fg=DARK_TEXT,
        ).pack(pady=14)

        tree = self.setup_tree(self.root)
        self.load_tree_data(tree, read_students())

        def delete_selected():
            selected_item = tree.focus()
            if selected_item == "":
                messagebox.showwarning("No Selection", "Please select a student record first.")
                return

            values = tree.item(selected_item, "values")
            confirmed = messagebox.askyesno("Confirm Delete", "Do you want to delete this record?")

            if confirmed:
                was_deleted = delete_student(values[0], values[2])
                if was_deleted:
                    messagebox.showinfo("Deleted", "The record was deleted.")
                    self.load_tree_data(tree, read_students())
                else:
                    messagebox.showerror("Error", "The selected record could not be found.")

        button_frame = tk.Frame(self.root, bg=BACKGROUND)
        button_frame.pack(pady=8)
        tk.Button(button_frame, text="Delete Selected", command=delete_selected, width=18, bg=PINK, fg=DARK_TEXT).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="Back to Menu", command=self.show_main_menu, width=18, bg=LIGHT_GREEN, fg=DARK_TEXT).grid(row=0, column=1, padx=6)

    def show_search_window(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Search and Update Records",
            font=("Arial", 18, "bold"),
            bg=BACKGROUND,
            fg=DARK_TEXT,
        ).pack(pady=14)

        search_frame = tk.Frame(self.root, bg=BACKGROUND)
        search_frame.pack(pady=6)

        tk.Label(search_frame, text="Search:", bg=BACKGROUND, fg=DARK_TEXT, font=("Arial", 11)).grid(row=0, column=0, padx=6)
        search_entry = tk.Entry(search_frame, width=34, font=("Arial", 11), bg=SOFT_WHITE, fg=DARK_TEXT)
        search_entry.grid(row=0, column=1, padx=6)

        tree = self.setup_tree(self.root)
        self.load_tree_data(tree, read_students())

        def run_search():
            self.load_tree_data(tree, search_students(search_entry.get()))

        def open_update_form():
            selected_item = tree.focus()
            if selected_item == "":
                messagebox.showwarning("No Selection", "Please select a student record first.")
                return

            values = tree.item(selected_item, "values")
            record = {
                "student_id": values[0],
                "student_name": values[1],
                "module_code": values[2],
                "module_name": values[3],
                "quiz": values[4],
                "project": values[5],
                "final_exam": values[6],
                "practical": values[7],
            }

            self.show_update_window(record)

        button_frame = tk.Frame(self.root, bg=BACKGROUND)
        button_frame.pack(pady=8)

        tk.Button(search_frame, text="Search", command=run_search, width=12, bg=PINK, fg=DARK_TEXT).grid(row=0, column=2, padx=6)
        tk.Button(button_frame, text="Update Selected", command=open_update_form, width=18, bg=LIGHT_GREEN, fg=DARK_TEXT).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="Show All", command=lambda: self.load_tree_data(tree, read_students()), width=18, bg=PINK, fg=DARK_TEXT).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="Back to Menu", command=self.show_main_menu, width=18, bg=LIGHT_GREEN, fg=DARK_TEXT).grid(row=0, column=2, padx=6)

    def show_update_window(self, old_record):
        self.clear_window()

        tk.Label(
            self.root,
            text="Update Student Record",
            font=("Arial", 18, "bold"),
            bg=BACKGROUND,
            fg=DARK_TEXT,
        ).pack(pady=18)

        entries = self.make_form(self.root, old_record)

        def save_update():
            try:
                new_record = self.get_form_values(entries)
                was_updated = update_student(
                    old_record["student_id"],
                    old_record["module_code"],
                    new_record,
                )

                if was_updated:
                    messagebox.showinfo("Updated", "The student record was updated.")
                    self.show_search_window()
                else:
                    messagebox.showerror("Error", "The record could not be updated.")
            except ValueError as error:
                messagebox.showerror("Invalid Data", str(error))
            except Exception as error:
                messagebox.showerror("Error", f"Update failed: {error}")

        tk.Button(self.root, text="Save Update", command=save_update, width=18, bg=LIGHT_GREEN, fg=DARK_TEXT).pack(pady=8)
        tk.Button(self.root, text="Back to Search", command=self.show_search_window, width=18, bg=PINK, fg=DARK_TEXT).pack(pady=4)


if __name__ == "__main__":
    window = tk.Tk()
    app = StudentGradeApp(window)
    window.mainloop()
