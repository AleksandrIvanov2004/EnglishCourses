from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.users_has_schedule import UsersHasScheduleSchema
from project.infrastructure.postgres.models import UsersHasSchedule
from project.core.config import settings


class UsersHasScheduleRepository:
    _collection: Type[UsersHasSchedule] = UsersHasSchedule

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users_has_schedule(
        self,
        session: AsyncSession,
    ) -> list[UsersHasScheduleSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users_has_schedule;"

        users_has_schedule = await session.execute(text(query))

        return [UsersHasScheduleSchema.model_validate(dict(us_has_sch)) for us_has_sch in
                users_has_schedule.mappings().all()]

    async def get_user_has_schedule_by_id(
            self,
            session: AsyncSession,
            user_id: int
    ) -> UsersHasScheduleSchema | None:
        query = text(f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.users_has_schedule
            WHERE user_id = :user_id 
        """)

        result = await session.execute(query, {"user_id": user_id})

        users_has_schedule_row = result.mappings().first()

        if users_has_schedule_row:
            return UsersHasScheduleSchema.model_validate(dict(users_has_schedule_row))
        return None

    async def insert_user_has_schedule(
            self,
            session: AsyncSession,
            user_id: int,
            schedule_id: int,
            attendance: bool,
            mark: int
    ) -> UsersHasScheduleSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users_has_schedule (user_id, schedule_id, attendance, mark) 
            VALUES (:user_id, :schedule_id, :attendance, :mark)
            RETURNING user_id, schedule_id, attendance, mark
        """)
        result = await session.execute(query, {"user_id": user_id, "schedule_id": schedule_id
                                                      , "attendance": attendance, "mark": mark})

        users_has_schedule_row = result.mappings().first()

        if users_has_schedule_row:
            return UsersHasScheduleSchema.model_validate(dict(users_has_schedule_row))
        return None

    async def delete_user_has_schedule_by_id(
            self,
            session: AsyncSession,
            user_id: int
    ) -> bool:
        query = text(f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.users_has_schedule
            WHERE user_id = :user_id 
            RETURNING user_id
        """)

        result = await session.execute(query, {"user_id": user_id})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_user_has_schedule_by_id(
            self,
            session: AsyncSession,
            user_id: int,
            schedule_id: int,
            attendance: bool,
            mark: int
    ) -> UsersHasScheduleSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.users_has_schedule
            SET user_id = :user_id
            WHERE user_id = :user_id 
            RETURNING user_id, schedule_id, attendance, mark
        """)

        result = await session.execute(query, {"user_id": user_id, "schedule_id": schedule_id
                                                      , "attendance": attendance, "mark": mark})

        updated_row = result.mappings().first()

        if updated_row:
            return UsersHasScheduleSchema.model_validate(dict(updated_row))

        return None