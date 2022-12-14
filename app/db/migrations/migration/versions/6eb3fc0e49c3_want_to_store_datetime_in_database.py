"""want to store datetime in database

Revision ID: 6eb3fc0e49c3
Revises: 75d9937ebdf7
Create Date: 2022-07-24 04:03:18.148377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eb3fc0e49c3'
down_revision = 'd9eeec695206'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ShopUnit_parentId_fkey', 'ShopUnit', type_='foreignkey')
    op.create_foreign_key(None, 'ShopUnit', 'ShopUnit', ['parentId'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ShopUnit', type_='foreignkey')
    op.create_foreign_key('ShopUnit_parentId_fkey', 'ShopUnit', 'ShopUnit', ['parentId'], ['id'])
    # ### end Alembic commands ###
