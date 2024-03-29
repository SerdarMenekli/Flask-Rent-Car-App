"""empty message

Revision ID: 32c26ca62fe9
Revises: e050cdc2672e
Create Date: 2023-12-30 13:27:08.337631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32c26ca62fe9'
down_revision = 'e050cdc2672e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_column('current_location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_location', sa.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###
