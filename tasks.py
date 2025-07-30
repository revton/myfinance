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
    c.run(f"uv run uvicorn src.main:app --reload --host {api_host} --port {api_port}")

@task
def frontend(c):
    """Inicia o frontend React (Vite) permitindo acesso externo."""
    with c.cd('frontend'):
        c.run("npm install")
        c.run("npm run dev -- --host")

@task
def docs(c, port=None):
    """Inicia a documentação MkDocs na porta especificada ou da variável de ambiente."""
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