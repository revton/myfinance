from invoke import task
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

@task
def backend(c, port=None, env=None):
    """Inicia o backend FastAPI na porta especificada ou da variável de ambiente."""
    # Define ambiente se especificado
    if env:
        os.environ["ENVIRONMENT"] = env
        print(f"Executando backend em ambiente: {env}")
    
    api_port = port or os.getenv("API_PORT", "8002")
    api_host = os.getenv("API_HOST", "0.0.0.0")
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"Backend iniciando em {api_host}:{api_port} (ambiente: {environment})")
    print("Usando SQLAlchemy direto com Supabase")
    c.run(f"uv run uvicorn src.main:app --reload --host {api_host} --port {api_port}")

@task
def test_sqlalchemy_migration(c):
    """Testa a migração para SQLAlchemy direto."""
    print("Testando migração para SQLAlchemy...")
    c.run("uv run python scripts/test_sqlalchemy_migration.py")

@task
def test_database_connection(c):
    """Testa a conexão direta com o banco via SQLAlchemy."""
    print("Testando conexão com banco via SQLAlchemy...")
    c.run("uv run python scripts/test_supabase_sqlalchemy.py")

@task
def frontend(c, port=5173):
    """Inicia o frontend React/Vite na porta especificada (padrão: 5173)."""
    frontend_port = port or os.getenv("VITE_PORT", "5173")
    c.run(f"cd frontend && npm run dev -- --port {frontend_port}")

@task
def docs(c, port=8001):
    """Inicia a documentação MkDocs na porta especificada (padrão: 8001), acessível na rede."""
    docs_port = port or os.getenv("DOCS_PORT", "8001")
    c.run(f"uv run mkdocs serve -a 0.0.0.0:{docs_port}")

@task
def run_all(c):
    """Inicia backend, frontend e docs em janelas/abas separadas do terminal (Windows)."""
    c.run('start cmd /k "uv run invoke backend"', pty=False)
    c.run('start cmd /k "uv run invoke frontend"', pty=False)
    c.run('start cmd /k "uv run invoke docs"', pty=False)

@task
def test_backend(c):
    """Executa os testes do backend com pytest usando mocks."""
    print("Executando testes com mocks (sem conexão real com Supabase)")
    c.run("uv run pytest")

@task
def test_frontend(c):
    """Executa os testes do frontend com npm test."""
    with c.cd('frontend'):
        c.run("npm test")

@task
def test_all(c):
    """Executa todos os testes (backend e frontend)."""
    c.run("uv run invoke test-backend")
    c.run("uv run invoke test-frontend")

@task
def test_coverage(c):
    """Executa os testes do backend e gera relatório de cobertura."""
    print("Executando testes com mocks (sem conexão real com Supabase)")
    c.run("uv run pytest --cov=src --cov-report=term-missing --cov-report=html")
    print('Relatório HTML gerado em htmlcov/index.html')

@task
def security_backend(c):
    """Valida vulnerabilidades nas dependências Python (backend e docs) usando safety."""
    # TODO: Migrar para 'safety scan' quando necessário (requer login)
    c.run("uv run safety check")

@task
def security_frontend(c):
    """Valida vulnerabilidades nas dependências do frontend (Node.js) usando npm audit."""
    with c.cd('frontend'):
        c.run("npm audit")

@task
def quality_ruff(c):
    """Roda o ruff para análise de qualidade e estilo do código Python."""
    c.run("uv run ruff check src tests")

@task
def quality_ruff_fix(c):
    """Roda o ruff com --fix para corrigir automaticamente problemas de estilo em src e tests."""
    c.run("uv run ruff check src tests --fix")

@task
def quality_radon_cc(c):
    """Mede a complexidade ciclomática do código Python com radon."""
    c.run("uv run radon cc -s -a src tests")

@task
def quality_radon_mi(c):
    """Mede o índice de manutenibilidade do código Python com radon."""
    c.run("uv run radon mi -s src tests")

@task
def quality_radon_raw(c):
    """Mostra métricas brutas do código Python com radon."""
    c.run("uv run radon raw src tests")

