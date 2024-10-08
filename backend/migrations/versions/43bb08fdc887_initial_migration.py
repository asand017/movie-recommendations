"""Initial migration

Revision ID: 43bb08fdc887
Revises: 
Create Date: 2024-06-09 13:04:10.509017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43bb08fdc887'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('directors', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('runtime', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.drop_column('runtime')
        batch_op.drop_column('directors')

    # ### end Alembic commands ###
