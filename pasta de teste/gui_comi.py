import base64
import io
import os
import shutil
import PySimpleGUI as sg
from PIL import Image
from bs4 import BeautifulSoup
import requests
import threading

link_foto = []
text = []


def create_sublists_fotos(photos, sublist_size, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    fotos = soup.select('dl.gallery-item > dt > img')
    texto = soup.select_one('h1')
    text.append(texto.getText())
    for t in fotos:
        comic = t.get('data-src')
        photos.append(requests.get(comic).content)
        link_foto.append(requests.get(comic).content)
    qty_el = len(photos)

    for i in range(0, qty_el, sublist_size):
        # Create an index range for l of n items:
        yield photos[i:i + sublist_size]


def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def to_pdf(caminho, nome, fotos):
    try:
        os.chdir(caminho)
        img = Image.open(fotos[0]).convert("RGB")
        del fotos[0]
        images: list = []
        for f in fotos:
            imgs = Image.open(f).convert("RGB")
            images.append(imgs)
        img.save(f'../{nome}.pdf', save_all=True, append_images=images)
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    finally:
        os.chdir('../')
        shutil.rmtree(caminho)


def download(fotos, filename):
    filename = filename[0].strip().replace(':', '')\
        .replace('?', '').replace('/', '')\
        .replace('!', '').replace(',', '').rstrip()
    os.makedirs(filename, exist_ok=True)
    lista_fotos = []
    i = 0
    for t in fotos:
        with open(os.path.join(filename, f'foto{i}.jpg'), 'wb') as f:
            f.write(t)
        lista_fotos.append(f'foto{i}.jpg')
        i += 1
    to_pdf(filename, filename, lista_fotos)


def display_images(files):
    currently_displaying = {}
    for i in range(len(files)):
        for j in range(len(files[i])):
            if i + 1 > len(files):
                break
            f = files[i][j]
            currently_displaying[(i, j)] = f
    return currently_displaying


def create_lists(n):
    imagens = []
    titulos = []
    links = []

    url = f'https://apiquadrinho.herokuapp.com/pageerotico/{str(n)}'
    response = requests.get(url)
    res = response.json()
    quadrinho = res['Quadrinho']

    for result in quadrinho:
        imagens.append(requests.get(result['img']).content)
        titulos.append(result['title'])
        links.append(result['link'])
    return imagens, titulos, links


def sub_list(biglista, sublista):
    qty_el = len(biglista)

    for i in range(0, qty_el, sublista):
        # Create an index range for l of n items:
        yield biglista[i:i + sublista]


def display_image_window(imfotos):
    try:
        layout = [[sg.Image(data=convert_to_bytes(imfotos, (650, 650)), enable_events=True)]]
        e, v = sg.Window('Revista', layout, modal=True, element_padding=(0, 0), element_justification='c',
                         margins=(0, 0)).read(close=True)
    except Exception as e:
        print(f'** Display image error **', e)
        return


def lay(b):
    sg.theme('Reddit')
    lay = [[]]
    for i in range(len(b)):
        btn = []
        for j in range(len(b[i])):
            btn.append(sg.Button(image_data=convert_to_bytes(b[i][j], (150, 150)), size=(0, 0),
                                 key=(i, j), pad=(0, 0), enable_events=True))

        lay.append(btn)
    layout = [[sg.Column(lay, scrollable=True)],
              [sg.Button('Exit'), sg.Button('Prev'), sg.Button('Next'), sg.Push(), sg.Text('Página'),
               sg.Text('1', k='pag')]]
    return sg.Window('Quadrinho', layout,  finalize=True)


def lay_2(f):
    sg.theme('Reddit')
    lay_conteudo = [[]]
    for i in range(len(f)):
        btn = []
        for j in range(len(f[i])):
            btn.append(sg.Button(image_data=convert_to_bytes(f[i][j], (150, 150)), size=(0, 0),
                                 key=(i, j), pad=(0, 0), enable_events=True, expand_x=True, expand_y=True))
        lay_conteudo.append(btn)
    layout = [[sg.Button('Sair'), sg.Button('Download')],
              [sg.Column(lay_conteudo, scrollable=True, key='coluna')],
              ]
    return sg.Window('Revista', layout, finalize=True, resizable=True)


def main():
    photos = []
    teste = []
    n = 1
    imag, tit, ur = create_lists(n)
    list_imag = sub_list(imag, 4)
    list_urls = sub_list(ur, 4)
    imag_list = [img for img in list_imag]
    urls_list = [url for url in list_urls]

    janela, janela2 = lay(imag_list), None
    current_link = display_images(urls_list)

    while True:
        win, event, values = sg.read_all_windows()
        if win == sg.WIN_CLOSED:
            break
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Prev':
            n = n - 1
            if n <= 1:
                n = 1
            imag, tit, ur = create_lists(n)
            list_imag = sub_list(imag, 4)
            list_urls = sub_list(ur, 4)
            imag_list = [img for img in list_imag]
            urls_list = [url for url in list_urls]

            janela.hide()
            janela = lay(imag_list)
            current_link = display_images(urls_list)
            janela['pag'].update(n)

        if event == 'Next':
            n = n + 1
            imag, tit, ur = create_lists(n)
            list_imag = sub_list(imag, 4)
            list_urls = sub_list(ur, 4)
            imag_list = [img for img in list_imag]
            urls_list = [url for url in list_urls]

            janela.hide()
            janela = lay(imag_list)
            current_link = display_images(urls_list)
            janela['pag'].update(n)

        if event == 'Download':
            threading.Thread(target=download, args=(link_foto, text, )).start()
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


if __name__ == '__main__':
    main()