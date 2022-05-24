"""update db

Revision ID: edd4aad64255
Revises: 6eb7e1173070
Create Date: 2022-05-25 00:02:25.372088

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'edd4aad64255'
down_revision = '6eb7e1173070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_cart', sa.Column('sum_price', sa.INTEGER(), nullable=True))
    op.alter_column('db_cart', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.create_index(op.f('ix_db_cart_sum_price'), 'db_cart', ['sum_price'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_cart_sum_price'), table_name='db_cart')
    op.alter_column('db_cart', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('db_cart', 'sum_price')
    # ### end Alembic commands ###
