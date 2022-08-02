import csv
import datetime
import re
import shutil
import asyncio
import PyPDF2
import httpx
from bs4 import BeautifulSoup

import converte
from models import Comics
from .pdf_pil import Pdf
from urllib.parse import urlparse
import os


def tratar_texto(txt: str) -> str:
    ignore = "!@#$?:;',"
    for char in ignore:
        txt = txt.replace(char, "")
    return txt.strip().rstrip()


def lerbanco(janela, site):
    try:
        comics = Comics.select().where(Comics.site_name == f'{site}').get()
        return comics.seletor_link, comics.seletor_img_1, comics.seletor_img_2
    except:
        janela['capa'].update('', size=(400, 600))
        janela['revista'].update('', size=(400, 600))
        janela['baixar_revista'].update(disabled=False)
        janela['url-site'].update('')
        janela['titulo'].update('')


def procurando_next(link, n):
    def not_lacie(href):
        return href and re.compile(f"/{n}/").search(href)
    with httpx.Client() as client:
        response = client.get(link)
        soup = BeautifulSoup(response.text, 'html5lib')
        texto = soup.find_all(href=not_lacie)
        return texto[-1].get('href')


async def coremain(janela, urlinit, valor):
    janela['baixar_revista'].update(disabled=True)
    base = urlparse(urlinit)
    url_ = ''
    sel_li, sel_im, sel_im2 = lerbanco(janela, f'{base.scheme}://{base.netloc}/')
    try:
        async with httpx.AsyncClient() as client:
            for p in range(1, valor + 1):
                if p == 1:
                    url = urlinit
                    url_ = url
                else:
                    page = procurando_next(url_, p)
                    url_ = page
                janela['m_mostra'].update(url_)
                response = await client.get(url_, timeout=None)
                soup = BeautifulSoup(response.text, 'html5lib')
                links = soup.select(sel_li)
                for link in links:
                    now = datetime.datetime.now()
                    horas = now.strftime("%X")
                    photos = []
                    lista_capa = []
                    if base.netloc in link.get('href'):
                        res = await client.get(link.get('href'), timeout=None)
                        sp = BeautifulSoup(res.text, 'html5lib')
                        fotos = sp.select(sel_im)
                        if fotos:
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
                                        r = await client.get(comic, timeout=None)
                                        try:
                                            capa = await client.get(lista_capa[0], timeout=None)
                                            janela['capa'].update(data=converte.convert_to_bytes(capa.content, (400, 600)))
                                        except:
                                            pass
                                        janela['revista'].update(data=converte.convert_to_bytes(r.content, (400, 600)))
                                        with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                            ft.write(r.content)
                                    with open('historico.csv', 'a+') as csvfile:
                                        csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}://{base.netloc}{base.path}', f'{txt}', f'{horas}'])
                                    Pdf(f'{base.netloc}/{txt}', txt, photos)
                                    shutil.rmtree(f'{base.netloc}/{txt}')
                            except FileNotFoundError:
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
                                    r = await client.get(comic, timeout=None)
                                    try:
                                        capa = await client.get(lista_capa[0], timeout=None)
                                        janela['capa'].update(data=converte.convert_to_bytes(capa.content, (400, 600)))
                                    except:
                                        pass
                                    janela['revista'].update(data=converte.convert_to_bytes(r.content, (400, 600)))
                                    with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                        ft.write(r.content)
                                with open('historico.csv', 'a+') as csvfile:
                                    csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}://{base.netloc}{base.path}', f'{txt}', f'{horas}'])
                                Pdf(f'{base.netloc}/{txt}', txt, photos)
                                shutil.rmtree(f'{base.netloc}/{txt}')
                        else:
                            continue
                    else:
                        continue
    except:
        pass
    janela['capa'].update('', size=(400, 600))
    janela['revista'].update('', size=(400, 600))
    janela['baixar_revista'].update(disabled=False)
    janela['url-site'].update('')
    janela['titulo'].update('')


def asi(j, v1, n1):
    asyncio.run(coremain(j, v1, n1))


