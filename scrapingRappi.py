from os import link
from time import sleep
import json
from turtle import distance
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd
import pygsheets
from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')         
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
driver = webdriver.Chrome(desired_capabilities=capabilities, service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.rappi.com.co/restaurantes")
sleep(3)
driver.execute_script("window.scrollTo(0, 1000)") 
sleep(3)
use_my_location_button = driver.find_element(By.XPATH, '//div[@class="sc-giIncl gHUUHu"]')
use_my_location_button.click()
sleep(5)


n_scrolls = 1#14 #16
for _ in range(n_scrolls): # Scrolls the page 'n_scrolls' times, to get more restaurants
    driver.execute_script("window.scrollTo(0, document);")
    sleep(3)
    load_more_button = driver.find_element(By.XPATH,'//button[@class="sc-hmzhuo fzSijE primary wide"]')
    load_more_button.click()
    sleep(3)


resturants = ["Masa","Maison Kayser","Starbucks","Avocalia","Crepes & Waffles","Azahar","Abasto","Brunch & Munch","Franco","WOK","Vin y Greta","Lina's Sándwiches","Sanamente Gourmet","Bagatelle"]
links = ['https://www.rappi.com.co/restaurantes/900025915-masa','https://www.rappi.com.co/restaurantes/900018774-maison-kayser','https://www.rappi.com.co/restaurantes/900030173-starbucks-cafe','https://www.rappi.com.co/restaurantes/900042109-avocalia','https://www.rappi.com.co/restaurantes/900055004-crepes-waffles','https://www.rappi.com.co/restaurantes/900068382-azahar-93','https://www.rappi.com.co/restaurantes/900011128-abasto','https://www.rappi.com.co/restaurantes/900042119-brunch-%26-munch-93','https://www.rappi.com.co/restaurantes/900028518-franco','https://www.rappi.com.co/restaurantes/900086567-wok','https://www.rappi.com.co/restaurantes/900244454-vin-y-gretta',"https://www.rappi.com.co/restaurantes/10000603-lina's-sandwiches-andino",'https://www.rappi.com.co/restaurantes/900026872?csr=true','https://www.rappi.com.co/restaurantes/900022963-bagatelle-parque-93']


name = []
description = []
price = []

restaurant= []
for j in range(len(resturants)):
    driver.get(links[j])
    sleep(7)
    restInfo = driver.find_elements(By.XPATH, '//div[@class="styles__ProductInfoContainer-sc-jkotxm-2 eCNeUM"]')
    platos = [info.text for info in restInfo]
    print(platos)
    for i in platos: 
        print(i)
        restaurant.append(resturants[j])
        
        if i =="":
            continue
        else:
            if len(i.split('\n')) <=2:
                name.append(i.split('\n')[0])
                description.append("No tiene descripción")
                price.append(i.split('\n')[1][:-3].replace("$ ","").replace(".",","))
            else:
                name.append(i.split('\n')[0]) 
                description.append(i.split('\n')[1])
                price.append(i.split('\n')[2][:-3].replace("$ ","").replace(".",","))
        
         
    print(name,description,price)
    print(len(name), len(description),len(price))

df = pd.DataFrame(list(zip(restaurant,name,description,price)), columns = ['Restaurante','Plato','Descripción','Precio'])
print(df)

gc = pygsheets.authorize(service_file='/Users/mariopesca/Documentos/scripts/webScraping/credentials.json')

sh = gc.open('Scraping')

wks = sh[4]

wks.set_dataframe(df,(1,1))

print("acabó")
