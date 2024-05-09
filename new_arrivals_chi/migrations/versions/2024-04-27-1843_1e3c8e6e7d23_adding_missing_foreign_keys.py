"""Adding missing foreign keys.

Revision ID: 1e3c8e6e7d23
Revises: 56a8e2512e2b
Create Date: 2024-04-27 18:43:14.482909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1e3c8e6e7d23"
down_revision = "56a8e2512e2b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("locations", schema=None) as batch_op:
        batch_op.add_column(sa.Column("org_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, "organizations", ["org_id"], ["id"])

    with op.batch_alter_table("service_dates", schema=None) as batch_op:
        batch_op.add_column(sa.Column("org_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, "organizations", ["org_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("service_dates", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("org_id")

    with op.batch_alter_table("locations", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("org_id")

    # ### end Alembic commands ###
