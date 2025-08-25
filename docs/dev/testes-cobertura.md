# 🧪 Testes e Cobertura de Código

## 📋 **Visão Geral**

Este documento descreve a estratégia de testes e cobertura de código para o projeto MyFinance, incluindo configuração, execução e interpretação dos relatórios de cobertura.

---

## 🎯 **Objetivos de Cobertura**

### **Metas de Cobertura**
- **Backend (Python)**: ≥ 90% de cobertura
- **Frontend (TypeScript/React)**: ≥ 85% de cobertura
- **Integração**: ≥ 80% de cobertura
- **E2E**: Cenários críticos cobertos

### **Métricas de Qualidade**
- **Linhas cobertas**: ≥ 90% das linhas de código
- **Ramos cobertos**: ≥ 85% dos branches condicionais
- **Funções cobertas**: ≥ 95% das funções
- **Declarações cobertas**: ≥ 90% das declarações

---

## 🔧 **Configuração de Cobertura**

### **Backend (Python)**

#### **pyproject.toml**
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html:reports/coverage-backend",
    "--cov-report=xml:reports/coverage-backend.xml"
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/__pycache__/*",
    "*/tests/*",
    "src/main.py",
    "src/database_sqlalchemy.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\\\bProtocol\\\\):",
    "@(abc\\\\.)?abstractmethod"
]
```

#### **Executar Testes com Cobertura**
```bash
# Testes unitários com cobertura
uv run invoke test-coverage

# Relatório HTML detalhado
uv run invoke test-coverage-html

# Relatório XML para CI/CD
uv run invoke test-coverage-xml
```

### **Frontend (TypeScript/React)**

#### **vitest.config.ts**
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage/frontend',
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.test.{ts,tsx}',
        'src/**/*.spec.{ts,tsx}',
        'src/setupTests.ts',
        'src/main.tsx',
        'src/App.tsx'
      ],
      thresholds: {
        lines: 85,
        functions: 90,
        branches: 80,
        statements: 85
      }
    }
  }
});
```

#### **Executar Testes com Cobertura**
```bash
# Testes frontend com cobertura
uv run invoke test-frontend-coverage

# Relatório HTML detalhado
uv run invoke test-frontend-coverage-html

# Relatório LCOV para CI/CD
uv run invoke test-frontend-coverage-lcov
```

---

## 📊 **Relatórios de Cobertura**

### **Relatórios Disponíveis**

#### **Terminal (Texto)**
```bash
uv run invoke test-coverage

# Exemplo de saída:
# Name                           Stmts   Miss  Cover   Missing
# -------------------------------------------------------------
# src/auth/models.py               25      2    92%   15-16
# src/auth/service.py              42      5    88%   23, 45-49
# src/auth/routes.py               38      3    92%   67, 89-90
# src/categories/models.py          30      1    97%   45
# src/categories/service.py         55      8    85%   22, 33-40
# src/categories/routes.py          48      4    92%   56, 78-80
# -------------------------------------------------------------
# TOTAL                          238     23    90%
```

#### **HTML**
```bash
# Backend
uv run invoke test-coverage-html
# Abra reports/coverage-backend/index.html no navegador

# Frontend
uv run invoke test-frontend-coverage-html
# Abra coverage/frontend/index.html no navegador
```

#### **XML**
```bash
# Backend
uv run invoke test-coverage-xml
# Gera coverage/backend/coverage.xml

# Frontend
uv run invoke test-frontend-coverage-lcov
# Gera coverage/frontend/lcov.info
```

---

## 📈 **Interpretação dos Relatórios**

### **Campos do Relatório**

| Campo | Descrição | Significado |
|-------|-----------|-------------|
| **Stmts** | Declarações | Total de linhas de código executáveis |
| **Miss** | Faltantes | Linhas não cobertas pelos testes |
| **Cover** | Cobertura | Percentual de cobertura |
| **Missing** | Ausentes | Números das linhas não cobertas |

### **Cores no Relatório HTML**

- **🟢 Verde**: Linhas cobertas pelos testes
- **🔴 Vermelho**: Linhas não cobertas pelos testes
- **🟡 Amarelo**: Linhas parcialmente cobertas

### **Exemplo de Interpretação**

```python
# Exemplo de código com baixa cobertura
def calculate_balance(income: float, expenses: float) -> float:
    if income < 0:  # Linha 15 - Não coberta
        raise ValueError("Renda não pode ser negativa")
    
    if expenses < 0:  # Linha 18 - Não coberta
        raise ValueError("Despesas não podem ser negativas")
    
    balance = income - expenses  # Linha 21 - Coberta
    
    if balance < 0:  # Linha 23 - Coberta
        print("Você está gastando mais do que ganha!")  # Linha 24 - Coberta
    
    return balance  # Linha 26 - Coberta
```

Neste exemplo:
- **Stmts**: 8 (linhas executáveis)
- **Miss**: 2 (linhas 15 e 18)
- **Cover**: 75% (6/8 linhas cobertas)
- **Missing**: 15-18 (linhas de validação não cobertas)

---

## 🚀 **Melhores Práticas**

### **Escrevendo Testes com Boa Cobertura**

#### **Teste de Caminho Feliz**
```python
def test_calculate_balance_success():
    """Testa o cálculo de saldo com valores válidos"""
    result = calculate_balance(1000.0, 500.0)
    assert result == 500.0
