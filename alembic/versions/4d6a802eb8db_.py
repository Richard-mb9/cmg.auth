"""empty message

Revision ID: 4d6a802eb8db
Revises: f26598d0bd07
Create Date: 2022-08-24 19:18:09.306741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d6a802eb8db'
down_revision = 'f26598d0bd07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'profiles', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.drop_column('profiles', 'role_id')
    # ### end Alembic commands ###
