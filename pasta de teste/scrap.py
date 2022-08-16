import requests
import httpx
from bs4 import BeautifulSoup as Bs


url = 'https://megahq.info/uma-mae-legal-4-interracial/'
response = requests.get(url)
soup = Bs(response.content, 'html5lib')
imgs = soup.select('p > noscript > img')
for img in imgs:
    # print(img.get('src'))
    ...
# body > main > div.row > div > div.posts > article > div.thumb > a

response = requests.get('https://superquadrinhosporno.com/page/2/')
soup = Bs(response.content, 'html5lib')
links = soup.select('ul > li > article > figure > a')
for link in links:
    if 'https://superquadrinhosporno.com/' in link.get('href'):
        print(link.get('href'))
        response = requests.get(link.get('href'))
        soup = Bs(response.content, 'html5lib')
        imgs = soup.select('span > p > img')
        for img in imgs:
            print(img.get('src'))
