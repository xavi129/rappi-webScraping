from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
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

# Obtener todas las imágenes de los productos
images = driver.find_elements(By.XPATH, '//img[@data-testid="image"]')

# Crear la carpeta 'imagenes' si no existe
if not os.path.exists('imagenes'):
    os.makedirs('imagenes')

# Descargar cada imagen
for idx, image in enumerate(images):
    image_url = image.get_attribute('src')
    print(f"URL de la imagen encontrada: {image_url}")
    
    # Filtrar URLs en formato data:image
    if image_url.startswith("data:image"):
        print(f"Saltando imagen en formato base64: {image_url}")
        continue
    
    try:
        image_data = requests.get(image_url).content
        with open(f'imagenes/imagen_{idx}.jpg', 'wb') as handler:
            handler.write(image_data)
        print(f"Imagen descargada y guardada como: imagenes/imagen_{idx}.jpg")
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")

print("Descarga de imágenes completada.")