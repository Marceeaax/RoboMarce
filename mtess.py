from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.mtess.gov.py/busca-empleo/vidriera-de-empleo")

# scrape all tr elements
tr_elements = driver.find_elements(By.XPATH,"//tr")

# declare td elements list
td_elements = []
i = 0

# iterate over tr elements list
for x in tr_elements:
    td_elements.append(x.find_elements(By.XPATH,"td"))
    if(i > 0):
        print(td_elements[i][1].text)
        
    i += 1

# regular expression that matches the text

