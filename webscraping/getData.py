# from models import *
import cloudscraper
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# lineas para evitar error SSL
import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.verdeesvida.es"


def getMarkupFromURL(url):
    try:
        return BeautifulSoup(urlopen(url), "lxml")
    except HTTPError as e:
        print("Error al obtener los datos de la url: " + url)
        print(e.code)
    except URLError as e:
        print("Error al obtener los datos de la url: " + url)
        print(e.reason)
    else:
        print("Datos obtenidos correctamente de la url: " + url)


def getPlantCategoryArray(soup):
    plantCategoryArray = []
    categoriesListItems = soup.find(
        'div', {'class': 'fichas-body'}).find('ul', {'class': 'navbar-nav'})

    for category in categoriesListItems.find_all('a'):
        plantCategoryArray.append(
            {'categoryName': category.text, 'categoryHref': category['href']})

    return plantCategoryArray


def getPlantItemsFromPage(bs):
    fichasItems = bs.findAll('div', {'class': 'fichas-item'})
    itemsArray = []

    for item in fichasItems:
        itemsArray.append(
            {'plantCategory': item.find('a', {'class': 'catblack'}).text,
             'plantHref': item.find('a', {'class': 'title'})['href'],
             'plantCientificName': item.find('span', {'class': 'science'}).text,
             'plantImageUrl': item.find('img')['src']})
    return itemsArray


def getAllPlantsFromPlantCategory(url):
    bs = getMarkupFromURL(url+'/0')
    plantsOnPageArray = []

    numPages = bs.find('div', {'class': 'fichas-body'}
                       ).find('div', {'class': 'col-md-12 text-center'}
                              ).findAll('a')[-1]['href'].split('/')[-1]

    plantsOnPageArray.append(getPlantItemsFromPage(bs))

    for i in range(1, int(numPages)+1):
        bs = getMarkupFromURL(url+'/'+str(i))
        plantsOnPageArray.append(getPlantItemsFromPage(bs))

    return plantsOnPageArray


def getAllPlants(plantCategoryArray):
    allPlants = {}
    for plantCategory in plantCategoryArray:
        allPlants[plantCategory['categoryName']] = getAllPlantsFromPlantCategory(
            url+plantCategory['categoryHref'])

    return allPlants


soup = getMarkupFromURL(url+'/fichas_de_plantas')
plantCategoryArray = getPlantCategoryArray(soup)

allPlantsArray = getAllPlants(plantCategoryArray)
