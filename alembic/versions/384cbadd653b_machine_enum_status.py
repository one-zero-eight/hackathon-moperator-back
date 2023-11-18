"""machine enum status

Revision ID: 384cbadd653b
Revises: f354f9de3862
Create Date: 2023-11-18 17:30:17.760683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "384cbadd653b"
down_revision: Union[str, None] = "f354f9de3862"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    machine_status_type = sa.Enum("free", "busy", "broken", name="machinestatus")
    machine_status_type.create(op.get_bind())

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "machines",
        "status",
        existing_type=sa.VARCHAR(),
        type_=machine_status_type,
        existing_nullable=False,
        postgresql_using="status::machinestatus",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    machine_status_type = sa.Enum("free", "busy", "broken", name="machinestatus")

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "machines",
        "status",
        existing_type=machine_status_type,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="status::text",
    )
    # ### end Alembic commands ###

    machine_status_type.drop(op.get_bind())
