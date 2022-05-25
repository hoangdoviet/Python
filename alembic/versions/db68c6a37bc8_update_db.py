"""update db

Revision ID: db68c6a37bc8
Revises: 7dc120738750
Create Date: 2022-05-25 17:10:20.967547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db68c6a37bc8'
down_revision = '7dc120738750'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_order_detail', sa.Column('sum_price', sa.INTEGER(), nullable=True))
    op.create_index(op.f('ix_db_order_detail_sum_price'), 'db_order_detail', ['sum_price'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_order_detail_sum_price'), table_name='db_order_detail')
    op.drop_column('db_order_detail', 'sum_price')
    # ### end Alembic commands ###