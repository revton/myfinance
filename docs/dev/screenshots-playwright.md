# 📸 Atualização de Screenshots com Playwright

Este diretório contém scripts para automatizar a navegação pelo aplicativo MyFinance e atualizar os screenshots da documentação do usuário.

## 📁 Estrutura de Arquivos

- `playwright_tests.py` - Script principal de automação
- `run_playwright.bat` - Script para executar no Windows
- `run_playwright.sh` - Script para executar em sistemas Unix/Linux/macOS
- `screenshots/` - Diretório onde os screenshots são salvos

## 🚀 Como Usar

### No Windows:

```cmd
npm run playwright-run-windows
```

Ou execute diretamente:

```cmd
run_playwright.bat
```

### No Linux/macOS:

```bash
npm run playwright-run-unix
```

Ou execute diretamente:

```bash
bash run_playwright.sh
```

### Execução Manual:

```bash
# Instalar Playwright (se necessário)
npm run playwright-install

# Executar os testes
npm run playwright-run
```

## ⚙️ Configuração

O script está configurado para acessar a URL padrão do Vercel:
`https://myfinance.vercel.app`

Se você quiser testar localmente, edite o arquivo `playwright_tests.py` e altere a variável `APP_URL`:

```python
# APP_URL = "https://myfinance.vercel.app"  # URL padrão do Vercel
APP_URL = "http://localhost:5173"  # Para testes locais
```

## 📷 O que o Script Faz

1. Abre o navegador Chromium
2. Navega para a página inicial do aplicativo
3. Tira um screenshot da página inicial
4. Procura e clica em links de login/registro (se existirem)
5. Navega pelo menu principal (se existir)
6. Acessa links importantes da página
7. Salva todos os screenshots na pasta `screenshots/` com nomes sequenciais

## 📁 Diretório de Screenshots

Os screenshots são salvos na pasta `screenshots/` com o seguinte padrão de nomenclatura:

- `01_initial_page_YYYYMMDD_HHMMSS.png` - Página inicial
- `02_login_page_YYYYMMDD_HHMMSS.png` - Página de login
- `03_signup_page_YYYYMMDD_HHMMSS.png` - Página de registro
- `04_menu_X_YYYYMMDD_HHMMSS.png` - Itens do menu
- `05_link_X_YYYYMMDD_HHMMSS.png` - Links da página

## 📚 Documentação Atualizada

A documentação do usuário foi atualizada para referenciar os screenshots gerados:

- `docs/user/index.md` - Documentação principal
- `docs/user/autenticacao-guia-usuario.md` - Guia de autenticação

## 🛠️ Personalização

Você pode personalizar o comportamento do script editando `playwright_tests.py`:

1. **Adicionar mais páginas específicas**: Modifique a função `navigate_app()`
2. **Alterar seletores**: Atualize os seletores CSS para corresponder ao seu aplicativo
3. **Modificar tempo de espera**: Ajuste os valores em `page.wait_for_timeout()`
4. **Adicionar mais validações**: Inclua verificações de texto ou elementos

## 🐛 Solução de Problemas

### Playwright não encontrado
```bash
npm run playwright-install
```

### Erros de conexão
Verifique se a URL do aplicativo está correta no arquivo `playwright_tests.py`

### Screenshots não atualizados
Verifique se o diretório `screenshots/` tem permissões de escrita

## 📝 Notas

- O script é executado em modo headful (com interface visível) para facilitar a depuração
- Os screenshots são salvos com timestamp para evitar conflitos
- O script limita o número de páginas navegadas para evitar execuções muito longas