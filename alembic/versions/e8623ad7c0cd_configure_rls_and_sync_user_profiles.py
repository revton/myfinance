"""configure_rls_and_sync_user_profiles

Revision ID: e8623ad7c0cd
Revises: d5c074db4dc5
Create Date: 2025-08-01 19:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e8623ad7c0cd'
down_revision = 'd5c074db4dc5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Configurar RLS (Row Level Security) para Supabase ###
    # Habilitar RLS na tabela user_profiles
    op.execute("ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;")
    
    # Criar política para usuários autenticados poderem ver apenas seus próprios perfis
    op.execute("""
        CREATE POLICY "Users can view own profile" ON user_profiles
        FOR SELECT USING (auth.uid()::text = user_id::text);
    """)
    
    # Criar política para usuários autenticados poderem inserir seus próprios perfis
    op.execute("""
        CREATE POLICY "Users can insert own profile" ON user_profiles
        FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);
    """)
    
    # Criar política para usuários autenticados poderem atualizar seus próprios perfis
    op.execute("""
        CREATE POLICY "Users can update own profile" ON user_profiles
        FOR UPDATE USING (auth.uid()::text = user_id::text);
    """)
    
    # Criar política para usuários autenticados poderem deletar seus próprios perfis
    op.execute("""
        CREATE POLICY "Users can delete own profile" ON user_profiles
        FOR DELETE USING (auth.uid()::text = user_id::text);
    """)
    
    # ### Sincronizar com PostgREST (Supabase) ###
    # Notificar PostgREST sobre a nova tabela
    op.execute("NOTIFY pgrst, 'reload schema';")
    
    # ### Configurar permissões para o schema public ###
    # Garantir que o schema public está acessível
    op.execute("GRANT USAGE ON SCHEMA public TO anon, authenticated;")
    op.execute("GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;")
    op.execute("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;")
    op.execute("GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;")
    
    # Configurar permissões específicas para a tabela user_profiles
    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON user_profiles TO anon, authenticated;")


def downgrade() -> None:
    # ### Remover políticas RLS ###
    op.execute("DROP POLICY IF EXISTS \"Users can view own profile\" ON user_profiles;")
    op.execute("DROP POLICY IF EXISTS \"Users can insert own profile\" ON user_profiles;")
    op.execute("DROP POLICY IF EXISTS \"Users can update own profile\" ON user_profiles;")
    op.execute("DROP POLICY IF EXISTS \"Users can delete own profile\" ON user_profiles;")
    
    # Desabilitar RLS
    op.execute("ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY;")
    
    # ### Remover permissões ###
    op.execute("REVOKE SELECT, INSERT, UPDATE, DELETE ON user_profiles FROM anon, authenticated;") 