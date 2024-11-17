from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.lesson import LessonSchema
from project.infrastructure.postgres.models import Lesson
from project.core.config import settings


class LessonRepository:
    _collection: Type[Lesson] = Lesson

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_lessons(
        self,
        session: AsyncSession,
    ) -> list[LessonSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.lessons;"
        lessons = await session.execute(text(query))
        return [LessonSchema.model_validate(obj=lesson) for lesson in lessons.mappings().all()]


    async def get_lesson_by_id(
            self,
            session: AsyncSession,
            id_lesson: int
    ) -> LessonSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.lessons where id = :id")

        result = await session.execute(query, {"id": id_lesson})

        lessons_row = result.mappings().first()

        if lessons_row:
            return LessonSchema.model_validate(dict(lessons_row))
        return None


    async def insert_lesson(
            self,
            session: AsyncSession,
            name: str,
            course_id: int
    ) -> LessonSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.lessons (name, course_id) 
               VALUES (:name, :course_id)
               RETURNING id, name, course_id
           """)
        result = await session.execute(query, {"name": name, "course_id": course_id})

        lessons_row = result.mappings().first()

        if lessons_row:
            return LessonSchema.model_validate(dict(lessons_row))
        return None


    async def delete_lesson_by_id(
            self,
            session: AsyncSession,
            id_lesson: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.lessons WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_lesson})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_lesson_by_id(
            self,
            session: AsyncSession,
            id_lesson: int,
            name: str,
            course_id: int
    ) -> LessonSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.lessons 
               SET name = :name, course_id = course_id
               WHERE id = :id 
               RETURNING id, name, course_id
           """)

        result = await session.execute(query, {"id": id_lesson, "name": name, "course_id": course_id})

        updated_row = result.mappings().first()

        if updated_row:
            return LessonSchema.model_validate(dict(updated_row))

        return None