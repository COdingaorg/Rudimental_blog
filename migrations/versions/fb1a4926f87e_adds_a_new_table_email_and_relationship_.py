"""adds a new table email, and relationship to user, make correct datatypes

Revision ID: fb1a4926f87e
Revises: c1e17cf55ab1
Create Date: 2021-06-23 07:19:16.057562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb1a4926f87e'
down_revision = 'c1e17cf55ab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emails',
    sa.Column('email_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('email_id')
    )
    op.add_column('users', sa.Column('email_list', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'emails', ['email_list'], ['email_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'email_list')
    op.drop_table('emails')
    # ### end Alembic commands ###
