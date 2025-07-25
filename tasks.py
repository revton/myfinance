from invoke import task
import os

@task
def backend(c, port=8002):
    """Inicia o backend FastAPI na porta especificada (padrão: 8002)."""
    c.run(f".venv\\Scripts\\activate && uvicorn src.main:app --reload --port {port}", pty=True)

@task
def frontend(c):
    """Inicia o frontend React (Vite) permitindo acesso externo."""
    with c.cd('frontend'):
        c.run("npm install", pty=True)
        c.run("npm run dev -- --host", pty=True)

@task
def docs(c, port=8001):
    """Inicia a documentação MkDocs na porta especificada (padrão: 8001)."""
    c.run(f".venv\\Scripts\\activate && mkdocs serve -a 127.0.0.1:{port}", pty=True)

@task
def all(c):
    """Inicia backend, frontend e docs em paralelo (cada um em um terminal)."""
    print("Abra três terminais e execute:\n")
    print("invoke backend")
    print("invoke frontend")
    print("invoke docs")

@task
def test_backend(c):
    """Executa os testes do backend com pytest."""
    c.run(".venv\\Scripts\\activate && pytest", pty=True)

@task
def test_frontend(c):
    """Executa os testes do frontend com npm test."""
    with c.cd('frontend'):
        c.run("npm test", pty=True)

@task
def test_all(c):
    """Executa todos os testes (backend e frontend)."""
    c.run("invoke test_backend", pty=True)
    c.run("invoke test_frontend", pty=True) 