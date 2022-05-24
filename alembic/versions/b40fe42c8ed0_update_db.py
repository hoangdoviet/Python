"""update db

Revision ID: b40fe42c8ed0
Revises: f0d180c77fad
Create Date: 2022-05-25 00:08:05.856470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b40fe42c8ed0'
down_revision = 'f0d180c77fad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_cart', sa.Column('sum_price', sa.INTEGER(), nullable=True))
    op.create_index(op.f('ix_db_cart_sum_price'), 'db_cart', ['sum_price'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_cart_sum_price'), table_name='db_cart')
    op.drop_column('db_cart', 'sum_price')
    # ### end Alembic commands ###
