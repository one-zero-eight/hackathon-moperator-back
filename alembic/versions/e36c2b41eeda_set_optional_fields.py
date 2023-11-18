"""set optional fields

Revision ID: e36c2b41eeda
Revises: 52d1b991585d
Create Date: 2023-11-18 06:01:51.376106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e36c2b41eeda"
down_revision: Union[str, None] = "52d1b991585d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("user_data", "employee_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("user_data", "rfid_id", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("user_data", "last_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("user_data", "first_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("user_data", "middle_name", existing_type=sa.VARCHAR(), nullable=True)
    op.create_unique_constraint(None, "user_data", ["employee_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_data", type_="unique")
    op.alter_column("user_data", "middle_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("user_data", "first_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("user_data", "last_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("user_data", "rfid_id", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("user_data", "employee_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###