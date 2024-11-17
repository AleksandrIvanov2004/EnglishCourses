from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.stream import StreamSchema
from project.infrastructure.postgres.models import Stream
from project.core.config import settings


class StreamRepository:
    _collection: Type[Stream] = Stream

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_streams(
        self,
        session: AsyncSession,
    ) -> list[StreamSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.streams;"
        streams = await session.execute(text(query))
        return [StreamSchema.model_validate(obj=stream) for stream in streams.mappings().all()]


    async def get_stream_by_number(
            self,
            session: AsyncSession,
            number_stream: int
    ) -> StreamSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.streams where stream_number = :stream_number")

        result = await session.execute(query, {"stream_number": number_stream})

        streams_row = result.mappings().first()

        if streams_row:
            return StreamSchema.model_validate(dict(streams_row))
        return None


    async def insert_stream(
            self,
            session: AsyncSession,
            course_id: int
    ) -> StreamSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.streams (course_id) 
               VALUES (:course_id)
               RETURNING stream_number, course_id
           """)
        result = await session.execute(query, {"course_id": course_id})

        streams_row = result.mappings().first()

        if streams_row:
            return StreamSchema.model_validate(dict(streams_row))
        return None


    async def delete_stream_by_number(
            self,
            session: AsyncSession,
            number_stream: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.streams WHERE stream_number = :stream_number RETURNING stream_number")

        result = await session.execute(query, {"stream_number": number_stream})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_stream_by_number(
            self,
            session: AsyncSession,
            number_stream: int,
            course_id: int
    ) -> StreamSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.streams 
               SET course_id = :course_id
               WHERE stream_number = :stream_number
               RETURNING stream_number, course_id
           """)

        result = await session.execute(query, {"stream_number": number_stream, "course_id": course_id})

        updated_row = result.mappings().first()

        if updated_row:
            return StreamSchema.model_validate(dict(updated_row))

        return None