from datetime import datetime
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.payment import PaymentSchema
from project.infrastructure.postgres.models import Payment
from project.core.config import settings


class PaymentRepository:
    _collection: Type[Payment] = Payment

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_payments(
        self,
        session: AsyncSession,
    ) -> list[PaymentSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.payments;"
        payments = await session.execute(text(query))
        return [PaymentSchema.model_validate(obj=payment) for payment in payments.mappings().all()]


    async def get_payment_by_id(
            self,
            session: AsyncSession,
            id_payment: int
    ) -> PaymentSchema | None:
        query = text(f"select * from {settings.POSTGRES_SCHEMA}.payments where id = :id")

        result = await session.execute(query, {"id": id_payment})

        payments_row = result.mappings().first()

        if payments_row:
            return PaymentSchema.model_validate(dict(payments_row))
        return None


    async def insert_payment(
            self,
            session: AsyncSession,
            user_id: int,
            course_id: int,
            pay_date: datetime
    ) -> PaymentSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.payments (user_id, course_id, pay_date) 
               VALUES (:user_id, :course_id, :pay_date)
               RETURNING id, user_id, course_id, pay_date
           """)
        result = await session.execute(query, {"user_id" : user_id, "course_id" : course_id, "pay_date" : pay_date})

        payments_row = result.mappings().first()

        if payments_row:
            return PaymentSchema.model_validate(dict(payments_row))
        return None


    async def delete_payment_by_id(
            self,
            session: AsyncSession,
            id_payment: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.payments WHERE id = :id RETURNING id")

        result = await session.execute(query, {"id": id_payment})

        deleted_row = result.fetchone()

        return True if deleted_row else False



    async def update_payment_by_id(
            self,
            session: AsyncSession,
            id_payment: int,
            user_id: int,
            course_id: int,
            pay_date: datetime
    ) -> PaymentSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.payments 
               SET user_id = :user_id, course_id = :course_id, pay_date = :pay_date
               WHERE id = :id 
               RETURNING id, user_id, course_id, pay_date
           """)

        result = await session.execute(query, {"id": id_payment, "user_id": user_id, "course_id": course_id, "pay_date": pay_date})

        updated_row = result.mappings().first()

        if updated_row:
            return PaymentSchema.model_validate(dict(updated_row))

        return None