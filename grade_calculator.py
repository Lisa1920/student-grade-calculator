WEIGHTS = {
    "quiz": 0.10,
    "project": 0.20,
    "final_exam": 0.50,
    "practical": 0.20,
}


def safe_float(value):
    """Convert a mark to float. Empty values are treated as 0."""
    if value is None:
        return 0.0

    text = str(value).strip()
    if text == "":
        return 0.0

    return float(text)


def validate_mark(value, field_name):
    """Check that a mark is numeric and between 0 and 100."""
    mark = safe_float(value)

    if mark < 0 or mark > 100:
        raise ValueError(f"{field_name} must be between 0 and 100.")

    return mark


def calculate_final_grade(quiz, project, final_exam, practical):
    quiz_mark = validate_mark(quiz, "Quiz")
    project_mark = validate_mark(project, "Project")
    exam_mark = validate_mark(final_exam, "Final Exam")
    practical_mark = validate_mark(practical, "Practical")

    final_grade = (
        quiz_mark * WEIGHTS["quiz"]
        + project_mark * WEIGHTS["project"]
        + exam_mark * WEIGHTS["final_exam"]
        + practical_mark * WEIGHTS["practical"]
    )

    return round(final_grade, 2)


def get_performance_comment(final_grade):
    if final_grade >= 75:
        return "Distinction"
    if final_grade >= 50:
        return "Pass"
    return "Fail"


def calculate_record_grade(record):
    final_grade = calculate_final_grade(
        record.get("quiz", ""),
        record.get("project", ""),
        record.get("final_exam", ""),
        record.get("practical", ""),
    )

    record["final_grade"] = final_grade
    record["performance"] = get_performance_comment(final_grade)
    return record
