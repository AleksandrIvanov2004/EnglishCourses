from datetime import datetime
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.teachers_raiting import TeachersRaitingSchema
from project.infrastructure.postgres.models import TeachersRaiting
from project.core.config import settings


class TeachersRaitingRepository:
    _collection: Type[TeachersRaiting] = TeachersRaiting

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_teachers_raiting(
        self,
        session: AsyncSession,
    ) -> list[TeachersRaitingSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.teachers_raiting;"

        teachers_raitings = await session.execute(text(query))

        return [TeachersRaitingSchema.model_validate(dict(teacher)) for teacher in teachers_raitings.mappings().all()]

    async def get_teachers_raiting_by_id(
            self,
            session: AsyncSession,
            teacher_id: int
    ) -> TeachersRaitingSchema | None:
        query = text(f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.teachers_raiting
            WHERE teacher_id = :teacher_id
        """)

        result = await session.execute(query, {"teacher_id": teacher_id})

        teachers_raiting_row = result.mappings().first()

        if teachers_raiting_row:
            return TeachersRaitingSchema.model_validate(dict(teachers_raiting_row))
        return None

    async def insert_teachers_raiting(
            self,
            session: AsyncSession,
            teacher_id: int,
            raiting: float,
            actually_date: datetime
    ) -> TeachersRaitingSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.teachers_raiting (teacher_id, raiting, actually_date) 
            VALUES (:teacher_id, :raiting, :actually_date)
            RETURNING teacher_id, raiting, actually_date
        """)
        result = await session.execute(query, {"teacher_id": teacher_id, "raiting": raiting, "actually_date": actually_date})

        teachers_raiting_row = result.mappings().first()

        if teachers_raiting_row:
            return TeachersRaitingSchema.model_validate(dict(teachers_raiting_row))
        return None

    async def delete_teachers_raiting_by_id(
            self,
            session: AsyncSession,
            teacher_id: int
    ) -> bool:
        query = text(f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.teachers_raiting 
            WHERE teacher_id = :teacher_id
            RETURNING teacher_id
        """)

        result = await session.execute(query, {"teacher_id": teacher_id})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_teachers_raiting_by_id(
            self,
            session: AsyncSession,
            teacher_id: int,
            raiting: float,
            actually_date: datetime
    ) -> TeachersRaitingSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.teachers_raiting 
            SET teacher_id = :teacher_id
            WHERE teacher_id = :teacher_id
            RETURNING teacher_id, raiting, actually_date
        """)

        result = await session.execute(query, {"teacher_id": teacher_id, "raiting": raiting, "actually_date": actually_date})

        updated_row = result.mappings().first()

        if updated_row:
            return TeachersRaitingSchema.model_validate(dict(updated_row))

        return None