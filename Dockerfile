# Dockerfile para Backend FastAPI
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências
RUN uv pip install --system -r pyproject.toml --extra backend

# Copiar código fonte
COPY src/ ./src/
COPY tests/ ./tests/

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 