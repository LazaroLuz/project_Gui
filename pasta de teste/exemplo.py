import base64
import os.path
import urllib.parse
from time import sleep

import httpx
from bs4 import BeautifulSoup
import PySimpleGUI as Sg
# from base_db import Quadrinho, Imagens
from model_db import Site, Revista, Imagens
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
                base64_message = resultado_bytes.decode('utf-8')
                Imagens.create(allporn=uncle_bob, fotos=base64_message)
                # lista_encod.append(resultado_bytes)
    # dict_revista = {'titulo': title,
    #                 'fotos': lista_encod}
    # revista_lista.append(dict_revista)
    except:
        foto = [f.fotos for f in Imagens.select().join(Quadrinho).where(Quadrinho.name == title)]
        if len(foto) >= len(lista_img):
            pass
        else:
            qd = Quadrinho.get(Quadrinho.name == title)
            im = Imagens.get(Imagens.allporn == qd)
            im.delete_instance()
            for img in lista_img:
                with open(f'{path}/{img}', 'rb') as file:
                    encod = file.read()
                    resultado_bytes = base64.b64encode(encod)
                    base64_message = resultado_bytes.decode('utf-8')
                    Imagens.create(allporn=qd, fotos=base64_message)
            print(f'atualizado, {title}')
    finally:
        sleep(0.2)
        for img in lista_img:
            os.unlink(f'{path}/{img}')

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
nome_site = Site.create(name='Maniacos por Comics')


def revista(url: str):
    base = urllib.parse.urlparse(url)
    janela['link'].update(url)
    with httpx.Client() as client:
        response = client.get(url, headers=head, timeout=None)
        soup = BeautifulSoup(response.content)
        info = soup.select('.aneTemaMa92318c_5fe9ae > div > a')
        next_page = soup.select('body > div.aneTemaMa92318c_Aabb50 > div > ul > li > a')

        for inf in info:
            link = inf.get('href')
            img = inf.select_one('span > img')
            title = img.get('alt')
            # print(f'imagem = {img.get("src")}')
            # print(f'link  = {link}')
            # print(title)
            lista_img: list = []
            if base.netloc in inf.get('href'):
            #     img = inf.find('div')
            #     title = inf.get('title')
            #     link = inf.get('href')
            #     imagens = img.get('style')[21:][:-2]
                imagens = img.get('src')
                res = client.get(imagens, headers=head, timeout=None)
                janela['texto'].update(title)
                progress_bar = janela['progress']

                janela['img'].update(data=converte.convert_to_bytes(res.content, (40, 35)))
                resposta = client.get(link, headers=head, timeout=None)
                s = BeautifulSoup(resposta.content)
                photo = s.select('#dgwt-jg-1 > figure > a')
                if photo:
                    foto = photo
                else:
                    foto = s.select('div.aneTemaMa92318c_243f73 > div > div.aneTemaMa92318c_8e8caa > p > a')
                # print(len(foto))
                # janela['progress'].update(max=len(foto))
                try:
                    if len(foto) > 1:
                        # uncle_bob = Quadrinho.create(name=title, )
                        uncle_bob = Revista.create(name=title, site=nome_site)
                        for i, ft in enumerate(foto):
                            result = (i + 1) * 100 / len(foto)
                            progress_bar.update_bar(int(result))  # show 10% complete
                            comic = ft.get('href')
                            # print(comic)
                            Imagens.create(allporn=uncle_bob, fotos=comic)
                    else:
                        pass
                #             # lista_img.append(os.path.basename(comic))
            #             # resultado = client.get(comic, timeout=None)
            #             # resultado_bytes = resultado.content
            #             # with open(os.path.join('past', os.path.basename(comic)), 'wb') as arquivo:
            #             #     arquivo.write(resultado_bytes)
            #         # sleep(0.2)
            #         # encriptar(title, lista_img)
                except:
                    pass

    if next_page[-1].getText() == 'Próximo':
        url_link = next_page[-1].get('href')
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