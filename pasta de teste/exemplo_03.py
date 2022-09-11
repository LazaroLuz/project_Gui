import os
import re

import httpx
from bs4 import BeautifulSoup

imagens: list = []


def imgs(url):
    # url = 'https://www.muitohentai.com/manga/hypnosis/capitulo-1/'  # 'https://www.muitohentai.com/manga/backward-alert/capitulo-1/'
    response = httpx.get(url)
    soup = BeautifulSoup(response.text)
    imagem_1 = soup.select_one('#gallery_imgs_manga > img:nth-child(1)')
    imagens.append(imagem_1.get('src'))
    lista = soup.select_one('#contenedor > div > div > div:nth-child(4) > script:nth-child(9)')
    resultado = str(lista)
    reslt = resultado.split('>')[1].split('<')[0]
    # print(reslt[15:][:-133])
    listas = reslt[15:][:-133].split('"')
    for i in range(len(listas)):
        if 'imgs' in listas[i]:
            imagens.append(listas[i])
            # print(os.path.basename(listas[i].split('?')[0]))
        # if i % 2 == 0:
        #     pass
        else:
            pass
            # if 'imgs' in listas[i]:
            #     print(os.path.basename(listas[i].split('?')[0]))
            #     response = httpx.get(listas[i])
            #
            #     with open(os.path.join('past', os.path.basename(listas[i].split('?')[0])), 'wb') as arquivo:
            #         arquivo.write(response.content)
    print('#' * 100)


def action(url):
    #  div> div > div.caption > h3 > a
    # url = 'https://www.muitohentai.com/manhwa/hypnosis/'  # 'https://www.muitohentai.com/manga/backward-alert/capitulo-1/'
    response = httpx.get(url)
    soup = BeautifulSoup(response.text)
    lista = soup.select('div> div > div.caption > h3 > a')
    for l in lista:
        print(f"https://www.muitohentai.com{l.get('href')}/")


def links():
    # div.data > h3 > a
    url = 'https://www.muitohentai.com/mangas/'  # 'https://www.muitohentai.com/manga/backward-alert/capitulo-1/'
    response = httpx.get(url)
    soup = BeautifulSoup(response.text)
    lista = soup.select('div.data > h3 > a')
    pag = soup.select('#paginacao > div > a')
    for l in lista:
        action(l.get('href'))
    proximo = pag[-1].get('href')
    print('https://www.muitohentai.com'+proximo)




links()
# imgs('https://www.muitohentai.com/manga/the-hypnosis-app-was-fake/capitulo-1/')
# # https://www.muitohentai.com/manga/baka-to-boing/capitulo-1/
# for im in imagens:
#     res = httpx.get(im)
#     with open(os.path.join('past', os.path.basename(im.split('?')[0])), 'wb') as arquivo:
#         arquivo.write(res.content)
# imagens.clear()