@task
def quality_radon_all(c):
    """Executa todas as métricas do radon (cc, mi, raw)."""
    c.run("uv run invoke quality-radon-cc")
    c.run("uv run invoke quality-radon-mi")
    c.run("uv run invoke quality-radon-raw")

@task
def test_coverage_html(c):
    """Executa os testes do backend e gera relatório de cobertura em HTML."""
    print("Executando testes com mocks (sem conexão real com Supabase)")
    c.run("uv run pytest --cov=src --cov-report=html")
    print('Relatório HTML gerado em htmlcov/index.html')

@task
def quality_bandit(c):
    """Roda o bandit para análise de segurança do código Python."""
    os.makedirs("reports", exist_ok=True)
    c.run("uv run bandit -r src -f html -o reports/bandit-report.html")
    print('Relatório HTML de segurança gerado em reports/bandit-report.html')

@task
def quality_eslint_html(c):
    """Roda o ESLint no frontend e gera relatório HTML na pasta reports/ (fora do versionamento)."""
    os.makedirs("reports", exist_ok=True)
    with c.cd('frontend'):
        c.run("npx eslint src --format html -o ../reports/eslint-report.html", warn=True)
    print('Relatório HTML do ESLint gerado em reports/eslint-report.html')

@task
def test_frontend_coverage_html(c):
    """Executa os testes do frontend e gera relatório de cobertura em HTML."""
    with c.cd('frontend'):
        c.run("npm run test -- --coverage")
    # Move o relatório HTML para fora da pasta frontend
    import shutil, os
    src = 'frontend/coverage'
    dst = 'reports/coverage-frontend'
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    print('Relatório HTML de cobertura gerado em reports/coverage-frontend/index.html')

@task
def quality_plato(c):
    """Gera relatório de métricas do frontend com Plato."""
    import os
    os.makedirs('reports/plato-report', exist_ok=True)
    with c.cd('frontend'):
        c.run("npx plato -r -d ../reports/plato-report src")
    print('Relatório HTML do Plato gerado em reports/plato-report/index.html')

@task
def quality_frontend_all(c):
    """Executa todas as métricas e relatórios do frontend (ESLint, cobertura, Plato)."""
    c.run("uv run invoke quality-eslint-html")
    c.run("uv run invoke test-frontend-coverage-html")
    c.run("uv run invoke quality-plato") 

@task
def coverage_all_reports(c):
    """Gera todos os relatórios de cobertura e xunit para SonarQube."""
    import os
    print("Executando testes com mocks (sem conexão real com Supabase)")
    
    # Backend: coverage.xml (htmlcov) e xunit
    os.makedirs('htmlcov', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    c.run("uv run pytest --cov=src --cov-report=xml:htmlcov/coverage.xml --cov-report=html --junitxml=reports/pytest-xunit.xml")
    # Frontend: lcov
    with c.cd('frontend'):
        c.run("npm run test -- --coverage")
    # lcov.info já estará em reports/coverage-frontend/lcov.info
    print('Relatórios de cobertura e xunit prontos para SonarQube!')
    print('Execute: sonar-scanner (token já configurado na variável SONAR_TOKEN)')

@task
def setup_env(c):
    """Cria arquivo .env baseado no env.example se não existir."""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print('Arquivo .env criado baseado no env.example')
            print('Configure as variáveis no arquivo .env antes de executar a aplicação')
        else:
            print('Arquivo env.example não encontrado')
    else:
        print('Arquivo .env já existe')

@task
def check_env(c):
    """Verifica se as variáveis de ambiente necessárias estão configuradas."""
    environment = os.getenv("ENVIRONMENT", "development")
    print(f"Verificando configuração para ambiente: {environment}")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f'Variáveis de ambiente ausentes: {", ".join(missing_vars)}')
        print('Configure estas variáveis no arquivo .env')
        return False
    else:
        print(f'Variáveis de ambiente configuradas para {environment}')
        return True

