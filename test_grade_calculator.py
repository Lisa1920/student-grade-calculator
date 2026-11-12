import unittest

from grade_calculator import calculate_final_grade, calculate_record_grade, get_performance_comment


class TestGradeCalculator(unittest.TestCase):
    def test_normal_grade_calculation(self):
        result = calculate_final_grade(80, 70, 60, 90)
        self.assertEqual(result, 70.0)

    def test_all_full_marks(self):
        result = calculate_final_grade(100, 100, 100, 100)
        self.assertEqual(result, 100.0)

    def test_missing_mark_is_counted_as_zero(self):
        result = calculate_final_grade("", 70, 60, 80)
        self.assertEqual(result, 60.0)

    def test_invalid_mark_above_100(self):
        with self.assertRaises(ValueError):
            calculate_final_grade(105, 60, 70, 80)

    def test_invalid_text_mark(self):
        with self.assertRaises(ValueError):
            calculate_final_grade("absent", 60, 70, 80)

    def test_invalid_negative_mark(self):
        with self.assertRaises(ValueError):
            calculate_final_grade(60, -5, 70, 80)

    def test_decimal_marks_are_calculated(self):
        result = calculate_final_grade(75.5, 80.5, 66.5, 90)
        self.assertEqual(result, 74.9)

    def test_performance_comment(self):
        self.assertEqual(get_performance_comment(76), "Distinction")
        self.assertEqual(get_performance_comment(55), "Pass")
        self.assertEqual(get_performance_comment(40), "Fail")

    def test_record_grade_adds_final_grade_and_performance(self):
        record = {
            "quiz": "75",
            "project": "50",
            "final_exam": "88",
            "practical": "65",
        }

        result = calculate_record_grade(record)
        self.assertEqual(result["final_grade"], 74.5)
        self.assertEqual(result["performance"], "Pass")


if __name__ == "__main__":
    unittest.main()
