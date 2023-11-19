"""attachments_to_machines_and_photos_to_user

Revision ID: 32e7adee66d0
Revises: 41766405a244
Create Date: 2023-11-19 03:43:44.456833

"""
from typing import Sequence, Union

import fastapi_storages
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e7adee66d0'
down_revision: Union[str, None] = '41766405a244'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from src.storages.sqlalchemy.models.machines import machines_attachments_storage
    from src.storages.sqlalchemy.models.users import photo_storage
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('machines', sa.Column('attachments', fastapi_storages.integrations.sqlalchemy.FileType(storage=machines_attachments_storage), nullable=True))
    op.drop_column('tasks', 'description')
    op.add_column('user_data', sa.Column('photo', fastapi_storages.integrations.sqlalchemy.ImageType(storage=photo_storage), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_data', 'photo')
    op.add_column('tasks', sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('machines', 'attachments')
    # ### end Alembic commands ###
