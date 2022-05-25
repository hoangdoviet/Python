"""update db

Revision ID: a1a111b5a028
Revises: 3ab0a0f328a7
Create Date: 2022-05-24 22:25:36.822386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1a111b5a028'
down_revision = '3ab0a0f328a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('db_cart', 'product_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('db_cart', 'product_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###