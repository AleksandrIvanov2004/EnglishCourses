"""initial

Revision ID: 470992da094d
Revises: 
Create Date: 2024-10-24 09:41:08.589247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision: str = '470992da094d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('email', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('password', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('first_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('second_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade() -> None:
    op.drop_table('users', schema=settings.POSTGRES_SCHEMA)
