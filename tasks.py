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
def security_backend(c):
    """Valida vulnerabilidades nas dependências Python (backend e docs) usando safety."""
    c.run("uv run safety check")

@task
def security_frontend(c):
    """Valida vulnerabilidades nas dependências do frontend (Node.js) usando npm audit."""
    with c.cd('frontend'):
        c.run("npm audit") 