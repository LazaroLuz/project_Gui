""" projeto de revista online"""
from urllib.parse import urlparse

import httpx
import PySimpleGUI as Sg
from bs4 import BeautifulSoup as Bs

import converte


def create_lists(url: str) -> tuple:
    imagens: list = []
    titulos: list = []
    links: list = []
    base = urlparse(url)
    with httpx.Client() as client:
        response = client.get(url)
        soup = Bs(response.content)
        info = soup.select('article > div.border > figure > a')
        for inf in info:
            if base.netloc in inf.get('href'):
                img = inf.find('div')
                title = inf.get('title')
                link = inf.get('href')
                imagens.append(img.get('style')[21:][:-2])
                titulos.append(title)
                links.append(link)
    return imagens, titulos, links


def sub_list(biglista, sublista):
    qty_el = len(biglista)

    for i in range(0, qty_el, sublista):
        # Create an index range for l of n items:
        yield biglista[i:i + sublista]


def lay_btn(nome, b):
    Sg.theme('Reddit')
    lay = [[]]
    for i in range(len(b)):
        btn = []
        txt = []
        for j in range(len(b[i])):
            with httpx.Client() as client:
                r = client.get(b[i][j])
            btn.append(Sg.Button(image_data=converte.convert_to_bytes(r.content, (150, 150)),
                                key=(i, j), enable_events=True, tooltip=nome[i][j]))
        lay.append(btn)
    layout = [
        [Sg.Column(lay, scrollable=True)],
        [Sg.Button('Exit'), Sg.Button('Prev'), Sg.Button('Next'), Sg.Push(), Sg.Text('Página'),
            Sg.Text('1', k='pag')]]
    return Sg.Window('Quadrinho', layout,  finalize=True)


def display_image_window(imfotos):
    try:
        layout = [[Sg.Image(data=converte.convert_to_bytes(imfotos, (720, 1024)), enable_events=True)]]
        e, v = Sg.Window('Revista', layout, modal=True, element_padding=(0, 0), element_justification='c',
                         margins=(0, 0)).read(close=True)
    except Exception as e:
        # print(f'** Display image error **', e)
        return


def display_images(files):
    currently_displaying = {}
    for i in range(len(files)):
        for j in range(len(files[i])):
            if i + 1 > len(files):
                break
            f = files[i][j]
            currently_displaying[(i, j)] = f
    return currently_displaying


def lay_2(f):
    
    lay_conteudo = [[]]
    for i in range(len(f)):
        btn = []
        for j in range(len(f[i])):
            btn.append(Sg.Button(image_data=converte.convert_to_bytes(f[i][j], (400, 400)), size=(0, 0),
                                key=(i, j), pad=(0, 0), enable_events=True, expand_x=True, expand_y=True))
        lay_conteudo.append(btn)
    layout = [
        [Sg.Button('Sair'), Sg.Button('Download')],
        [Sg.Column(lay_conteudo, scrollable=True, key='coluna')],
        ]
    return Sg.Window('Revista', layout, finalize=True, resizable=True)


link_foto = []
text = []


def create_sublists_fotos(photos, sublist_size, url):
    response = httpx.get(url)
    soup = Bs(response.text, features='html.parser')
    fotos = soup.select('dl.gallery-item > dt > img')

    texto = soup.select_one('h1')
    text.append(texto.getText())
    for t in fotos:
        comic = t.get('src')
        photos.append(httpx.get(comic).content)
        link_foto.append(httpx.get(comic).content)
    qty_el = len(photos)

    for i in range(0, qty_el, sublist_size):
        # Create an index range for l of n items:
        yield photos[i:i + sublist_size]

def main():
    photos = []
    teste = []
    img, tit, lin = create_lists('https://www.quadrinhoseroticos.blog/')
    lista_imagem = sub_list(img, 4)
    lista_url = sub_list(lin, 4)
    lista_titulo = sub_list(tit, 4)
    imagens = [jpg for jpg in lista_imagem]
    urls = [http for http in lista_url]
    titulos = [title for title in lista_titulo]

    janela, janela2 = lay_btn(titulos, imagens), None
    current_link = display_images(urls)
    n: int = 1
    while True:
        win, event, values = Sg.read_all_windows()
        if win == Sg.WIN_CLOSED:
            break
        if event in (Sg.WIN_CLOSED, 'Exit'):
            break
        print(event)
        print(current_link.get(event))
        if event == 'Prev':
            n =- 1
            if n <= 1:
                n = 1
            if n == 1:
                url = f'https://www.quadrinhoseroticos.blog/'
            else:
                url = f'https://www.quadrinhoseroticos.blog/page/{n}/'
            imag, tit, ur = create_lists(url)
            list_imag = sub_list(imag, 4)
            list_urls = sub_list(ur, 4)
            list_tits = sub_list(tit, 4)
            imag_list = [img for img in list_imag]
            urls_list = [url for url in list_urls]
            tits_list = [titl for titl in list_tits]

            janela.hide()
            # janela.refresh()
            janela = lay_btn(tits_list, imag_list)

            current_link = display_images(urls_list)
            janela['pag'].update(n)

        if event == 'Next':
            n = n + 1
            url = f'https://www.quadrinhoseroticos.blog/page/{n}/'
            imag, tit, ur = create_lists(url)
            list_imag = sub_list(imag, 4)
            list_urls = sub_list(ur, 4)
            list_tits = sub_list(tit, 4)
            imag_list = [img for img in list_imag]
            urls_list = [url for url in list_urls]
            tits_list = [titl for titl in list_tits]

            janela.hide()

            janela = lay_btn(tits_list, imag_list)
            janela.refresh()
            current_link = display_images(urls_list)
            janela['pag'].update(n)
        if win == janela:
            teste.clear()
            photos.clear()
            link_foto.clear()
            text.clear()
            jan = create_sublists_fotos(photos, 6, current_link.get(event))
            photos_link = [f for f in jan]
            janela.hide()
            janela2 = lay_2(photos_link)
            janela2['coluna'].expand(True, True)
            teste.append(display_images(photos_link))
        if win == janela2:
            display_image_window(teste[0].get(event))

            if event == 'Sair':
                janela2.hide()
                janela.un_hide()

    janela.close()


main()