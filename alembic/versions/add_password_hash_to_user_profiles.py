"""add password_hash to user_profiles

Revision ID: add_password_hash
Revises: e8623ad7c0cd
Create Date: 2025-08-06 10:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_password_hash'
down_revision = 'e8623ad7c0cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar coluna password_hash à tabela user_profiles
    op.add_column('user_profiles', sa.Column('password_hash', sa.String(255), nullable=True))


def downgrade() -> None:
    # Remover coluna password_hash da tabela user_profiles
    op.drop_column('user_profiles', 'password_hash') 