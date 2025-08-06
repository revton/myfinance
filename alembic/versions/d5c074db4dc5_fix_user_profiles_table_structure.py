"""fix_user_profiles_table_structure

Revision ID: d5c074db4dc5
Revises: 9feb93f37ce2
Create Date: 2025-08-01 19:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd5c074db4dc5'
down_revision = '9feb93f37ce2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Verificar se a tabela user_profiles existe e tem a estrutura correta ###
    connection = op.get_bind()
    
    # Verificar se a tabela existe
    result = connection.execute(sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'user_profiles'
        );
    """))
    
    table_exists = result.scalar()
    
    if not table_exists:
        # Criar a tabela se não existir
        op.create_table('user_profiles',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('full_name', sa.String(length=255), nullable=True),
            sa.Column('avatar_url', sa.Text(), nullable=True),
            sa.Column('timezone', sa.String(length=50), nullable=False, server_default='America/Sao_Paulo'),
            sa.Column('currency', sa.String(length=3), nullable=False, server_default='BRL'),
            sa.Column('language', sa.String(length=5), nullable=False, server_default='pt-BR'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id'),
            sa.CheckConstraint("timezone IN ('America/Sao_Paulo', 'UTC', 'America/New_York', 'Europe/London')", name='check_valid_timezone'),
            sa.CheckConstraint("currency IN ('BRL', 'USD', 'EUR', 'GBP')", name='check_valid_currency'),
            sa.CheckConstraint("language IN ('pt-BR', 'en-US', 'es-ES')", name='check_valid_language'),
            sa.CheckConstraint("length(email) >= 3", name='check_email_length'),
            sa.CheckConstraint("length(full_name) <= 255", name='check_full_name_length')
        )
        
        # Criar índices
        op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'], unique=False)
        op.create_index('idx_user_profiles_email', 'user_profiles', ['email'], unique=False)
        op.create_index('idx_user_profiles_created_at', 'user_profiles', ['created_at'], unique=False)
    else:
        # Verificar se os índices existem
        result = connection.execute(sa.text("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename = 'user_profiles' 
            AND indexname = 'idx_user_profiles_user_id';
        """))
        
        if not result.fetchone():
            op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'], unique=False)
        
        result = connection.execute(sa.text("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename = 'user_profiles' 
            AND indexname = 'idx_user_profiles_email';
        """))
        
        if not result.fetchone():
            op.create_index('idx_user_profiles_email', 'user_profiles', ['email'], unique=False)
        
        result = connection.execute(sa.text("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename = 'user_profiles' 
            AND indexname = 'idx_user_profiles_created_at';
        """))
        
        if not result.fetchone():
            op.create_index('idx_user_profiles_created_at', 'user_profiles', ['created_at'], unique=False)


def downgrade() -> None:
    # ### Remover índices se existirem ###
    connection = op.get_bind()
    
    # Verificar se os índices existem antes de tentar removê-los
    result = connection.execute(sa.text("""
        SELECT indexname FROM pg_indexes 
        WHERE tablename = 'user_profiles' 
        AND indexname = 'idx_user_profiles_created_at';
    """))
    
    if result.fetchone():
        op.drop_index('idx_user_profiles_created_at', table_name='user_profiles')
    
    result = connection.execute(sa.text("""
        SELECT indexname FROM pg_indexes 
        WHERE tablename = 'user_profiles' 
        AND indexname = 'idx_user_profiles_email';
    """))
    
    if result.fetchone():
        op.drop_index('idx_user_profiles_email', table_name='user_profiles')
    
    result = connection.execute(sa.text("""
        SELECT indexname FROM pg_indexes 
        WHERE tablename = 'user_profiles' 
        AND indexname = 'idx_user_profiles_user_id';
    """))
    
    if result.fetchone():
        op.drop_index('idx_user_profiles_user_id', table_name='user_profiles') 