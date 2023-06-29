"""first msg

Revision ID: 17a2ea7a0d38
Revises: 0d9a34fd97c3
Create Date: 2023-06-27 16:18:21.277658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17a2ea7a0d38'
down_revision = '0d9a34fd97c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_title', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('event_title')

    # ### end Alembic commands ###
