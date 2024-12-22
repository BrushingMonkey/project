"""Add position_type to trades

Revision ID: 1367891eefb1
Revises: c6443a05d781
Create Date: 2024-11-28 13:01:02.297704

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1367891eefb1"
down_revision = "c6443a05d781"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("trades", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("position_type", sa.String(length=10), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("trades", schema=None) as batch_op:
        batch_op.drop_column("position_type")

    # ### end Alembic commands ###
