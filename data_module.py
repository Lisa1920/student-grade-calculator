import csv
import os

from grade_calculator import calculate_record_grade, validate_mark


CSV_FILE = "students.csv"

FIELDNAMES = [
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
]


def create_csv_if_missing(file_path=CSV_FILE):
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
            writer.writeheader()


def validate_student_record(record):
    required_fields = ["student_id", "student_name", "module_code", "module_name"]

    for field in required_fields:
        if str(record.get(field, "")).strip() == "":
            raise ValueError(f"{field.replace('_', ' ').title()} cannot be empty.")

    validate_mark(record.get("quiz", ""), "Quiz")
    validate_mark(record.get("project", ""), "Project")
    validate_mark(record.get("final_exam", ""), "Final Exam")
    validate_mark(record.get("practical", ""), "Practical")


def read_students(file_path=CSV_FILE):
    try:
        create_csv_if_missing(file_path)

        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            students = []

            for row in reader:
                try:
                    students.append(calculate_record_grade(row))
                except ValueError:
                    row["final_grade"] = "Invalid"
                    row["performance"] = "Invalid record"
                    students.append(row)

            return students

    except FileNotFoundError:
        return []
    except PermissionError:
        print("The CSV file cannot be opened because permission was denied.")
        return []
    except csv.Error as error:
        print(f"CSV file error: {error}")
        return []


def save_all_students(students, file_path=CSV_FILE):
    create_csv_if_missing(file_path)

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for student in students:
            writer.writerow({field: student.get(field, "") for field in FIELDNAMES})


def add_student(record, file_path=CSV_FILE):
    validate_student_record(record)
    record = calculate_record_grade(record)
    create_csv_if_missing(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writerow({field: record.get(field, "") for field in FIELDNAMES})


def search_students(search_text, file_path=CSV_FILE):
    search_text = search_text.lower().strip()
    students = read_students(file_path)

    return [
        student
        for student in students
        if search_text in student.get("student_id", "").lower()
        or search_text in student.get("student_name", "").lower()
        or search_text in student.get("module_code", "").lower()
    ]


def delete_student(student_id, module_code, file_path=CSV_FILE):
    students = read_students(file_path)
    updated_students = [
        student
        for student in students
        if not (
            student.get("student_id") == student_id
            and student.get("module_code") == module_code
        )
    ]

    save_all_students(updated_students, file_path)
    return len(students) != len(updated_students)


def update_student(student_id, module_code, new_record, file_path=CSV_FILE):
    validate_student_record(new_record)
    students = read_students(file_path)
    updated = False

    for index, student in enumerate(students):
        if student.get("student_id") == student_id and student.get("module_code") == module_code:
            students[index] = calculate_record_grade(new_record)
            updated = True
            break

    if updated:
        save_all_students(students, file_path)

    return updated


def create_sample_data(file_path=CSV_FILE):
    if os.path.exists(file_path):
        return

    sample_students = [
        {
            "student_id": "demo-001",
            "student_name": "Example Student One",
            "module_code": "JAVA",
            "module_name": "Java Programming",
            "quiz": "75",
            "project": "50",
            "final_exam": "88",
            "practical": "65",
        },
        {
            "student_id": "demo-002",
            "student_name": "Example Student Two",
            "module_code": "DBS",
            "module_name": "Database Systems",
            "quiz": "52",
            "project": "68",
            "final_exam": "38",
            "practical": "95",
        },
        {
            "student_id": "demo-003",
            "student_name": "Example Student Three",
            "module_code": "CPP",
            "module_name": "C++ Programming",
            "quiz": "65",
            "project": "85",
            "final_exam": "78",
            "practical": "85",
        },
        {
            "student_id": "demo-004",
            "student_name": "Example Student Four",
            "module_code": "NET",
            "module_name": "Networks",
            "quiz": "90",
            "project": "95",
            "final_exam": "48",
            "practical": "95",
        },
    ]

    create_csv_if_missing(file_path)
    for student in sample_students:
        add_student(student, file_path)
