# from models import *
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# lineas para evitar error SSL
import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url = "http://garden.org/plants"
# url = "https://www.jardineriaon.com/plantas-de-interior" // de reserva si garden.org no funciona


def getData(url):
    hdrs = {
        'Host': 'garden.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64 rv: 109.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'text/html, application/xhtml+xml, application/xml q = 0.9, image/avif, image/webp, */* q = 0.8',
        'Accept-Language': 'es-ES, es q = 0.8, en-US q = 0.5, en q = 0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://garden.org/plants/',
        'Cookie': '''cf_clearance = PS_Y4c9MFKVlskY6EyjoUk4Ethezc6u0oQ9YO0PKAxE-1684596223-0-160
        cusess = 8e6480d5e12d0a675ae56fa7608add5d
        sr = %2F
        _pk_id.1.94cf = 3a6c0b2e127904bf.1684596227.
        _pk_ses.1.94cf = 1
        __cf_bm = kjFeR6WlQwXxWkr3DHQshD_oQCzikQE2Bx86mmoYLcU-1684607657-0-Aecpx8XphjOQIVmV8flbd88VxZh0NcKZ50W /
        eSkhgxvv+A3YHF+SA6Rn8Xu+BOjE0yGeXc3oM4NJF1nlPjruiseabA5rUTGs6rXZihSWlSJx
        fs.bot.check = true
        euconsent-v2 = CPsEIcAPsEIcAAKAvAENDFCsAP_AAH_AAAwIJbtX_H__bW9r8f5_aft0eY1P9_j77uQzDhfNk-4F3L_W_JwX52E7NF36tq4KmR4Eu3LBIUNlHNHUTVmwaokVryHsak2cpTNKJ6BEkHMRO2dYGF5umxtjeQKY5_p_d3fx2D-t_dv-39z3z81Xn3dZf-_0-PCdU5_9Dfn9fRfb-9IL9_78v8v8_9_rk2_eX_3_79_7_H9-f_84JcAEmGrcQBdmUODNoGEUCIEYVhARQKACCgGFogIAHBwU7IwCfWESAFAKAIwIgQ4AoyIBAAAJAEhEAEgRYIAAABAIAAQAIBEIAGBgEFABYCAQAAgOgYohQACBIQJEREQpgQFQJBAS2VCCUF0hphAFWWAFAIjYKABEEgIrAAEBYOAYIkBKxYIEmINogAGAFAKJUK1FJ6aAhYzMAAAA.YAAAAAAAAAAA
        addtl_consent = 1~39.4.3.9.6.9.13.6.4.15.9.5.2.11.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.20.5.20.6.5.1.4.11.29.4.14.4.5.3.10.6.2.9.6.6.9.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.146.8.42.15.1.14.3.1.18.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.10.15.2.5.6.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.2.2.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.14.1.3.3.4.5.4.3.2.2.5.4.1.1.2.9.1.6.9.1.5.2.1.7.10.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.4.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.6.2.1.6.2.3.2.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.4.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1.4.6.1.1.6.1.1.2.6.3.1.2.201.300.100''',
        'Upgrade-Insecure-Requests': 1,
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }
    # request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    request = Request(url, headers=hdrs)
    try:
        return BeautifulSoup(urlopen(request), "lxml")
    except HTTPError as e:
        print("Error al obtener los datos de la url: " + url)
        print(e.code)
    except URLError as e:
        print("Error al obtener los datos de la url: " + url)
        print(e.reason)
    else:
        print("Datos obtenidos correctamente de la url: " + url)


def getPlantTypesArray(soup):
    plantTypesArray = []

    plantTypesTable = soup.find("table")
    print(plantTypesTable)
    plantTypesRows = plantTypesTable.find_all("a")

    for plantTypeRow in plantTypesRows:
        plantTypesArray.append({plantTypeRow.text: plantTypeRow["href"]})

    return plantTypesArray


soup = getData(url)
print(getPlantTypesArray(soup))
