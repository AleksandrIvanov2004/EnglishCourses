from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.group import GroupSchema
from project.infrastructure.postgres.models import Group
from project.core.config import settings


class GroupRepository:
    _collection: Type[Group] = Group

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_groups(
        self,
        session: AsyncSession,
    ) -> list[GroupSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.groups;"
        groups = await session.execute(text(query))
        return [GroupSchema.model_validate(obj=group) for group in groups.mappings().all()]


    async def get_group_by_number(
            self,
            session: AsyncSession,
            number_group: int
    ) -> GroupSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.groups where group_number = :group_number")

        result = await session.execute(query, {"group_number": number_group})

        groups_row = result.mappings().first()

        if groups_row:
            return GroupSchema.model_validate(dict(groups_row))
        return None


    async def insert_group(
            self,
            session: AsyncSession,
            number_group: int,
            course_id: int
    ) -> GroupSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.groups (group_number, course_id) 
               VALUES (:group_number, :course_id)
               RETURNING group_number, course_id
           """)
        result = await session.execute(query, {"group_number": number_group, "course_id": course_id})

        groups_row = result.mappings().first()

        if groups_row:
            return GroupSchema.model_validate(dict(groups_row))
        return None


    async def delete_group_by_number(
            self,
            session: AsyncSession,
            number_group: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.groups WHERE group_number = :group_number RETURNING group_number")

        result = await session.execute(query, {"group_number": number_group})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_group_by_number(
            self,
            session: AsyncSession,
            number_group: int,
            course_id: int
    ) -> GroupSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.groups 
               SET course_id = :course_id
               WHERE group_number = :group_number
               RETURNING group_number, course_id
           """)

        result = await session.execute(query, {"group_number": number_group, "course_id": course_id})

        updated_row = result.mappings().first()

        if updated_row:
            return GroupSchema.model_validate(dict(updated_row))

        return None