"""add create-date and remove unit-per-floor field from house table

Revision ID: deda2701efe4
Revises: 
Create Date: 2023-10-17 16:12:04.751960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'deda2701efe4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('houses', sa.Column('create_date', sa.TIMESTAMP, server_default=sa.func.now()))
    op.drop_column('houses', 'unit_per_floor')
    op.alter_column('houses', 'Building_infrastructure', new_column_name='building_infrastructure')


def downgrade() -> None:
    raise NotImplemented
