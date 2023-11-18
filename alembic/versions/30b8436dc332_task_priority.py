"""task priority

Revision ID: 30b8436dc332
Revises: fc51c09aaadc
Create Date: 2023-11-18 17:58:47.244954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "30b8436dc332"
down_revision: Union[str, None] = "fc51c09aaadc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    priority_type = sa.Enum("undefined", "low", "medium", "high", name="taskpriority")
    priority_type.create(op.get_bind())

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.VARCHAR(),
        type_=priority_type,
        postgresql_using="priority::taskpriority",
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    priority_type = sa.Enum("undefined", "low", "medium", "high", name="taskpriority")

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks",
        "priority",
        existing_type=priority_type,
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###

    priority_type.drop(op.get_bind())
