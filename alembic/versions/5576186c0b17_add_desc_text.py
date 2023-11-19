"""add desc TEXT

Revision ID: 5576186c0b17
Revises: 0020f1db8756
Create Date: 2023-11-19 10:48:48.034874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5576186c0b17"
down_revision: Union[str, None] = "0020f1db8756"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("agregates", "description", existing_type=sa.VARCHAR(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("machines", "description", existing_type=sa.VARCHAR(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("task_types", "description", existing_type=sa.VARCHAR(), type_=sa.TEXT(), existing_nullable=True)
    op.alter_column("tasks", "description", existing_type=sa.VARCHAR(), type_=sa.TEXT(), existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tasks", "description", existing_type=sa.TEXT(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column("task_types", "description", existing_type=sa.TEXT(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column("machines", "description", existing_type=sa.TEXT(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column("agregates", "description", existing_type=sa.TEXT(), type_=sa.VARCHAR(), existing_nullable=True)
    # ### end Alembic commands ###
