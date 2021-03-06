"""update db

Revision ID: 6eb7e1173070
Revises: a1a111b5a028
Create Date: 2022-05-24 22:28:46.868955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6eb7e1173070'
down_revision = 'a1a111b5a028'
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
