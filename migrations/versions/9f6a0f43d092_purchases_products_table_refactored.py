"""purchases_products table refactored

Revision ID: 9f6a0f43d092
Revises: e1067b27d75d
Create Date: 2022-03-03 11:34:28.186493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f6a0f43d092'
down_revision = 'e1067b27d75d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases_products', sa.Column('quantity', sa.Integer(), nullable=False))
    op.add_column('purchases_products', sa.Column('value', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchases_products', 'value')
    op.drop_column('purchases_products', 'quantity')
    # ### end Alembic commands ###