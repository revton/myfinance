from invoke import task
import os

@task
def backend(c, port=8002):
    """Inicia o backend FastAPI na porta especificada (padrão: 8002), acessível na rede."""
    c.run(f"uv run uvicorn src.main:app --reload --host 0.0.0.0 --port {port}")

@task
def frontend(c):
    """Inicia o frontend React (Vite) permitindo acesso externo."""
    with c.cd('frontend'):
        c.run("npm install")
        c.run("npm run dev -- --host")

@task
def docs(c, port=8001):
    """Inicia a documentação MkDocs na porta especificada (padrão: 8001), acessível na rede."""
    c.run(f"uv run mkdocs serve -a 0.0.0.0:{port}")

@task
def run_all(c):
    """Inicia backend, frontend e docs em janelas/abas separadas do terminal (Windows)."""
    c.run('start cmd /k "uv run invoke backend"', pty=False)
    c.run('start cmd /k "uv run invoke frontend"', pty=False)
    c.run('start cmd /k "uv run invoke docs"', pty=False)

@task
def test_backend(c):
    """Executa os testes do backend com pytest."""
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
    c.run("uv run pytest --cov=src --cov-report=term-missing")

@task
def security_backend(c):
    """Valida vulnerabilidades nas dependências Python (backend e docs) usando safety."""
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
        c.run("npx eslint src --format html -o ../reports/eslint-report.html")
    print('Relatório HTML do ESLint gerado em reports/eslint-report.html')

@task
def test_frontend_coverage_html(c):
    """Executa os testes do frontend e gera relatório de cobertura em HTML."""
    with c.cd('frontend'):
        c.run("npm run test -- --coverage")
    # Move o relatório HTML para fora da pasta frontend
    import shutil, os
    src = 'frontend/coverage/lcov-report'
    dst = 'reports/coverage-frontend/lcov-report'
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    print('Relatório HTML de cobertura gerado em reports/coverage-frontend/lcov-report/index.html')

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
    # Backend: coverage.xml (htmlcov) e xunit
    os.makedirs('htmlcov', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    c.run("uv run pytest --cov=src --cov-report=xml:htmlcov/coverage.xml --cov-report=html --junitxml=reports/pytest-xunit.xml")
    # Frontend: lcov
    with c.cd('frontend'):
        c.run("npm run test -- --coverage")
    # lcov.info já estará em reports/coverage-frontend/lcov.info
    print('Relatórios de cobertura e xunit prontos para SonarQube!') 