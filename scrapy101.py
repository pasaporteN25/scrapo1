from bs4 import BeautifulSoup
import requests
import urllib
import webbrowser

def traerCrypto(url,nombre):
    #Preguntar para ver en btc o usd
    pedido = requests.get(url)
    soup = BeautifulSoup(pedido.content,'html.parser')
    precio = soup.find_all('td', {'class':'wbreak_word align-middle coin_price'})
    variac = soup.find_all('td',{'class':'fz16'})
    volumen = soup.find_all('td',{'class':'coin_price_3'})

    vercot = input("Ver cotizacion en 1.USD o 2.BTC 3.Ambos?")
    if vercot == '1':
        cotizaenusd(precio,variac,nombre)
    elif vercot == '2': cotizaenbtc(precio,variac,nombre)
    elif vercot == '3':
        cotizaenusd(precio,variac,nombre)
        cotizaenbtc(precio, variac, nombre)
    else: print("Entonces que queres?")

    print("Desea ver el volumen operado?",end='\n\n')
    vol = input()
    if vol == 'y' or vol == 'Y' or vol == '':
        calcularVolumenes(volumen,nombre)
    else: print("Buenas Noches!")

def calcularVolumenes(volumen,nombre):

    print("Volumen ultimas 24 hs",end='\n')
    print('en USD: {}'.format(volumen[0].text))
    print('en BTC: {}'.format(volumen[1].text))
    if nombre != 'Bitcoin':
        print('en {}: {}'.format(nombre,volumen[2].text),end='\n\n')
    print("Capitalizacion de Mercado: ")
    if nombre != 'Bitcoin':
        print('en USD: {}'.format(volumen[3].text))
        print('en BTC: {}'.format(volumen[4].text))
        print("{} en circulacion: {}".format(nombre,volumen[6].text))

    else:
        print("en USD: {}".format(volumen[2].text))
        print("{} en circulacion: {}".format(nombre, volumen[3].text))

def cotizaenusd(precio,variac,nombre):
    print("Cotizacion actual en USD",end='\n')
    print('Precio actual de {}'.format(nombre), precio[0].text)

    varia = input("¿Desea ver las variaciones? [Y/n]")
    if varia == 'Y' or varia == 'y' or varia == '': variacionesusd(variac)

def variacionesusd(variac):
    print('Variacion Precio 24hs:', variac[0].text.strip('\n'))
    print('Variacion % ultima hora:', variac[1].text.strip('\n'))
    print('Variacion % ultimo dia:', variac[2].text.strip('\n'))
    print('Variacion % ultima semana:', variac[3].text.strip('\n'))

def cotizaenbtc(precio,variac,nombre):

    if nombre != ' btc' or nombre != 'Bitcoin':
        print("{} to BTC".format(nombre),end='\n')
        print('Precio actual de {}'.format(nombre), precio[1].text)
        varia = input("¿Desea ver las variaciones? [Y/n]")
        if varia == 'Y' or varia == 'y' or varia == '':
            variacionesbtc(variac)
    else: print("BTC vs BTC 404")

def variacionesbtc(variac):
    print('Variacion Precio 24hs:', variac[4].text)
    print('Variacion % ultima hora:', variac[5].text.strip('\n'))
    print('Variacion % ultimo dia:', variac[6].text.strip('\n'))
    print('Variacion % ultima semana:', variac[7].text.strip('\n'))


def traerBTC():
    nombre = 'btc'
    url = 'https://awebanalysis.com/es/coin-details/bitcoin/'
    traerCrypto(url,nombre)

def traerETH():
    nombre = 'ETH'
    url = 'https://awebanalysis.com/es/coin-details/ethereum/'
    traerCrypto(url,nombre)


def getMonedas():
    url = 'https://awebanalysis.com/es/crypto-currencies-monitor-price/'
    monedas = requests.get(url)
    soup = BeautifulSoup(monedas.content,'html.parser')
    datos = soup.find_all('a',{'class':'crypto_name crypto_name_break'})
    return datos

def elegirMoneda():
    datos = getMonedas()
    nombres=[]
    urls = []
    for item in datos:
        nombres.append(item.text.strip('\n '))
        urls.append(item['href'])

    for x in range(0,50):
        print(x+1,nombres[x])

    coin = int(input('Elija el numero de su moneda: '))
    url = urls[coin-1]

    traerCrypto(url,nombres[coin-1])


#traerBTC()
#traerETH()

elegirMoneda()