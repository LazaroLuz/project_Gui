import json
import os

import requests
import httpx
from bs4 import BeautifulSoup as Bs
from base_db import Allporn, Photo


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}


def prymary(url):
    response = httpx.get(url, headers=head, timeout=None)
    soup = Bs(response.content, 'html5lib')
    links = soup.select('div.col-6 > div > div > a')
    for link in links:
        yield link.get('href')


def secundary(link:str):

    res = httpx.get(link, headers=head, timeout=None)
    s = Bs(res.content, 'html5lib')
    s_links = s.select('li.wp-manga-chapter > a')
    for s_link in s_links:
        yield s_link.get('href')


lista_completa = []


def terceary(link:str):
    photos:list = []
    res = httpx.get(link, headers=head, timeout=None)
    s = Bs(res.content, 'html5lib')
    s_links = s.select('dl >dt.gallery-icon > img')  # 'div.reading-content > div > img'
    s_text = s.select_one('h1').text
    os.makedirs('past', exist_ok=True)
    try:
        # uncle_bob = Allporn.create(name=s_text)
        for s_link in s_links:
            ft = s_link.get('src').strip().rstrip() # data-src
            response = httpx.get(ft)
            with open(f'past/{os.path.basename(ft)}', 'wb') as f:
                f.write(response.content)
        # confirmacao = {'nome': s_text,
        #                'fotos': photos}
            # Photo.create(allporn=uncle_bob, fotos=ft)
    except:
        print('já existe')


terceary('https://www.quadrinhoseroticos.blog/sogro-comendo-nora-de-18-anos/')
# for i in range(1, 333):  # 333
#     if i == 1:
#         url = 'https://allporncomic.com/porncomic/'
#     else:
#         url = f'https://allporncomic.com/porncomic/page/{i}/'
#     pry = prymary(url)
#     print(url)
#     for p in pry:
#         sec = secundary(p)
#         for s in sec:
#             terceary(s)


