"""Add relationships

Revision ID: 260f6aa83c15
Revises: 2e2254d22b7d
Create Date: 2024-11-24 14:51:47.506877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '260f6aa83c15'
down_revision: Union[str, None] = '2e2254d22b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('owner_id', sa.Integer(), nullable=False, server_default='9'))
    op.create_foreign_key(None, 'project', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
    op.alter_column('project', 'owner_id', server_default=None)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'owner_id')
    # ### end Alembic commands ###
