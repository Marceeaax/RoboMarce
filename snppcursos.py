from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://identidad.mtess.gov.py/alumno/login.php")

documentoidentidad = 4669759
contrasena = "6KKiXTMsnX8w3jstl$$y8f%VU"

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    element.send_keys(documentoidentidad)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    element.send_keys(contrasena)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "submitLogin1"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "itemlink9"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "itemlink16"))
    )
    element.click()

    
finally:
    driver.quit()
