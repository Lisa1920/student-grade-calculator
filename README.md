# Student Grade Calculator

A Python desktop application for recording assessment marks, validating student records, calculating weighted results, and reviewing records through a Tkinter interface.

This is a cleaned portfolio copy of a coursework project. The assessment-specific report generator was omitted, and the sample records use clearly fictional demo data. The application source was otherwise retained from the recovered project.

## Features

- Create, view, search, update, and delete student records in a CSV file.
- Validate required fields and mark ranges from 0 to 100.
- Calculate a weighted final grade and classify the result as Distinction, Pass, or Fail.
- Run the calculation unit tests with Python's built-in `unittest` framework.

## Grade calculation

| Assessment component | Weight |
| --- | ---: |
| Quiz | 10% |
| Project | 20% |
| Final examination | 50% |
| Practical | 20% |

```text
Final grade = quiz × 0.10 + project × 0.20 + final exam × 0.50 + practical × 0.20
```

The application treats blank marks as zero. Results of 75 or above are classified as Distinction, results from 50 to below 75 as Pass, and results below 50 as Fail.

## Requirements

- Python 3
- Tkinter, included with most standard Python installations

## Run

```bash
python3 main.py
```

On first launch, the application creates `students.csv` with fictional demo records. The CSV is local runtime data and is excluded from this repository. Keep real student information out of public repositories.

Run the existing calculation tests with:

```bash
python3 -m unittest discover -s tests -v
```

The private recovery archive recorded nine existing calculation tests as passing on 12 November 2026. They were not rerun while preparing this portfolio copy; GUI behaviour has not been reverified here.

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | Tkinter desktop interface and application navigation |
| `data_module.py` | CSV persistence, input validation, search, update, and deletion operations |
| `grade_calculator.py` | Mark validation, weighted grade calculation, and result classification |
| `tests/test_grade_calculator.py` | Existing unit tests for grade calculations |

## Provenance and scope

The application was developed as coursework and is presented here as a student portfolio example. It is an educational record-management demonstration, not a production student information system. The CSV file has no authentication, encryption, or multi-user access controls.
