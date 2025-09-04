"""add_revoked_tokens_table

Revision ID: 8b6b7108caa1
Revises: 49c69a18767d
Create Date: 2025-09-03 20:20:58.375339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b6b7108caa1'
down_revision = '49c69a18767d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'revoked_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(length=36), nullable=False),
        sa.Column('token_type', sa.String(length=10), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criar índices para melhorar a performance das consultas
    op.create_index('ix_revoked_tokens_jti', 'revoked_tokens', ['jti'], unique=True)
    op.create_index('ix_revoked_tokens_user_id', 'revoked_tokens', ['user_id'], unique=False)
    op.create_index('ix_revoked_tokens_expires_at', 'revoked_tokens', ['expires_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_revoked_tokens_expires_at', table_name='revoked_tokens')
    op.drop_index('ix_revoked_tokens_user_id', table_name='revoked_tokens')
    op.drop_index('ix_revoked_tokens_jti', table_name='revoked_tokens')
    op.drop_table('revoked_tokens')