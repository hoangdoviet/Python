"""update db

Revision ID: f0d180c77fad
Revises: edd4aad64255
Create Date: 2022-05-25 00:05:36.993715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0d180c77fad'
down_revision = 'edd4aad64255'
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