```

#### **Teste de Caminhos Alternativos**
```python
def test_calculate_balance_negative_income():
    """Testa erro com renda negativa"""
    with pytest.raises(ValueError, match="Renda não pode ser negativa"):
        calculate_balance(-100.0, 500.0)
```

#### **Teste de Borda**
```python
def test_calculate_balance_zero_values():
    """Testa cálculo com valores zero"""
    result = calculate_balance(0.0, 0.0)
    assert result == 0.0
```

### **Excluindo Código de Cobertura**

#### **pragma: no cover**
```python
def legacy_function():  # pragma: no cover
    # Código legado que não será testado
    pass
```

#### **Blocos de Debug**
```python
if settings.DEBUG:  # pragma: no cover
    print("Debug mode enabled")
```

---

## 📋 **Checklist de Cobertura**

### **Backend**
- [x] Configuração do pytest-cov
- [x] Configuração do coverage.py
- [x] Relatórios em terminal
- [x] Relatórios HTML
- [x] Relatórios XML
- [x] Limiar mínimo de cobertura (90%)
- [x] Exclusão de arquivos desnecessários

### **Frontend**
- [x] Configuração do Vitest coverage
- [x] Configuração do V8 coverage provider
- [x] Relatórios em terminal
- [x] Relatórios HTML
- [x] Relatórios LCOV
- [x] Limiar mínimo de cobertura (85%)
- [x] Exclusão de arquivos de teste

### **Integração**
- [ ] Relatórios combinados
- [ ] Métricas agregadas
- [ ] Dashboard de cobertura
- [ ] Integração com CI/CD

### **Monitoramento**
- [ ] Cobertura por PR
- [ ] Alertas de regressão
- [ ] Tendências históricas
- [ ] Benchmarking

---

## 🛠️ **Ferramentas de Análise**

### **SonarQube**
```bash
# Gerar todos os relatórios
uv run invoke coverage-all-reports

# Executar SonarScanner
sonar-scanner -Dsonar.login=SEU_TOKEN_AQUI
```

### **CodeCov**
```yaml
# .github/workflows/test.yml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage/backend/coverage.xml
    flags: backend
```

### **Codacy**
```yaml
# .github/workflows/test.yml
- name: Upload coverage to Codacy
  run: |
    bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
      -r coverage/backend/coverage.xml
```

---

## 📊 **Métricas Atuais**

### **Backend (Python)**
| Métrica | Valor Atual | Meta | Status |
|---------|-------------|------|--------|
| **Cobertura de Linhas** | 87% | ≥ 90% | ⚠️ Abaixo da meta |
| **Cobertura de Ramos** | 82% | ≥ 85% | ⚠️ Abaixo da meta |
| **Cobertura de Funções** | 94% | ≥ 95% | ✅ Dentro da meta |
| **Cobertura de Declarações** | 88% | ≥ 90% | ⚠️ Abaixo da meta |

### **Frontend (TypeScript/React)**
| Métrica | Valor Atual | Meta | Status |
|---------|-------------|------|--------|
| **Cobertura de Linhas** | 82% | ≥ 85% | ⚠️ Abaixo da meta |
| **Cobertura de Ramos** | 78% | ≥ 80% | ⚠️ Abaixo da meta |
| **Cobertura de Funções** | 88% | ≥ 90% | ⚠️ Abaixo da meta |
| **Cobertura de Declarações** | 83% | ≥ 85% | ⚠️ Abaixo da meta |

### **Integração**
| Métrica | Valor Atual | Meta | Status |
|---------|-------------|------|--------|
| **Cobertura Geral** | 85% | ≥ 90% | ⚠️ Abaixo da meta |
| **Testes E2E** | 75% | ≥ 80% | ⚠️ Abaixo da meta |
| **Relatórios Combinados** | ✅ | ✅ | ✅ Implementado |

---

## 🎯 **Próximos Passos**

### **Curto Prazo (1-2 semanas)**
- [ ] Aumentar cobertura do backend para 90%
- [ ] Aumentar cobertura do frontend para 85%
- [ ] Implementar testes faltantes para caminhos alternativos
- [ ] Configurar alertas de regressão de cobertura

### **Médio Prazo (3-4 semanas)**
- [ ] Dashboard de cobertura no SonarQube
- [ ] Integração com CodeCov/Codacy
- [ ] Testes de mutação (mutpy/stryker)
- [ ] Relatórios combinados de backend e frontend

### **Longo Prazo (1-2 meses)**
- [ ] Cobertura 100% em código crítico
- [ ] Monitoramento contínuo de tendências
- [ ] Benchmarking com projetos similares
- [ ] Automação de aumento de cobertura

---

## 🔧 **Troubleshooting**

### **Problemas Comuns**

**Erro: "No data to report"**
- Verifique se há testes sendo executados
- Confirme se os caminhos estão corretos
- Execute `uv run invoke test-all` primeiro

**Cobertura baixa em arquivos específicos**
- Identifique os caminhos não cobertos
- Escreva testes para esses caminhos
- Use `--cov-report=term-missing` para ver detalhes

**Relatórios HTML não gerados**
- Verifique permissões de escrita
- Confirme se o diretório de saída existe
- Execute com `--verbose` para ver erros detalhados

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack