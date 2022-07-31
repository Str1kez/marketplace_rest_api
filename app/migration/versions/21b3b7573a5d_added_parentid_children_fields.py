"""added parentId, children fields

Revision ID: 21b3b7573a5d
Revises: 6d19a7806578
Create Date: 2022-07-24 01:24:58.444995

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '21b3b7573a5d'
down_revision = '6d19a7806578'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ShopUnit', sa.Column('parentId', postgresql.UUID(), nullable=True))
    op.create_foreign_key(None, 'ShopUnit', 'ShopUnit', ['parentId'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ShopUnit', type_='foreignkey')
    op.drop_column('ShopUnit', 'parentId')
    # ### end Alembic commands ###