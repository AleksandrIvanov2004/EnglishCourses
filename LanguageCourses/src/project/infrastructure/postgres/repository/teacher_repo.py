from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.teacher import TeacherSchema
from project.infrastructure.postgres.models import Teacher
from project.core.config import settings


class TeacherRepository:
    _collection: Type[Teacher] = Teacher

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_teachers(
        self,
        session: AsyncSession,
    ) -> list[TeacherSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.teachers;"
        teachers = await session.execute(text(query))
        return [TeacherSchema.model_validate(obj=teacher) for teacher in teachers.mappings().all()]


    async def get_teacher_by_id(
            self,
            session: AsyncSession,
            id_teacher: int
    ) -> TeacherSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.teachers where id = :id")

        result = await session.execute(query, {"id": id_teacher})

        teachers_row = result.mappings().first()

        if teachers_row:
            return TeacherSchema.model_validate(dict(teachers_row))
        return None


    async def insert_teacher(
            self,
            session: AsyncSession,
            age: int,
            experience: int,
            first_name: str,
            second_name: str
    ) -> TeacherSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.teachers (age, experience, first_name, second_name) 
               VALUES (:age, :experience, :first_name, :second_name)
               RETURNING id, age, experience, first_name, second_name
           """)
        result = await session.execute(query, {"age" : age, "experience": experience, "first_name" : first_name, "second_name" : second_name})

        teachers_row = result.mappings().first()

        if teachers_row:
            return TeacherSchema.model_validate(dict(teachers_row))
        return None


    async def delete_teacher_by_id(
            self,
            session: AsyncSession,
            id_teacher: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.teachers WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_teacher})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_teacher_by_id(
            self,
            session: AsyncSession,
            id_teacher: int,
            age: int,
            experience: int,
            first_name: str,
            second_name: str
    ) -> TeacherSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.teachers 
               SET age = :age, experience = :experience, first_name = :first_name, second_name = :second_name 
               WHERE id = :id 
               RETURNING id, age, experience, first_name, second_name
           """)

        result = await session.execute(query, {"id": id_teacher, "age": age, "experience": experience, "first_name": first_name, "second_name": second_name})

        updated_row = result.mappings().first()

        if updated_row:
            return TeacherSchema.model_validate(dict(updated_row))

        return None