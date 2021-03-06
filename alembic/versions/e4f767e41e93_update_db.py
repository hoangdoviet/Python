"""update db

Revision ID: e4f767e41e93
Revises: d884e3a702af
Create Date: 2022-05-23 17:40:03.930474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f767e41e93'
down_revision = 'd884e3a702af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_cart', sa.Column('quantity', sa.INTEGER(), nullable=True))
    op.create_index(op.f('ix_db_cart_quantity'), 'db_cart', ['quantity'], unique=False)
    op.add_column('db_order_detail', sa.Column('quantity', sa.INTEGER(), nullable=True))
    op.create_index(op.f('ix_db_order_detail_quantity'), 'db_order_detail', ['quantity'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_order_detail_quantity'), table_name='db_order_detail')
    op.drop_column('db_order_detail', 'quantity')
    op.drop_index(op.f('ix_db_cart_quantity'), table_name='db_cart')
    op.drop_column('db_cart', 'quantity')
    # ### end Alembic commands ###
