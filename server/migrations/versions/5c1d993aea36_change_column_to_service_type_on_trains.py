"""change column to service_type on trains

Revision ID: 5c1d993aea36
Revises: c5f49adb3833
Create Date: 2023-08-17 14:33:32.121735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c1d993aea36'
down_revision = 'c5f49adb3833'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_type', sa.String(), nullable=True))
        batch_op.drop_column('is_express')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trains', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_express', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('service_type')

    # ### end Alembic commands ###