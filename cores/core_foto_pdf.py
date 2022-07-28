import csv
import datetime

import PyPDF2
import httpx
from bs4 import BeautifulSoup

import converte
from .pdf_pil import Pdf
from urllib.parse import urlparse
import os
import re


now = datetime.datetime.now()
horas = now.strftime("%X")
def tratar_texto(txt: str) -> str:
    ignore = "!@#$?:;'"
    for char in ignore:
        txt = txt.replace(char, "")
    return txt.strip().rstrip()


def coremain(janela, url, sel1, sel_img):
    base = urlparse(url)
    with httpx.Client() as client:
        response = client.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        links = soup.select(sel1)
        for link in links:
            photos = []
            lista_capa = []
            if base.netloc in link.get('href'):
                res = client.get(link.get('href'))
                sp = BeautifulSoup(res.text, 'html5lib')
                fotos = sp.select(sel_img)
                texto = sp.select_one('h1').text
                txt = tratar_texto(texto)
                janela['titulo'].update(txt)
                try:
                    file = open(f'{base.netloc}/{txt}.pdf', 'rb')
                    readpdf = PyPDF2.PdfFileReader(file)
                    totalpages = readpdf.numPages
                    if totalpages == len(fotos):
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
                            lista_capa.append(comic)
                            photos.append(os.path.basename(comic))
                            r = client.get(comic).content
                            capa = client.get(lista_capa[0]).content
                            janela['capa'].update(data=converte.convert_to_bytes(capa, (400, 600)))
                            janela['revista'].update(data=converte.convert_to_bytes(r, (400, 600)))
                            with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                ft.write(r)
                        with open('../historico.csv', 'a+') as csvfile:
                            csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}//{base.netloc}{base.path}', f'{txt}', f'{horas}'])
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
                            photos.append(os.path.basename(comic))
                            r = client.get(comic).content
                            # capa = client.get(photos[0]).content
                            # janela['capa'].update(data=converte.convert_to_bytes(capa, (400, 600)))
                            janela['revista'].update(data=converte.convert_to_bytes(r, (400, 600)))
                            with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                ft.write(r)
                        with open('../historico.csv', 'a+') as csvfile:
                            csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}//{base.netloc}{base.path}', f'{txt}', f'{horas}'])
                    Pdf(f'{base.netloc}/{txt}', txt, photos)
            else:
                continue




