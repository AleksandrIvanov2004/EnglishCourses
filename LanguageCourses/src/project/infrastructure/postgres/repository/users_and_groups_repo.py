from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.users_and_groups import UsersAndGroupsSchema
from project.infrastructure.postgres.models import UsersAndGroups
from project.core.config import settings


class UsersAndGroupsRepository:
    _collection: Type[UsersAndGroups] = UsersAndGroups

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users_and_groups(
        self,
        session: AsyncSession,
    ) -> list[UsersAndGroupsSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users_and_groups;"

        users_and_groups = await session.execute(text(query))

        return [UsersAndGroupsSchema.model_validate(dict(us_and_gr)) for us_and_gr in users_and_groups.mappings().all()]

    async def get_users_and_groups_by_id(
            self,
            session: AsyncSession,
            user_id: int
    ) -> UsersAndGroupsSchema | None:
        query = text(f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.users_and_groups 
            WHERE user_id = :user_id 
        """)

        result = await session.execute(query, {"user_id": user_id})

        users_and_groups_row = result.mappings().first()

        if users_and_groups_row:
            return UsersAndGroupsSchema.model_validate(dict(users_and_groups_row))
        return None

    async def insert_users_and_groups(
            self,
            session: AsyncSession,
            user_id: int,
            group_number: int,
            stream_number: int
    ) -> UsersAndGroupsSchema | None:
        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users_and_groups (user_id, group_number, stream_number) 
            VALUES (:user_id, :group_number, :stream_number)
            RETURNING user_id, group_number, stream_number
        """)
        result = await session.execute(query, {"user_id": user_id, "group_number": group_number, "stream_number": stream_number})

        users_and_groups_row = result.mappings().first()

        if users_and_groups_row:
            return UsersAndGroupsSchema.model_validate(dict(users_and_groups_row))
        return None

    async def delete_users_and_groups_by_id(
            self,
            session: AsyncSession,
            user_id: int
    ) -> bool:
        query = text(f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.users_and_groups 
            WHERE user_id = :user_id 
            RETURNING user_id
        """)

        result = await session.execute(query, {"user_id": user_id})

        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_users_and_groups_by_id(
            self,
            session: AsyncSession,
            user_id: int,
            group_number: int,
            stream_number: int
    ) -> UsersAndGroupsSchema | None:
        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.users_and_groups 
            SET user_id = :user_id
            WHERE user_id = :user_id 
            RETURNING user_id, group_number, stream_number
        """)

        result = await session.execute(query, {"user_id": user_id, "group_number": group_number
                                                       , "stream_number": stream_number})

        updated_row = result.mappings().first()

        if updated_row:
            return UsersAndGroupsSchema.model_validate(dict(updated_row))

        return None