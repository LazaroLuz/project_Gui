import requests
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
url = 'https://weather.com/pt-BR/clima/hoje/l/ff780ef2293ddcda4599f5c0da0c723e68fb845c931320b00d6ce63f3320193b'
session = requests.Session()
session.headers['User-Agent'] = USER_AGENT
html = session.get(url)
soup = BeautifulSoup(html.text, 'html5lib')
base = soup.find('div', attrs={'id': 'todayDetails'})
title = base.find('h2').text
temp = base.find('span', attrs={'data-testid': 'TemperatureValue'}).text
sen_ter = base.find('span', attrs={'data-testid': 'FeelsLikeLabel'}).text
nascer = base.find('div', attrs={'data-testid': 'SunriseValue'}).text
morrer = base.find('div', attrs={'data-testid': 'SunsetValue'}).text
# max_min = base.find('div', attrs={'data-testid': 'wxData'}).text
max_min = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(1)').text
vento = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(2)').text
umidade = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(3)').text
p_orv = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(4)').text
pressao = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(5)').text
uv = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(6)').text
visibilidade = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(7)').text
fase_lua = base.select_one('.WeatherDetailsListItem--WeatherDetailsListItem--1gmc0:nth-child(8)').text


print(title)
print(temp)
print(sen_ter)
print(nascer[8:])
print(morrer[6:])
print(max_min[22:])
print(vento[23:])
print(umidade[15:])
print(p_orv[25:])
print(pressao[25:])
print(uv[17:])
print(visibilidade[22:])
print(fase_lua[21:])
