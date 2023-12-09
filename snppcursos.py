from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sqlite3

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

import sqlite3

def create_database():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            familia TEXT,
            unidad_operativa TEXT,
            areas TEXT,
            id_planificacion TEXT,
            especialidad TEXT,
            modalidad TEXT,
            edad_requerida TEXT,
            cantidad_maxima_alumnos TEXT,
            cantidad_alumnos TEXT,
            carga_horaria TEXT,
            distrito TEXT,
            ciudad TEXT,
            barrio TEXT,
            dias_semanas TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT
        )
    ''')
    conn.commit()
    conn.close()

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

        time.sleep(1)

        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, SUBMIT_LOGIN_ID)))
        submit_button.click()
        print("Login successful")
    except TimeoutException:
        print("Timeout occurred during login.")
    except NoSuchElementException:
        print("Login element not found.")

def procesar_cursos(driver, categoria):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    grid_rows = driver.find_elements(By.CSS_SELECTOR, "tr.bs-gridrow")
    
    for row in grid_rows:
        course_data = {}
        for data_field in CAMPOS_DE_CURSOS:
            css_selector = f"td[data-field='{data_field}']"
            try:
                element = row.find_element(By.CSS_SELECTOR, css_selector)
                course_data[data_field] = element.text
            except NoSuchElementException:
                course_data[data_field] = None

        # Check if the course already exists
        cursor.execute('SELECT * FROM courses WHERE id_planificacion = ?', (course_data['id_planificacion'],))
        if cursor.fetchone() is None:
            # Insert new course
            columns = ', '.join(course_data.keys())
            placeholders = ':' + ', :'.join(course_data.keys())
            query = f'INSERT INTO courses ({columns}) VALUES ({placeholders})'
            cursor.execute(query, course_data)
    
    conn.commit()
    conn.close()


def navegar_por_modalidad(driver):
    try:
        item_link_9 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "itemlink9")))
        print("se detecto item 9")
        item_link_9.click()

        time.sleep(1)          

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

                if page_urls:
                    print("Hay mas de una pagina")
                    # imprimir cantidad de paginas
                    print(f"Paginas encontradas: {len(page_urls)}")
                    for page in page_urls:
                        driver.get(page)
                        procesar_cursos(driver, categoria)
                else:
                    print("Solo hay una sola pagina")
                    procesar_cursos(driver, categoria)

            except NoSuchElementException:
                # Pagination element not found
                print("Solo hay una pagina")
                procesar_cursos(driver, categoria)

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
    create_database()
    driver = initialize_driver()
    login(driver)
    navegar_por_modalidad(driver)
    driver.quit()

if __name__ == "__main__":
    main()