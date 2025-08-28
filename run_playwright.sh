#!/usr/bin/env bash

# Script para instalar e executar Playwright

echo "Instalando Playwright..."
uv pip install playwright
playwright install chromium

echo "Executando testes de navegação..."
python playwright_tests.py

echo "Processo concluído!"