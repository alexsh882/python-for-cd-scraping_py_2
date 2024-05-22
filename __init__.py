import requests
from bs4 import BeautifulSoup
import re
import os

# url elegida
url = 'https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories'

# request
response = requests.get(url)


# se crea el directorio imgs si no existe
os.makedirs('./imgs', exist_ok=True)
    

# obtener texto plano y dárselo a BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# búsqueda por algo distinto, en este caso es la clase.
results = soup.find_all('img', class_="dynamic-carousel__img")

# función que descarga las imágenes
def downloadImages(url):
    if re.search(r'jpg|jpeg|png|webp', url) is None:
        return
            
    try:
        response = requests.get(url)        
        
        # si el status code no es 200, se lanza una excepción
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")
        
        # si el tipo de contenido no es una imagen, se lanza una excepción
        if 'image' not in response.headers['Content-Type']:
            raise Exception(f"Error: no se descargó por que la url no corresponde a una imagen, es de tipo {response.headers['Content-Type']}")
        
        save_images_from_bytes(response.content)
        
    except Exception as e:
        print(e)

def save_images_from_bytes(img : bytes):  
    print(f"Se descargó una imagen de {len(img)} bytes")
    with open(f'./imgs/{len(img)}.jpg', 'wb') as file:
        file.write(img)

# se muestran por consola las url de las imágenes
for img in results:    
    # se descargan las imágenes
    downloadImages(img['data-src']);
