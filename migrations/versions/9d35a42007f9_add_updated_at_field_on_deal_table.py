"""add updated_at field on Deal table

Revision ID: 9d35a42007f9
Revises: cefd0d2ef0c7
Create Date: 2024-04-26 12:05:46.431318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d35a42007f9'
down_revision: Union[str, None] = 'cefd0d2ef0c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deals', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_deals_updated_at'), 'deals', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_deals_updated_at'), table_name='deals')
    op.drop_column('deals', 'updated_at')
    # ### end Alembic commands ###