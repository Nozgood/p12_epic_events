"""test

Revision ID: cefd0d2ef0c7
Revises: 79f90c2e065c
Create Date: 2024-04-20 13:27:40.406019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cefd0d2ef0c7'
down_revision: Union[str, None] = '79f90c2e065c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_customers_first_name', table_name='customers')
    op.create_index(op.f('ix_customers_first_name'), 'customers', ['first_name'], unique=False)
    op.drop_index('ix_customers_last_name', table_name='customers')
    op.create_index(op.f('ix_customers_last_name'), 'customers', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customers_last_name'), table_name='customers')
    op.create_index('ix_customers_last_name', 'customers', ['last_name'], unique=True)
    op.drop_index(op.f('ix_customers_first_name'), table_name='customers')
    op.create_index('ix_customers_first_name', 'customers', ['first_name'], unique=True)
    # ### end Alembic commands ###
