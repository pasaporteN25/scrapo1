from bs4 import BeautifulSoup
import requests

def traerCrypto(url, nombre, mostrar):
    pedido = requests.get(url)
    soup = BeautifulSoup(pedido.content, 'html.parser')

    #implementar clausula boolean de visualizacion para usar en la calculadora
    if not mostrar:
        vercot = input("Ver cotizacion en 1.USD o 2.BTC 3.Ambos?")
        if vercot == '1':
            cotizaenusd(soup, nombre, False)
        elif vercot == '2':
            cotizaenbtc(soup, nombre)
        elif vercot == '3':
            cotizaenusd(soup, nombre, False)
            cotizaenbtc(soup, nombre)
        else:
            print("Entonces que queres?")

        print("Desea ver el volumen operado?", end='\n\n')
        vol = input()
        if vol == 'y' or vol == 'Y' or vol == '':
            calcularVolumenes(soup, nombre)
        else:
            print("Buenas Noches!")

    else:
        return cotizaenusd(soup, nombre, mostrar)


def calcularVolumenes(soup, nombre):

    volumen = soup.find_all('td', {'class': 'coin_price_3'})
    print("Volumen ultimas 24 hs", end='\n')
    print('en USD: {}'.format(volumen[0].text))
    print('en BTC: {}'.format(volumen[1].text))
    if nombre != 'Bitcoin':
        print('en {}: {}'.format(nombre, volumen[2].text), end='\n\n')
    print("Capitalizacion de Mercado: ")
    if nombre != 'Bitcoin':
        print('en USD: {}'.format(volumen[3].text))
        print('en BTC: {}'.format(volumen[4].text))
        print("{} en circulacion: {}".format(nombre, volumen[6].text))

    else:
        print("en USD: {}".format(volumen[2].text))
        print("{} en circulacion: {}".format(nombre, volumen[3].text))


def cotizaenusd(soup, nombre, mostrar):
    precio = soup.find_all('td', {'class': 'wbreak_word align-middle coin_price'})
    variac = soup.find_all('td', {'class': 'fz16'})

    if mostrar:
        return precio[0].text
    else:
        print("Cotizacion actual en USD", end='\n')
        print('Precio actual de {}'.format(nombre), precio[0].text)

        varia = input("¿Desea ver las variaciones? [Y/n]")
        if varia == 'Y' or varia == 'y' or varia == '':
            variacionesusd(variac)


def variacionesusd(variac):
    print('Variacion Precio 24hs:', variac[0].text.strip('\n'))
    print('Variacion % ultima hora:', variac[1].text.strip('\n'))
    print('Variacion % ultimo dia:', variac[2].text.strip('\n'))
    print('Variacion % ultima semana:', variac[3].text.strip('\n'))


def cotizaenbtc(soup, nombre):
    precio = soup.find_all('td', {'class': 'wbreak_word align-middle coin_price'})
    variac = soup.find_all('td', {'class': 'fz16'})

    if nombre != ' btc' or nombre != 'Bitcoin':
        print("{} to BTC".format(nombre), end='\n')
        print('Precio actual de {}'.format(nombre), precio[1].text)
        varia = input("¿Desea ver las variaciones? [Y/n]")
        if varia == 'Y' or varia == 'y' or varia == '':
            variacionesbtc(variac)
    else:
        print("BTC vs BTC 404")


def variacionesbtc(variac):
    print('Variacion Precio 24hs:', variac[4].text)
    print('Variacion % ultima hora:', variac[5].text.strip('\n'))
    print('Variacion % ultimo dia:', variac[6].text.strip('\n'))
    print('Variacion % ultima semana:', variac[7].text.strip('\n'))


def traerCoin(nombre):
    url = 'https://awebanalysis.com/es/coin-details/{}/'.format(nombre)
    return float(''.join(filter(str.isdigit, traerCrypto(url, nombre, True).rstrip(''))))


def cryptotoars(nombre, dolar):
    crypto = traerCoin(nombre)
    return (crypto/100)*dolar


def getMonedas():
    url = 'https://awebanalysis.com/es/crypto-currencies-monitor-price/'
    monedas = requests.get(url)
    soup = BeautifulSoup(monedas.content, 'html.parser')
    datos = soup.find_all('a', {'class': 'crypto_name crypto_name_break'})
    return datos


def elegirMoneda():
    datos = getMonedas()
    nombres = []
    urls = []
    for item in datos:
        nombres.append(item.text.strip('\n '))
        urls.append(item['href'])

    for x in range(0, 50):
        print(x+1, nombres[x])

    coin = int(input('Elija el numero de su moneda: '))
    url = urls[coin-1]

    traerCrypto(url, nombres[coin-1], False)


def dolartoars():
    #en dolar hoy
    print("Opciones")
    print("1.Dolar Blue")
    print("2.Dolar oficial")
    print("3.Dolar bolsa")
    print("4.Dolar contado con Liquidacion")
    print("5.Dolar Solidario/Turista")
    print("6.Todos")
    opcion = int(input("Elija opcion a visualizar: "))

    #reemplazar por match al pasar a python 3.10
    if opcion == 1:
        print(dolarblue(True))
    elif opcion == 2:
        print(dolaroficial())
    elif opcion == 3:
        print(dolarbolsa())
    elif opcion == 4:
        print(dolarliq())
    elif opcion == 5:
        print(dolarsol())
    else:
        print(getallusd())


def getusdinfo(url):
    pedido = requests.get(url)
    soup = BeautifulSoup(pedido.content, 'html.parser')
    precios = soup.find_all('div', {'class': 'value'})
    compra = precios[0].text
    venta = precios[1].text
    return compra, venta


def dolarblue(mostrar):
    url = 'https://www.dolarhoy.com/cotizaciondolarblue'
    precio = getusdinfo(url)
    if mostrar:
        print("Precio Dolar Blue ")
        print('Compra: ', precio[0], '| Venta: ', precio[1])
    else:
        return precio[1]


def dolaroficial():
    url = 'https://www.dolarhoy.com/cotizaciondolaroficial'
    precio = getusdinfo(url)
    print("Precio Dolar Oficial ")
    print('Compra: ', precio[0], '| Venta: ', precio[1])


def dolarsol():
    url = 'https://www.dolarhoy.com/cotizaciondolarbolsa'
    precio = getusdinfo(url)
    print("Precio Dolar Solidario ")
    print('Venta: ', precio[1])


def dolarbolsa():
    url = 'https://www.dolarhoy.com/cotizaciondolarcontadoconliqui'
    precio = getusdinfo(url)
    print("Precio Dolar Blue ")
    print('Compra: ', precio[0], '| Venta: ', precio[1])


def dolarliq():
    url = 'https://www.dolarhoy.com/cotizaciondolarturista'
    precio = getusdinfo(url)
    print("Precio Dolar Blue ")
    print('Compra: ', precio[0], '| Venta: ', precio[1])


def getallusd():
    dolarblue(True)
    dolaroficial()
    dolarsol()
    dolarbolsa()
    dolarliq()


def calculadora():
    dolar = float(''.join(filter(str.isdigit, dolarblue(False).rstrip('0'))))
    print("1.Valor btc en AR$")
    print("2.Valor eth en AR$")
    nombre = ''
    #Esta parte se puede cambiar y mejorar
    calculo = input("Elija calculo: ")
    if calculo == '1':
        nombre = 'bitcoin'
    elif calculo == '2':
        nombre = 'ethereum'
    print('1 {} equivale a $', cryptotoars(nombre, dolar), sep='')

    print()


#elegirMoneda()

#calculadora()

