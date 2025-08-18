"""Merge heads

Revision ID: 173ad7416018
Revises: add_password_hash, b2f5g4h6i1j3
Create Date: 2025-08-14 14:45:39.101315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '173ad7416018'
down_revision = ('add_password_hash', 'b2f5g4h6i1j3')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 