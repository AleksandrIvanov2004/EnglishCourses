from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from project.infrastructure.postgres.database import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[str] = mapped_column(nullable=False)

class Group(Base):
    __tablename__ = "groups"

    group_number: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class ChangeOfGroups(Base):
    __tablename__ = "change_of_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    group_number_before: Mapped[int] = mapped_column(ForeignKey("groups.group_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    group_number_after: Mapped[int] = mapped_column(ForeignKey("groups.group_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

class CoursesRaiting(Base):
    __tablename__ = "courses_raiting"

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    raiting: Mapped[float] = mapped_column(nullable=False)
    actually_date: Mapped[datetime] = mapped_column(nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    pay_date: Mapped[datetime] = mapped_column(nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    experience: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)

class TeachersRaiting(Base):
    __tablename__ = "teachers_raiting"

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    raiting: Mapped[float] = mapped_column(nullable=False)
    actually_date: Mapped[datetime] = mapped_column(nullable=False)

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    group_number: Mapped[int] = mapped_column(ForeignKey("groups.group_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    start_lesson: Mapped[datetime] = mapped_column(nullable=False)
    end_lesson: Mapped[datetime] = mapped_column(nullable=False)

class Stream(Base):
    __tablename__ = "streams"

    stream_number: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

class UsersAndGroups(Base):
    __tablename__ = "users_and_groups"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    group_number: Mapped[float] = mapped_column(ForeignKey("groups.group_number", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    stream_number: Mapped[datetime] = mapped_column(ForeignKey("streams.stream_number", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

class UsersHasSchedule(Base):
    __tablename__ = "users_has_schedule"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    schedule_id: Mapped[float] = mapped_column(ForeignKey("schedule.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    attendance: Mapped[bool] = mapped_column(nullable=False)
    mark: Mapped[int] = mapped_column(nullable=True)