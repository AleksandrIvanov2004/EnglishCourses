from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.course import CourseSchema
from project.infrastructure.postgres.models import Course
from project.core.config import settings


class CourseRepository:
    _collection: Type[Course] = Course

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_courses(
        self,
        session: AsyncSession,
    ) -> list[CourseSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.courses;"
        courses = await session.execute(text(query))
        return [CourseSchema.model_validate(obj=course) for course in courses.mappings().all()]


    async def get_course_by_id(
            self,
            session: AsyncSession,
            id_course: int
    ) -> CourseSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.courses where id = :id")

        result = await session.execute(query, {"id": id_course})

        courses_row = result.mappings().first()

        if courses_row:
            return CourseSchema.model_validate(dict(courses_row))
        return None


    async def insert_course(
            self,
            session: AsyncSession,
            language: str,
            level: str
    ) -> CourseSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.courses (language, level) 
               VALUES (:language, :level)
               RETURNING id, language, level
           """)
        result = await session.execute(query, {"language": language, "level": level})

        courses_row = result.mappings().first()

        if courses_row:
            return CourseSchema.model_validate(dict(courses_row))
        return None


    async def delete_course_by_id(
            self,
            session: AsyncSession,
            id_course: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.courses WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_course})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_course_by_id(
            self,
            session: AsyncSession,
            id_course: int,
            language: str,
            level: str
    ) -> CourseSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.courses 
               SET language = :language, level = :level
               WHERE id = :id 
               RETURNING id, language, level
           """)

        result = await session.execute(query, {"id": id_course, "language": language, "level": level})

        updated_row = result.mappings().first()

        if updated_row:
            return CourseSchema.model_validate(dict(updated_row))

        return None