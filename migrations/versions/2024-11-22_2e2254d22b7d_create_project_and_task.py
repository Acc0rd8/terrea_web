"""Create Project and Task

Revision ID: 2e2254d22b7d
Revises: c36d059fe5d7
Create Date: 2024-11-22 13:15:31.317556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e2254d22b7d'
down_revision: Union[str, None] = 'c36d059fe5d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('project')
    # ### end Alembic commands ###