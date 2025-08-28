import asyncio
import os
import re
from playwright.async_api import async_playwright, TimeoutError
from datetime import datetime

# URL do aplicativo (substitua pela URL real do seu app)
# APP_URL = "https://myfinance.vercel.app"  # URL padrão do Vercel
APP_URL = "http://localhost:5173"  # Para testes locais

# Credenciais de teste (substitua pelas suas credenciais reais)
TEST_EMAIL = "revtonbr@gmail.com"
TEST_PASSWORD = "4b6e3gmR$"

# Diretório para salvar os screenshots
SCREENSHOTS_DIR = "screenshots"

async def take_screenshot(page, name):
    """Tirar um screenshot e salvá-lo"""
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)
    
    # Sanitizar o nome do arquivo removendo caracteres inválidos
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', name)
    sanitized_name = re.sub(r'\s+', '_', sanitized_name)  # Substituir espaços por underscores
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOTS_DIR}/{sanitized_name}_{timestamp}.png"
    await page.screenshot(path=filename, full_page=True)
    print(f"Screenshot salvo: {filename}")
    return filename

async def navigate_app():
    async with async_playwright() as p:
        # Iniciar o browser
        browser = await p.chromium.launch(headless=False)  # headless=False para ver o processo
        page = await browser.new_page()
        
        try:
            # 1. Página inicial
            print("Acessando a página inicial...")
            await page.goto(APP_URL)
            await page.wait_for_timeout(3000)  # Esperar carregar
            await take_screenshot(page, "01_initial_page")
            
            # 2. Navegar para a página de login (se existir)
            try:
                # Procurar um link de login ou botão
                login_button = await page.wait_for_selector("text=Login", timeout=5000)
                
                if login_button:
                    await login_button.click()
                    await page.wait_for_timeout(2000)
                    await take_screenshot(page, "02_login_page")
                    
                    # Preencher os campos de login
                    try:
                        email_field = await page.wait_for_selector("input[type='email']", timeout=3000)
                        password_field = await page.wait_for_selector("input[type='password']", timeout=3000)
                        
                        if email_field and password_field:
                            await email_field.fill(TEST_EMAIL)
                            await password_field.fill(TEST_PASSWORD)
                            
                            # Procurar e clicar no botão de submit
                            submit_button = await page.wait_for_selector("button[type='submit'], button:has-text('Entrar')", timeout=3000)
                            if submit_button:
                                await submit_button.click()
                                await page.wait_for_timeout(3000)  # Esperar carregar a página após login
                                await take_screenshot(page, "03_logged_in_dashboard")
                                print("Login realizado com sucesso!")
                    except TimeoutError:
                        print("Campos de login não encontrados, continuando...")
            except TimeoutError:
                print("Botão de login não encontrado, continuando...")
            
            # 3. Navegar para a página de registro (se existir)
            try:
                signup_button = await page.wait_for_selector("text=Registrar", timeout=5000)
                if signup_button:
                    await signup_button.click()
                    await page.wait_for_timeout(2000)
                    await take_screenshot(page, "04_signup_page")
            except TimeoutError:
                print("Botão de registro não encontrado, continuando...")
            
            # 4. Navegar pelo menu (se existir)
            try:
                # Procurar elementos do menu
                menu_items = await page.query_selector_all("nav a, .menu a, .navbar a, [role='navigation'] a")
                for i, item in enumerate(menu_items[:5]):  # Limitar a 5 itens para não ficar muito longo
                    try:
                        text = await item.text_content()
                        if text and text.strip():
                            print(f"Navegando para: {text.strip()}")
                            await item.click()
                            await page.wait_for_timeout(2000)
                            await take_screenshot(page, f"05_menu_{i+1}_{text.strip()}")
                            # Voltar para a página anterior
                            await page.go_back()
                            await page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Erro ao clicar no item de menu: {e}")
                        continue
            except Exception as e:
                print(f"Erro ao navegar pelo menu: {e}")
            
            # 5. Navegar por links da página
            try:
                links = await page.query_selector_all("a[href]")
                for i, link in enumerate(links[:10]):  # Limitar a 10 links
                    try:
                        href = await link.get_attribute("href")
                        text = await link.text_content()
                        if href and not href.startswith("#") and not href.startswith("javascript:"):
                            print(f"Acessando link: {text.strip() if text else href}")
                            # Abrir em nova aba para não perder a página atual
                            new_page = await browser.new_page()
                            await new_page.goto(APP_URL + href if href.startswith("/") else href)
                            await new_page.wait_for_timeout(2000)
                            await take_screenshot(new_page, f"06_link_{i+1}_{text.strip() if text else 'unnamed'}")
                            await new_page.close()
                    except Exception as e:
                        print(f"Erro ao acessar link: {e}")
                        continue
            except Exception as e:
                print(f"Erro ao coletar links: {e}")
                
        except Exception as e:
            print(f"Erro durante a navegação: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    print("Iniciando a navegação automatizada...")
    asyncio.run(navigate_app())
    print("Navegação concluída!")