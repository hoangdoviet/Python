"""update db

Revision ID: fa3bc0eee260
Revises: 70623960df15
Create Date: 2022-05-25 02:54:27.823839

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fa3bc0eee260'
down_revision = '70623960df15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('db_cart', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('db_cart', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
