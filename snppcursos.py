from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Add any Chrome options if needed

driver = webdriver.Chrome()
driver.get("https://identidad.mtess.gov.py/alumno/login.php")

documentoidentidad = 4669759
contrasena = "6KKiXTMsnX8w3jstl$$y8f%VU"

try:
    try:
        # Login process
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys(documentoidentidad)
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(contrasena)
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitLogin1")))
        submit_button.click()

        print("iniciar sesion")
        
        time.sleep(5)
        # Navigating through items
        item_link_9 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "itemlink9")))
        print("se detecto item 9")
        item_link_9.click()
        
        item_link_10 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "itemlink10")))
        print("se detecto item 10")
        item_link_10.click()
        
        print("entro a cursos")
        # iterate from gridRow4 to gridRow21 and extract the innerText string
        
        for i in range(4, 22):
            grid_row = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"gridRow{i}")))
            #print("logro detectar")
            print(grid_row.text)
            
    except TimeoutException:
        print("Timeout occurred while waiting for element.")
    except NoSuchElementException:
        print("Element not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
finally:
    driver.quit()
