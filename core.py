import httpx
from bs4 import BeautifulSoup


res = httpx.get('https://hqerotico.com/')
soup = BeautifulSoup(res.text, 'html5lib')
links = soup.select('li > div.thumb-conteudo a')
for link in links:
    res = httpx.get(link.get('href'))
    soup = BeautifulSoup(res.text, 'html5lib')
    imgs = soup.select('li > a > img')
    for img in imgs:
        print(img.get('src'))



