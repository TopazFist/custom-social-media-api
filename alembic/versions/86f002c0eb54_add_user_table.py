"""add user table

Revision ID: 86f002c0eb54
Revises: 59a229fed9a3
Create Date: 2025-04-01 18:27:00.056458

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "86f002c0eb54"
down_revision = "59a229fed9a3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "email",
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
