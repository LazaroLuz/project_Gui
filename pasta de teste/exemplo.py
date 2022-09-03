import base64
import os.path
import pickle
import urllib.parse
from time import sleep

import httpx
from bs4 import BeautifulSoup
import PySimpleGUI as Sg
from base_db import Quadrinho, Imagens
import converte


def calback(link, funcao):
    funcao(link)


revista_lista: list = []


def encriptar(title, lista_img):
    path = 'past'
    lista_encod: list = []
    try:
        uncle_bob = Quadrinho.create(name=title)
        for img in lista_img:
            with open(f'{path}/{img}', 'rb') as file:
                encod = file.read()
                resultado_bytes = base64.b64encode(encod)
                Imagens.create(allporn=uncle_bob, fotos=resultado_bytes)
                # lista_encod.append(resultado_bytes)
    # dict_revista = {'titulo': title,
    #                 'fotos': lista_encod}
    # revista_lista.append(dict_revista)
    except:
        pass
    finally:
        sleep(0.2)
        for img in lista_img:
            os.unlink(f'{path}/{img}')

    # with open('quadrinho.pkl', 'wb') as arquivo:
    #     pickle.dump(revista_lista, arquivo)


def revista(url: str):
    base = urllib.parse.urlparse(url)
    with httpx.Client() as client:
        response = client.get(url, timeout=None)
        soup = BeautifulSoup(response.content)
        info = soup.select('article > div.border > figure > a')
        next_page = soup.select_one('a.next.page-numbers')
        for inf in info:

            lista_img: list = []
            if base.netloc in inf.get('href'):
                img = inf.find('div')
                title = inf.get('title')
                link = inf.get('href')
                imagens = img.get('style')[21:][:-2]
                res = client.get(imagens, timeout=None)
                janela['texto'].update(title)
                progress_bar = janela['progress']

                janela['img'].update(data=converte.convert_to_bytes(res.content, (40, 35)))
                resposta = client.get(link, timeout=None)
                s = BeautifulSoup(resposta.content)
                foto = s.select('dl > dt.gallery-icon > img')

                janela['progress'].update(max=len(foto))
                try:
                    uncle_bob = Quadrinho.create(name=title)
                    for i, ft in enumerate(foto):
                        result = (i + 1) * 100 / len(foto)
                        progress_bar.update_bar(int(result))  # show 10% complete
                        comic = ft.get('src')
                        Imagens.create(allporn=uncle_bob, fotos=comic)
                except:
                    pass
                #     lista_img.append(os.path.basename(comic))
                #     resultado = client.get(comic, timeout=None)
                #     resultado_bytes = resultado.content
                #     with open(os.path.join('past', os.path.basename(comic)), 'wb') as arquivo:
                #         arquivo.write(resultado_bytes)
                # sleep(0.2)
                # encriptar(title, lista_img)

    if next_page:
        url_link = next_page.get('href')

        janela['link'].update(url_link)
        calback(url_link, revista)
    else:
        # with open('revista.pkl', 'wb') as arquivo:
        #     pickle.dump(revista_lista, arquivo)
        # print(revista_lista)
        print('Acabou')


layout = [
    [Sg.T('Quadrinho Erotico')],
    [Sg.T('Url:'), Sg.In(key='LINK'), Sg.B('Ok')],
    [Sg.Frame('Frame', [
        [
            Sg.T('', size=(30, 1), key='texto'),
            Sg.ProgressBar(max_value=100, orientation='h', size=(25, 5), key='progress'),
            Sg.Im(key='img')
        ]], key='-FRAME-', grab=True)],
    [Sg.T('', key='link')],
    [Sg.B('Exit')]
]

janela = Sg.Window('Exemplo', layout)

while True:  # Event Loop
    event, values = janela.read()
    if event in (Sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Ok':
        janela.perform_long_operation(lambda: revista(values['LINK']), 'action')

janela.close()