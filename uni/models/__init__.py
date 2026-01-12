from .users_table import User
from .departments_table import Department
from .batches_table import Batch
from .subjects_table import Subject

# Dependent tables
from .teachers_table import Teacher
from .students_table import Student
from .results_table import Result

# Association tables
from .assosiations import (
    batch_subjects,
    department_subjects,
    teaching_assignments,
)

__all__ = [
    "User",
    "Department",
    "Batch",
    "Subject",
    "Teacher",
    "Student",
    "Result",
    "batch_subjects",
    "department_subjects",
    "teaching_assignments",
]
