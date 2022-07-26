import httpx
from bs4 import BeautifulSoup
from pdf_pil import Pdf
from urllib.parse import urlparse
import json
import os
import re


def tratar_texto(txt: str) -> str:
    ignore = "!@#$?:;'"
    for char in ignore:
        txt = txt.replace(char, "")
    return txt.strip().rstrip()


def main(url, sel1, sel_img):
    base = urlparse(url)
    with httpx.Client() as client:
        response = client.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        links = soup.select(sel1)
        for link in links:
            photos = []
            if base.netloc in link.get('href'):
                res = client.get(link.get('href'))
                sp = BeautifulSoup(res.text, 'html5lib')
                fotos = sp.select(sel_img)
                texto = sp.select_one('h1').text
                txt = tratar_texto(texto)
                print(txt)
                if len(fotos) >= 4:
                    os.makedirs(f'{base.netloc}/{txt}', exist_ok=True)
                    for foto in fotos:
                        if foto.get('src'):
                            comic = foto.get('src')
                        elif foto.get('href'):
                            comic = foto.get('href')
                        else:
                            comic = foto.get('data-src')
                        # print(comic)
                        photos.append(os.path.basename(comic))
                        r = client.get(comic).content
                        with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                            ft.write(r)
                Pdf(f'{base.netloc}/{txt}', txt, photos)
            else:
                ...


def procurando_next(link):
    def not_lacie(href):
        return href and re.compile("page").search(href)
    with httpx.Client() as client:
        response = client.get(link)
        soup = BeautifulSoup(response.text, 'html5lib')
        texto = soup.find_all(href=not_lacie)
        return texto[-1].get('href')


def golran(n):
    url_ = ''
    for p in range(1, n+1):
        if p == 1:
            url = 'https://www.quadrinhoseroticos.blog/'
            url_ = url
        else:
            page = procurando_next(url_)
            url_ = page
        print(url_)
        sel_li = 'div.cn-list > article > div.border > figure a'
        sel_im = 'dl dt.gallery-icon > img'
        main(url_, sel_li, sel_im)


# golran(4)
# url_ = 'https://www.quadrinhoseroticos.blog/page/2/'       # 'https://maniacosporcomics.com/'
# sel_li = 'div.cn-list > article > div.border > figure a'   # 'ul.videos > li  div.thumb-conteudo > a'
# sel_im = 'dl dt.gallery-icon > img'                        # 'figure > a > img'
# main(url_, sel_li, sel_im)
url_ = 'https://maniacosporcomics.com/'
sel_li = 'ul.videos > li  div.thumb-conteudo > a'
sel_im = 'figure > a'
main(url_, sel_li, sel_im)


