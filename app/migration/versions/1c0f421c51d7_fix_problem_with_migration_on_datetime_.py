"""fix problem with migration on DateTime field

Revision ID: 1c0f421c51d7
Revises: 43269a7c851f
Create Date: 2022-07-24 04:11:52.555403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c0f421c51d7'
down_revision = '6eb3fc0e49c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ShopUnit', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
