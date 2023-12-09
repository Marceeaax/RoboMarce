from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Constants
LOGIN_URL = "https://identidad.mtess.gov.py/alumno/login.php"
DOCUMENTO_IDENTIDAD = 4669759
CONTRASENA = "6KKiXTMsnX8w3jstl$$y8f%VU"
ITEM_LINK_9_ID = "itemlink9"
USERNAME_ID = "username"
PASSWORD_ID = "password"
SUBMIT_LOGIN_ID = "submitLogin1"

CATEGORIAS = {
    "a Distancia": "itemlink10",
    "Hibrida": "itemlink11",
    "Programa Emprendedurismo": "itemlink12",
    "Generacion Digital": "itemlink13",
    "Fonoclases": "itemlink14",
    "TV Clases": "itemlink15",
    "Presenciales": "itemlink16",
    "Curso Probatorio de Ingreso": "itemlink17",
    "Cursos a distancia SINAFOCAL": "itemlink18",
    "Cursos presenciales SINAFOCAL": "itemlink19",
    "Cursos CEE": "itemlink20",
    "Cursos SPE": "itemlink21",
    "Cursos MITIC": "itemlink22"
}

CAMPOS_DE_CURSOS = [
    "familia",
    "unidad_operativa",
    "areas",
    "id_planificacion",
    "especialidad",
    "modalidad",
    "edad_requerida",
    "cantidad_maxima_alumnos",
    "cantidad_alumnos",
    "carga_horaria",
    "distrito",
    "ciudad",
    "barrio",
    "dias_semanas",
    "fecha_inicio",
    "fecha_fin"
]
def initialize_driver():
    # Initialize the Chrome webdriver and return it as a variable
    # Notice that, you need to download the chromedriver.exe file and put it in your PATH
    driver = webdriver.Chrome()
    driver.get("https://identidad.mtess.gov.py/alumno/login.php")
    return driver

def login(driver):
    try:
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, USERNAME_ID)))
        username.send_keys(DOCUMENTO_IDENTIDAD)
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, PASSWORD_ID)))
        password.send_keys(CONTRASENA)
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, SUBMIT_LOGIN_ID)))
        submit_button.click()
        print("Login successful")
    except TimeoutException:
        print("Timeout occurred during login.")
    except NoSuchElementException:
        print("Login element not found.")

def navigate_and_extract_courses(driver):
    try:
        item_link_9 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "itemlink9")))
        print("se detecto item 9")
        item_link_9.click()          

        for categoria, item_link_id in CATEGORIAS.items():
            item_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, item_link_id)))
            print(f"se detecto {categoria}")
            item_link.click()
            print(f"entro a {categoria} cursos")
            
            time.sleep(2)  # Wait for the page to load (adjust the sleep time as needed)

            try:
                pagination = driver.find_element(By.CSS_SELECTOR, "ul.pagination[data-function='pagination1']")
                # Find all page links within the pagination section
                page_links = pagination.find_elements(By.TAG_NAME, "a")
                # Create a list to store the page URLs
                page_urls = [link.get_attribute("href") for link in page_links]

                if pagination:
                    print("se detecto paginacion")
                else:
                    print("no se detecto paginacion")

            except NoSuchElementException:
                # Pagination element not found
                print("No pagination element found")
                page_urls = []  # Set an empty list for page URLs

            grid_rows = driver.find_elements(By.CSS_SELECTOR, "tr.bs-gridrow")
            print(f"{categoria} Cursos encontrados: {len(grid_rows)}")
            
            for row in grid_rows:
                for data_field in CAMPOS_DE_CURSOS:
                    # Construct the CSS selector to find the <td> element with the data-field attribute
                    css_selector = f"td[data-field='{data_field}']"
                    
                    try:
                        # Find the element using the CSS selector within the current row
                        element = row.find_element(By.CSS_SELECTOR, css_selector)
                        
                        # Extract the text content (outer_text) of the element
                        text_content = element.text
                        
                        # Print the text content
                        print(f"{data_field}: {text_content}")

                    except NoSuchElementException:
                        # Element not found, continue with the next iteration
                        continue

            print("Cursos extraidos")
            item_link_9 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "itemlink9")))
            time.sleep(1)
            item_link_9.click()
            time.sleep(1)
            
    except TimeoutException:
        print("Timeout occurred while waiting for element.")
    except NoSuchElementException:
        print("Element not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    driver = initialize_driver()
    login(driver)
    navigate_and_extract_courses(driver)
    driver.quit()

if __name__ == "__main__":
    main()