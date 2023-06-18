import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def main():
    """
    Esta función extrae información sobre laptops del sitio web de Mercado Libre y la almacena en un archivo CSV.
    La función no toma ningún parámetro ni tiene ningún tipo de retorno.

    La función hace lo siguiente:
    - Envía una solicitud GET a una URL.
    - Extrae los datos de la respuesta HTML utilizando BeautifulSoup.
    - Almacena los datos extraídos en una lista que contiene el nombre, el precio y las características de cada laptop.
    - Crea un DataFrame de pandas a partir de la lista y lo guarda en un archivo CSV.
    """

    url_inicial = "https://listado.mercadolibre.com.mx/laptop"
    response_inicial = requests.get(url_inicial)
    soup_inicial = BeautifulSoup(response_inicial.content, 'html.parser')

    seccion = soup_inicial.find('section', class_="ui-search-results ui-search-results--without-disclaimer shops__search-results")
    ol = seccion.find('ol')
    articulos = ol.find_all('li', class_="ui-search-layout__item shops__layout-item")

    laptops = []
    i:int = 1

    for articulo in articulos:
        # Imprime el número de la iteración que es el número de artículo visitado
        print(i)
        time.sleep(random.randint(10, 13))
        # print(str(articulo.find('a').attrs['href']))

        url = str(articulo.find('a').attrs['href'])

        response = requests.get(url)
        response = response.content

        soup = BeautifulSoup(response, 'html.parser')

        nombre = soup.find('h1', class_="ui-pdp-title").text
        precio = soup.find('span', class_="andes-money-amount__fractaion").text
        lista_caracteristicas = soup.find('section', class_="ui-vpp-highlighted-specs")
        try:
            lista_caracteristicas = lista_caracteristicas.find('ul', class_="ui-vpp-highlighted-specs__features-list")
            caracteristicas = lista_caracteristicas.find_all('li', class_="ui-vpp-highlighted-specs__features-list-item ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR")
            caracteristicas = [caracteristica.text for caracteristica in caracteristicas]
            laptops.append([nombre, precio, caracteristicas])
        except:
            pass

        i += 1

    # for laptop in laptops:
    #     print(laptop)

    df = pd.DataFrame(laptops, columns=['Nombre', 'Precio', 'Caracteristicas'])
    df.to_csv('laptops.csv')
    print("Proceso finalizado con éxito")


if __name__ == '__main__':
    main()
