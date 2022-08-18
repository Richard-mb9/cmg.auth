"""empty message

Revision ID: 9be886fe78c3
Revises: 4485b6a617ab
Create Date: 2022-08-17 13:05:44.791323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9be886fe78c3'
down_revision = '4485b6a617ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('enable', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'enable')
    # ### end Alembic commands ###
