from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import requests
import os

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs

chrome_options.set_capability('goog:loggingPrefs', capabilities["goog:loggingPrefs"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.rappi.com.mx/tiendas/1923249724-farmacias-similares/alivio-del-dolor/multi-sintoma")
sleep(3)
driver.execute_script("window.scrollTo(0, 1000)") 
sleep(3)

restaurants = ["Farmacia similares"]
links = ['https://www.rappi.com.mx/tiendas/1923249724-farmacias-similares/alivio-del-dolor/multi-sintoma']

name = []
description = []
price = []
real_price = []
discount = []
price_per_unit = []
image_urls = []

restaurant= []
for j in range(len(restaurants)):
    driver.get(links[j])
    sleep(7)
    products = driver.find_elements(By.XPATH, '//div[@data-qa="product-information"]')
    
    for product in products:
        restaurant.append(restaurants[j])
        
        product_name = product.find_element(By.XPATH, './/h3[@data-qa="product-name"]').text
        product_price = product.find_element(By.XPATH, './/span[@data-qa="product-price"]').text
        product_real_price = product.find_element(By.XPATH, './/span[@data-qa="product-real-price"]').text
        
        try:
            product_discount = product.find_element(By.XPATH, './/span[@data-qa="product-discount"]').text
        except NoSuchElementException:
            product_discount = "No discount"
        
        try:
            product_price_per_unit = product.find_element(By.XPATH, './/span[@data-qa="product-pum"]').text
        except NoSuchElementException:
            product_price_per_unit = "No price per unit"
        
        try:
            product_description = product.find_element(By.XPATH, './/span[@data-qa="product-description"]').text
        except NoSuchElementException:
            product_description = "No description"
        
        try:
            product_image_url = product.find_element(By.XPATH, './/img[@data-testid="image"]').get_attribute('src')
        except NoSuchElementException:
            product_image_url = "No image"
        
        name.append(product_name)
        price.append(product_price)
        real_price.append(product_real_price)
        discount.append(product_discount)
        price_per_unit.append(product_price_per_unit)
        description.append(product_description)
        image_urls.append(product_image_url)
        
        # Descargar la imagen
        if product_image_url != "No image":
            image_data = requests.get(product_image_url).content
            # Crear la carpeta 'images' si no existe
            if not os.path.exists('images'):
                os.makedirs('images')
            with open(f'images/{product_name}.jpg', 'wb') as handler:
                handler.write(image_data)
        
    print(name, description, price, real_price, discount, price_per_unit, image_urls)
    print(len(name), len(description), len(price), len(real_price), len(discount), len(price_per_unit), len(image_urls))

df = pd.DataFrame(list(zip(restaurant, name, description, price, real_price, discount, price_per_unit, image_urls)), 
                  columns = ['Restaurante', 'Nombre', 'Descripción', 'Precio', 'Precio Real', 'Descuento', 'Precio por Unidad', 'URL de Imagen'])
print(df)

# Guardar el DataFrame en un archivo Excel
df.to_excel('productos_rappi.xlsx', index=False)

print("acabó")