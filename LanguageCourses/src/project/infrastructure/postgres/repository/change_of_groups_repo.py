from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.change_of_groups import ChangeOfGroupsSchema
from project.infrastructure.postgres.models import ChangeOfGroups
from project.core.config import settings


class ChangeOfGroupsRepository:
    _collection: Type[ChangeOfGroups] = ChangeOfGroups

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_changes_of_groups(
        self,
        session: AsyncSession,
    ) -> list[ChangeOfGroupsSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.change_of_groups;"
        change_of_groups = await session.execute(text(query))
        return [ChangeOfGroupsSchema.model_validate(obj=change) for change in change_of_groups.mappings().all()]


    async def get_change_of_groups_by_id(
            self,
            session: AsyncSession,
            id_change: int
    ) -> ChangeOfGroupsSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.change_of_groups where id = :id")

        result = await session.execute(query, {"id": id_change})

        changes_row = result.mappings().first()

        if changes_row:
            return ChangeOfGroupsSchema.model_validate(dict(changes_row))
        return None


    async def insert_change_of_groups(
            self,
            session: AsyncSession,
            user_id: int,
            group_number_before: int,
            group_number_after: int,
            date: datetime
    ) -> ChangeOfGroupsSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.change_of_groups (user_id, group_number_before, group_number_after, date) 
               VALUES (:user_id, :group_number_before, :group_number_after, :date)
               RETURNING id, user_id, group_number_before, group_number_after, date
           """)
        result = await session.execute(query, {"user_id": user_id, "group_number_before": group_number_before, "group_number_after": group_number_after, "date": date})

        changes_row = result.mappings().first()

        if changes_row:
            return ChangeOfGroupsSchema.model_validate(dict(changes_row))
        return None


    async def delete_change_of_groups_by_id(
            self,
            session: AsyncSession,
            id_change: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.change_of_groups WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_change})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_change_of_groups_by_id(
            self,
            session: AsyncSession,
            id_change: int,
            user_id: int,
            group_number_before: int,
            group_number_after: int,
            date: datetime
    ) -> ChangeOfGroupsSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.change_of_groups 
               SET user_id = :user_id, group_number_before = :group_number_before, group_number_after = :group_number_after, date = :date 
               WHERE id = :id 
               RETURNING id, user_id, group_number_before, group_number_after, date
           """)

        result = await session.execute(query, {"id": id_change, "user_id": user_id, "group_number_before": group_number_before, "group_number_after": group_number_after, "date": date})

        updated_row = result.mappings().first()

        if updated_row:
            return ChangeOfGroupsSchema.model_validate(dict(updated_row))

        return None