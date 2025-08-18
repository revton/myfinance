from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome WebDriver
# Make sure to replace 'path/to/chromedriver.exe' with the actual path to your chromedriver
# If chromedriver is in your system's PATH, you can remove the 'service' argument.
# service = Service(executable_path='path/to/chromedriver.exe')
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome()

# base_url = "https://myfinance-three.vercel.app/"
base_url = "http://localhost:5173/"

try:
    # --- Screenshot 1: Initial Page ---
    driver.get(base_url)
    driver.maximize_window()
    time.sleep(2) # Give some time for the page to load
    # driver.save_screenshot("screenshot_01_initial_page.png")
    # print("Screenshot 01: Initial page saved.")

    # --- Screenshot 2: Registration Form (assuming there's a register link/button) ---
    # You might need to adjust the selector for the register link/button
    # try:
        
    #     register_link = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/auth/register']")) # Or By.ID, By.CLASS_NAME, etc.
    #     )
    #     register_link.click()
    #     time.sleep(2)
    #     driver.save_screenshot("screenshot_02_registration_form.png")
    #     print("Screenshot 02: Registration form saved.")
    # except Exception as e:
    #     print(f"Could not find or click register link: {e}")
    #     print("Skipping registration form screenshot.")

    # --- Screenshot 3: Login Form (assuming there's a login link/button) ---
    # driver.get(base_url) # Go back to base URL if needed
    # try:
    #     login_link = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.LINK_TEXT, "Login")) # Or By.ID, By.CLASS_NAME, etc.
    #     )
    #     login_link.click()
    #     time.sleep(2)
    #     driver.save_screenshot("screenshot_03_login_form.png")
    #     print("Screenshot 03: Login form saved.")
    # except Exception as e:
    #     print(f"Could not find or click login link: {e}")
    #     print("Skipping login form screenshot.")

    # # --- Screenshot 4: Forgot Password (assuming there's a forgot password link) ---
    # # This assumes you are on the login page. Adjust if the link is elsewhere.
    # try:
    #     forgot_password_link = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.LINK_TEXT, "Esqueceu sua senha?")) # Or By.PARTIAL_LINK_TEXT
    #     )
    #     forgot_password_link.click()
    #     time.sleep(2)
    #     driver.save_screenshot("screenshot_04_forgot_password.png")
    #     print("Screenshot 04: Forgot password page saved.")
    # except Exception as e:
    #     print(f"Could not find or click forgot password link: {e}")
    #     print("Skipping forgot password screenshot.")

    # --- Screenshot 5: Main Application Screen (after hypothetical login) ---
    # For this, you would need to actually log in. This is a placeholder.
    # Example: driver.get("https://myfinance-three.vercel.app/dashboard")
    # For now, I'll just take a screenshot of the base URL again as a placeholder for "main screen"
    driver.get(base_url)
    time.sleep(2)
    # Preencher os campos de login e senha
    username_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys("revtonbr@gmail.com")  # Substitua pelo seu nome de usuário
    password_input.send_keys("4b6e3gmR$")  # Substitua pela sua senha
    # Submeter o formulário de login
    password_input.submit()
    # Esperar até que a página principal seja carregada
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "main-dashboard"))  # Ajuste o seletor conforme necessário
    # )   
    
    time.sleep(5)
    driver.save_screenshot("screenshot_05_main_application_screen.png")
    print("Screenshot 05: Main application screen saved.")


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Browser closed.")
