import PyPDF2
import httpx
from bs4 import BeautifulSoup
from pdf_pil import Pdf
from urllib.parse import urlparse
import os
import re


def tratar_texto(txt: str) -> str:
    ignore = "!@#$?:;'/"
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
                try:
                    file = open(f'{base.netloc}/{txt}.pdf', 'rb')
                    readpdf = PyPDF2.PdfFileReader(file)
                    totalpages = readpdf.numPages
                    if totalpages == len(fotos):
                        print('numero igual proximo!')
                        continue
                    else:
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
                except FileNotFoundError:
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
                continue


def maintest(url, sel1):
    base = urlparse(url)
    photos = []
    with httpx.Client() as client:
        response = client.get(url, timeout=None)
        soup = BeautifulSoup(response.text, 'html5lib')
        links = soup.select(sel1)
        for link in links:
            photos.append(link.get('href'))
    return photos


def create_sublists(big_list, sublist_size):
    qty_el = len(big_list)

    for i in range(0, qty_el, int(len(big_list)/ sublist_size)):
        # Create an index range for l of n items:
        yield big_list[i:i + int(len(big_list)/ sublist_size)]



url = urlparse('https://www.quadrinhoseroticos.blog/page/6/')
if url.path != '/':
    number = url.path.split('/')[-2]
else:
    number = 1
valor = 3
for i in range(int(number), int(number) + valor+1):
    print(i)
