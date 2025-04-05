"""Rename fields in Task table

Revision ID: 70b62f66c64a
Revises: 6061c5eb5eea
Create Date: 2025-04-02 21:11:03.890872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '70b62f66c64a'
down_revision: Union[str, None] = '6061c5eb5eea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'user', ['username'])
    op.add_column('task', sa.Column('customer_name', sa.String(), nullable=False))
    op.add_column('task', sa.Column('performer_name', sa.String(), nullable=False))
    op.drop_constraint('task_customer_id_fkey', 'task', type_='foreignkey')
    op.drop_constraint('task_performer_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'user', ['performer_name'], ['username'], ondelete='CASCADE')
    op.create_foreign_key(None, 'task', 'user', ['customer_name'], ['username'], ondelete='CASCADE')
    op.drop_column('task', 'performer_id')
    op.drop_column('task', 'customer_id')


def downgrade() -> None:
    op.drop_constraint(None, 'user', type_='unique')
    op.add_column('task', sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('task', sa.Column('performer_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_performer_id_fkey', 'task', 'user', ['performer_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('task_customer_id_fkey', 'task', 'user', ['customer_id'], ['id'], ondelete='CASCADE')
    op.drop_column('task', 'performer_name')
    op.drop_column('task', 'customer_name')
