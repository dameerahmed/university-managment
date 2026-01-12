from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, func
from uni.database.connection import Base

department_subjects = Table(
    "department_subjects",
    Base.metadata,
    Column(
        "department_id",
        Integer,
        ForeignKey("departments.department_id", ondelete="CASCADE"),
    ),
    Column(
        "subject_id", Integer, ForeignKey("subjects.subject_id", ondelete="CASCADE")
    ),
)


batch_subjects = Table(
    "batch_subjects",
    Base.metadata,
    Column("batch_id", Integer, ForeignKey("batches.batch_id", ondelete="CASCADE")),
    Column(
        "subject_id", Integer, ForeignKey("subjects.subject_id", ondelete="CASCADE")
    ),
)

teaching_assignments = Table(
    "teaching_assignments",
    Base.metadata,
    Column("assignment_id", Integer, primary_key=True, autoincrement=True),
    Column(
        "teacher_id", Integer, ForeignKey("teachers.teacher_id", ondelete="CASCADE")
    ),
    Column(
        "department_id",
        Integer,
        ForeignKey("departments.department_id", ondelete="CASCADE"),
    ),
    Column("batch_id", Integer, ForeignKey("batches.batch_id", ondelete="CASCADE")),
    Column("semester", Integer),
    Column(
        "subject_id", Integer, ForeignKey("subjects.subject_id", ondelete="CASCADE")
    ),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)
