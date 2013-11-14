"""Users table

Revision ID: 1672f08dd120
Revises: 17b3cdd5f40d
Create Date: 2013-06-29 22:05:29.142801

"""

# revision identifiers, used by Alembic.
revision = '1672f08dd120'
down_revision = '17b3cdd5f40d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('passphrase_hash', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###