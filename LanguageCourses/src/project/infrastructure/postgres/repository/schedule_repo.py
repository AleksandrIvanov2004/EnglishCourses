from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.schedule import ScheduleSchema
from project.infrastructure.postgres.models import Schedule
from project.core.config import settings


class ScheduleRepository:
    _collection: Type[Schedule] = Schedule

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_schedules(
        self,
        session: AsyncSession,
    ) -> list[ScheduleSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.schedule;"
        schedules = await session.execute(text(query))
        return [ScheduleSchema.model_validate(obj=schedule) for schedule in schedules.mappings().all()]


    async def get_schedule_by_id(
            self,
            session: AsyncSession,
            id_schedule: int
    ) -> ScheduleSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.schedule where id = :id")

        result = await session.execute(query, {"id": id_schedule})

        schedules_row = result.mappings().first()

        if schedules_row:
            return ScheduleSchema.model_validate(dict(schedules_row))
        return None


    async def insert_schedule(
            self,
            session: AsyncSession,
            teacher_id: int,
            group_number: int,
            lesson_id: int,
            start_lesson: datetime,
            end_lesson: datetime
    ) -> ScheduleSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.schedule (teacher_id, group_number, lesson_id, start_lesson, end_lesson) 
               VALUES (:teacher_id, :group_number, :lesson_id, :start_lesson, :end_lesson)
               RETURNING id, teacher_id, group_number, lesson_id, start_lesson, end_lesson
           """)
        result = await session.execute(query, {"teacher_id": teacher_id, "group_number": group_number, "lesson_id": lesson_id, "start_lesson": start_lesson, "end_lesson": end_lesson})

        schedules_row = result.mappings().first()

        if schedules_row:
            return ScheduleSchema.model_validate(dict(schedules_row))
        return None


    async def delete_schedule_by_id(
            self,
            session: AsyncSession,
            id_schedule: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.schedule WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_schedule})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_schedule_by_id(
            self,
            session: AsyncSession,
            id_schedule: int,
            teacher_id: int,
            group_number: int,
            lesson_id: int,
            start_lesson: datetime,
            end_lesson: datetime
    ) -> ScheduleSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.schedule 
               SET teacher_id = :teacher_id, group_number = :group_number, lesson_id = :lesson_id, start_lesson = :start_lesson, end_lesson = :end_lesson
               WHERE id = :id 
               RETURNING id, teacher_id, group_number, lesson_id, start_lesson, end_lesson
           """)

        result = await session.execute(query, {"id": id_schedule, "teacher_id": teacher_id, "group_number": group_number, "lesson_id": lesson_id, "start_lesson": start_lesson, "end_lesson": end_lesson})

        updated_row = result.mappings().first()

        if updated_row:
            return ScheduleSchema.model_validate(dict(updated_row))

        return None