from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from sqlalchemy.testing.pickleable import User

from project.infrastructure.security.JWT_token import create_access_token
from project.infrastructure.security.bcrypt import hash_password, verify_password
from project.schemas.user import UserSchema
from project.infrastructure.postgres.models import User
from project.core.config import settings


class UserRepository:
    _collection: Type[User] = User

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users;"
        users = await session.execute(text(query))
        return [UserSchema.model_validate(dict(user)) for user in users.mappings().all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> UserSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id")
        result = await session.execute(query, {"id": id_user})
        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> UserSchema | None:
        query = text(f"SELECT * FROM {settings.POSTGRES_SCHEMA}.users WHERE email = :email")
        result = await session.execute(query, {"email": email})
        user_row = result.mappings().first()

        if user_row:
            return UserSchema.model_validate(dict(user_row))
        return None

    async def register_user(
            self,
            session: AsyncSession,
            age: int,
            email: str,
            passw: str,
            first_name: str,
            second_name: str,
            role: str
    ) -> UserSchema | None:
        if role not in ["user", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        # Check if the user already exists
        query = text(f"SELECT 1 FROM {settings.POSTGRES_SCHEMA}.users WHERE email = :email LIMIT 1")
        result = await session.execute(query, {"email": email})
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # If user does not exist, insert the new user
        password_hashed = hash_password(passw)

        query = text(f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.users (age, email, password, first_name, second_name, role) 
            VALUES (:age, :email, :password, :first_name, :second_name, :role)
            RETURNING id, age, email, password, first_name, second_name, role
        """)

        try:
            result = await session.execute(query, {"age": age,
                                                          "email": email,
                                                          "password": password_hashed,
                                                          "first_name": first_name,
                                                          "second_name": second_name,
                                                          "role": role})
            user_row = result.mappings().first()

            if user_row:
                return UserSchema.model_validate(dict(user_row))
            return None

        except IntegrityError:
            raise HTTPException(status_code=400, detail="Error while registering the user")

    async def login_user(
        self,
        session: AsyncSession,
        email: str,
        passw: str
    ) -> dict:
        user = await self.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User with such email not found")

        if not verify_password(passw, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token({"user_id": user.id, "role":user.role})

        return {"user": user, "access_token": token, "token_type": "bearer"}

    async def delete_user_by_id(
        self,
        session: AsyncSession,
        id_user: int
    ) -> bool:
        query = text(f"DELETE FROM {settings.POSTGRES_SCHEMA}.users WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_user})
        deleted_row = result.fetchone()

        return True if deleted_row else False

    async def update_user_by_id(
            self,
            session: AsyncSession,
            id_user: int,
            age: int,
            email: str,
            password: str,
            first_name: str,
            second_name: str,
            role: str
    ) -> UserSchema | None:
        query = text(f"""
               UPDATE {settings.POSTGRES_SCHEMA}.users 
               SET age = :age, email = :email, password = :password, first_name = :first_name, second_name = :second_name, role = :role
               WHERE id = :id 
               RETURNING id, age, email, password, first_name, second_name, role
           """)

        result = await session.execute(query, {"id": id_user, "age": age, "email": email, "password": password,
                                               "first_name": first_name, "second_name": second_name, "role": role})

        updated_row = result.mappings().first()

        if updated_row:
            return UserSchema.model_validate(dict(updated_row))

        return None

    async def insert_user(
            self,
            session: AsyncSession,
            age: int,
            email: str,
            password: str,
            first_name: str,
            second_name: str,
            role: str
    ) -> UserSchema | None:
        query = text(f"""
               INSERT INTO {settings.POSTGRES_SCHEMA}.users (age, email, password, first_name, second_name, role) 
               VALUES (:age, :email, :password, :first_name, :second_name, :role)
               RETURNING id, age, email, password, first_name, second_name, role
           """)
        result = await session.execute(query,
                                       {"age": age, "email": email, "password": password, "first_name": first_name,
                                        "second_name": second_name, "role": role})

        users_row = result.mappings().first()

        if users_row:
            return UserSchema.model_validate(dict(users_row))
        return None