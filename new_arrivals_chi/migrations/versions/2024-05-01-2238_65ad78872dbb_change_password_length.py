"""change password length

Revision ID: 65ad78872dbb
Revises: 923816bbaeb7
Create Date: 2024-05-01 22:38:44.167349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "65ad78872dbb"
down_revision = "923816bbaeb7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "password",
            existing_type=sa.VARCHAR(length=100),
            type_=sa.String(length=255),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "password",
            existing_type=sa.String(length=255),
            type_=sa.VARCHAR(length=100),
            existing_nullable=False,
        )

    # ### end Alembic commands ###