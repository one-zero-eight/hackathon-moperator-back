"""attachments_to_tasks

Revision ID: 41766405a244
Revises: 1aac94fa8e0a
Create Date: 2023-11-19 00:49:39.481351

"""
from typing import Sequence, Union

import fastapi_storages
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41766405a244'
down_revision: Union[str, None] = '1aac94fa8e0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from src.storages.sqlalchemy.models.tasks import attachments_storage

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_role',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('tasks', sa.Column('attachments', fastapi_storages.integrations.sqlalchemy.FileType(storage=attachments_storage), nullable=True))
    op.drop_column('tasks', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('tasks', 'attachments')
    op.drop_table('user_role')
    # ### end Alembic commands ###