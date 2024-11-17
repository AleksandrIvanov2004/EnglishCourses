from datetime import datetime
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.courses_raiting import CoursesRaitingSchema
from project.infrastructure.postgres.models import CoursesRaiting
from project.core.config import settings


class CoursesRaitingRepository:
    _collection: Type[CoursesRaiting] = CoursesRaiting

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_courses_raiting(
        self,
        session: AsyncSession,
    ) -> list[CoursesRaitingSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.courses_raiting;"

        courses_raitings = await session.execute(text(query))

        return [CoursesRaitingSchema.model_validate(dict(course)) for course in courses_raitings.mappings().all()]

    async def get_courses_raiting_by_id(
            self,
            session: AsyncSession,
            course_id: int
    ) -> CoursesRaitingSchema | None:
        query = text(f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.courses_raiting
            WHERE course_id = :course_id
        """)

        result = await session.execute(query, {"course_id": course_id})

        courses_raiting_row = result.mappings().first()

        if courses_raiting_row:
            return CoursesRaitingSchema.model_validate(dict(courses_raiting_row))
        return None

    async def insert_courses_raiting(
            self,
            session: AsyncSession,
            course_id: int,
            raiting: float,
            actually_date: datetime
    ) -> CoursesRaitingSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.courses_raiting (course_id, raiting, actually_date) 
            VALUES (:course_id, :raiting, :actually_date)
            RETURNING course_id, raiting, actually_date
        """)
        result = await session.execute(query, {"course_id": course_id, "raiting": raiting, "actually_date": actually_date})

        courses_raiting_row = result.mappings().first()

        if courses_raiting_row:
            return CoursesRaitingSchema.model_validate(dict(courses_raiting_row))
        return None

    async def delete_courses_raiting_by_id(
            self,
            session: AsyncSession,
            course_id: int
    ) -> bool:
        query = text(f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.courses_raiting 
            WHERE course_id = :course_id
            RETURNING course_id
        """)

        result = await session.execute(query, {"course_id": course_id})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_courses_raiting_by_id(
            self,
            session: AsyncSession,
            course_id: int,
            raiting: float,
            actually_date: datetime
    ) -> CoursesRaitingSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.courses_raiting 
            SET course_id = :course_id
            WHERE course_id = :course_id
            RETURNING course_id, raiting, actually_date
        """)

        result = await session.execute(query, {"course_id": course_id, "raiting": raiting, "actually_date": actually_date})

        updated_row = result.mappings().first()

        if updated_row:
            return CoursesRaitingSchema.model_validate(dict(updated_row))

        return None