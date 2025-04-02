"""add content column to post table

Revision ID: 59a229fed9a3
Revises: 6223f63b0000
Create Date: 2025-04-01 18:21:20.908454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59a229fed9a3'
down_revision = '6223f63b0000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
