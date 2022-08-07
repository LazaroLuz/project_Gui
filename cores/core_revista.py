import csv
import datetime
import re
import shutil
import asyncio
import PyPDF2
import httpx
from bs4 import BeautifulSoup  # type: ignore

import converte
from models import Comics
from .pdf_pil import Pdf
from urllib.parse import urlparse
import os

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
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


def create_sublists(big_list, sublist_size):
    qty_el = len(big_list)

    for i in range(0, qty_el, int(len(big_list)/ sublist_size)):
        # Create an index range for l of n items:
        yield big_list[i:i + int(len(big_list)/ sublist_size)]


def dividir(janela, urlinit , valor):
    janela['baixar_revista'].update(disabled=True)
    base = urlparse(urlinit)
    print(base)
    url_ = ''
    tir: list = []
    try:
        sel_li, sel_im, sel_im2 = lerbanco(janela, f'{base.scheme}://{base.netloc}/')
        with httpx.Client() as client:
            for p in range(1, valor + 1):
                if p == 1:
                    url = urlinit
                    url_ = url
                else:
                    page = procurando_next(url_, p)
                    url_ = page
                response = client.get(url_, timeout=None)
                soup = BeautifulSoup(response.text, 'html5lib')
                links = soup.select(sel_li)
                for link in links:
                    if base.netloc in link.get('href'):
                        tir.append(link.get('href'))
                    else:
                        continue
        # x = int(len(tir) / 2)
        # print(x)
        # final_list = lambda test_list, x: [test_list[i:i + x] for i in range(0, len(test_list), x)]
        # output = final_list(tir, x)
        # print(output)
        x1 = create_sublists(tir, 2)
        output = [i for i in x1]
        return output[0], output[1], sel_im, sel_im2
    except:
        print('Ocorreu algum erro')



def tratar_texto(txt: str) -> str:
    ignore = r"!@#$?:;',/\\"
    for char in ignore:
        txt = txt.replace(char, "")
    return txt.strip().rstrip()


async def core1(janela, links, sel_im, sel_im2):
    base = urlparse(links[0])
    await asyncio.sleep(0.03)
    try:
        async with httpx.AsyncClient() as client:
            for link in links:
                now = datetime.datetime.now()
                horas = now.strftime("%X")
                photos = []
                res = await client.get(link, timeout=None)
                sp = BeautifulSoup(res.text, 'html5lib')
                album1 = sp.select(sel_im)

                if album1:
                    fotos = album1
                else:
                    album2 = sp.select(sel_im2)
                    fotos = album2
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
                                photos.append(os.path.basename(comic))
                                r = await client.get(comic, timeout=None)
                                janela['capa'].update(data=converte.convert_to_bytes(r.content, (400, 600)))
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
                            photos.append(os.path.basename(comic))
                            r = await client.get(comic, timeout=None)
                            janela['capa'].update(data=converte.convert_to_bytes(r.content, (400, 600)))
                            with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                ft.write(r.content)
                        with open('historico.csv', 'a+') as csvfile:
                            csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}://{base.netloc}{base.path}', f'{txt}', f'{horas}'])
                        Pdf(f'{base.netloc}/{txt}', txt, photos)
                        shutil.rmtree(f'{base.netloc}/{txt}')
                else:
                    continue
    except:
        pass


async def core2(janela, links, sel_im, sel_im2):
    base = urlparse(links[0])
    await asyncio.sleep(0.04)
    try:
        async with httpx.AsyncClient() as client:
            for link in links:
                now = datetime.datetime.now()
                horas = now.strftime("%X")
                photos = []
                res = await client.get(link, timeout=None)
                sp = BeautifulSoup(res.text, 'html5lib')
                album1 = sp.select(sel_im)

                if album1:
                    fotos = album1
                else:
                    album2 = sp.select(sel_im2)
                    fotos = album2
                if fotos:
                    texto = sp.select_one('h1').text
                    txt = tratar_texto(texto)
                    janela['titulo2'].update(txt)
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
                                print(comic)
                                photos.append(os.path.basename(comic))
                                r = await client.get(comic, timeout=None)
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
                            photos.append(os.path.basename(comic))
                            r = await client.get(comic, timeout=None)
                            janela['revista'].update(data=converte.convert_to_bytes(r.content, (400, 600)))
                            with open(os.path.join(f'{base.netloc}/{txt}', os.path.basename(comic)), 'wb') as ft:
                                ft.write(r.content)
                        with open('historico.csv', 'a+') as csvfile:
                            csv.writer(csvfile, delimiter=',').writerow([f'{base.scheme}://{base.netloc}{base.path}', f'{txt}', f'{horas}'])
                        Pdf(f'{base.netloc}/{txt}', txt, photos)
                        shutil.rmtree(f'{base.netloc}/{txt}')
                else:
                    continue

    except:
        pass


async def main(janela, n_link, n):
    l1, l2, im, im2 = dividir(janela, n_link, n)

    await asyncio.gather(
        core1(janela, l1, im, im2),
        core2(janela, l2, im, im2), return_exceptions=False
    )
    janela['capa'].update('', size=(400, 600))
    janela['revista'].update('', size=(400, 600))
    janela['baixar_revista'].update(disabled=False)
    janela['url-site'].update('')
    janela['titulo2'].update('')
    janela['titulo'].update('')
    # loop.close()


def chamada(janela,n_link, n):
    # asyncio.run(main(janela))

    asyncio.run(main(janela, n_link, n))
