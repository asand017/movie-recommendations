"""Initial migration

Revision ID: a381714e8f8a
Revises: 43bb08fdc887
Create Date: 2024-06-09 22:32:27.496054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a381714e8f8a'
down_revision = '43bb08fdc887'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('review', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('imdb_rating', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('imdb_votes', sa.Integer(), nullable=False))

    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('count', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.drop_column('count')

    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.drop_column('imdb_votes')
        batch_op.drop_column('imdb_rating')
        batch_op.drop_column('review')

    # ### end Alembic commands ###