@task
def switch_env(c, env):
    """Altera o ambiente atual no arquivo .env."""
    if env not in ['development', 'production']:
        print('Ambiente deve ser: development ou production')
        return
    
    if not os.path.exists('.env'):
        print('Arquivo .env não encontrado. Execute "uv run invoke setup-env" primeiro.')
        return
    
    # Lê o arquivo .env
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Atualiza a linha ENVIRONMENT
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('ENVIRONMENT='):
            lines[i] = f'ENVIRONMENT={env}\n'
            updated = True
            break
    
    if not updated:
        # Adiciona se não existir
        lines.append(f'ENVIRONMENT={env}\n')
    
    # Escreve de volta
    with open('.env', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f'Ambiente alterado para: {env}')
    print('⚠️  IMPORTANTE: Configure SUPABASE_URL e SUPABASE_ANON_KEY para o novo ambiente!')
    print('Execute "uv run invoke check-env" para verificar a configuração')

@task
def show_env(c):
    """Mostra o ambiente atual e suas configurações."""
    environment = os.getenv("ENVIRONMENT", "development")
    print(f"Ambiente atual: {environment}")
    print()
    
    url = os.getenv("SUPABASE_URL", "Não configurado")
    key = os.getenv("SUPABASE_ANON_KEY", "Não configurado")
    print(f"SUPABASE_URL: {url}")
    print(f"SUPABASE_ANON_KEY: {key[:10]}..." if len(key) > 10 else f"SUPABASE_ANON_KEY: {key}")
    
    print()
    print(f"API_PORT: {os.getenv('API_PORT', '8002')}")
    print(f"DEBUG: {os.getenv('DEBUG', 'True')}")
    print(f"LOG_LEVEL: {os.getenv('LOG_LEVEL', 'INFO')}") 

@task
def generate_schema(c):
    """Gera schema SQL baseado nos modelos Pydantic do FastAPI."""
    print("Gerando schema SQL baseado nos modelos Pydantic...")
    c.run("uv run python scripts/generate_schema.py")

@task
def test_schema(c):
    """Testa se o schema foi aplicado corretamente no Supabase."""
    print("Testando schema aplicado no Supabase...")
    c.run("uv run python scripts/generate_schema.py --test")

@task
def setup_database(c):
    """Configura o banco de dados no Supabase baseado nos modelos Pydantic."""
    print("Configurando banco de dados baseado nos modelos Pydantic...")
    print("1. Gerando schema SQL...")
    c.run("uv run invoke generate-schema")
    print()
    print("2. Execute o SQL gerado no Supabase SQL Editor")
    print("3. Teste a configuração com: uv run invoke test-schema") 

# =============================================================================
# TAREFAS DE MIGRAÇÃO COM ALEMBIC
# =============================================================================

@task
def migrate_init(c):
    """Cria a migração inicial baseada nos modelos Pydantic."""
    print("Criando migração inicial baseada nos modelos Pydantic...")
    c.run("uv run python scripts/migrate_database.py")

@task
def migrate_generate(c, message):
    """Gera uma nova migração baseada nos modelos."""
    print(f"Gerando migração: {message}")
    c.run(f'uv run alembic revision --autogenerate -m "{message}"')

@task
def migrate_upgrade(c):
    """Aplica as migrações pendentes."""
    print("Aplicando migrações pendentes...")
    c.run("uv run alembic upgrade head")

@task
def migrate_status(c):
    """Mostra o status das migrações."""
    print("Status das migrações:")
    c.run("uv run alembic current")

@task
def migrate_history(c):
    """Mostra o histórico de migrações."""
    print("Histórico de migrações:")
    c.run("uv run alembic history")

@task
def migrate_downgrade(c, revision):
    """Reverte para uma revisão específica."""
    print(f"Revertendo para revisão: {revision}")
    c.run(f"uv run alembic downgrade {revision}")

@task
def setup_migrations(c):
    """Configura o sistema de migrações completo."""
    print("🚀 Configurando sistema de migrações com Pydantic e Alembic")
    print("=" * 60)
    
    # Verifica ambiente
    if not check_env(c):
        print("❌ Configure o ambiente primeiro")
        return
    
    # Verifica DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado")
        print("💡 Configure DATABASE_URL no .env com a URL do banco Supabase")
        return
    
    print("✅ Ambiente configurado")
    print()
    print("🎯 Próximos passos:")
    print("1. Execute: uv run invoke migrate-init")
    print("2. Revise a migração gerada em alembic/versions/")
    print("3. Execute: uv run invoke migrate-upgrade")
    print("4. Teste com: uv run invoke test-backend") 