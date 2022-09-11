import base64
import os
from typing import List, Any

from PIL import Image
import httpx
from natsort import natsorted
# from base_db import Quadrinho, Imagens
from model_db import Site, Revista, Imagens
import PySimpleGUI as Sg
from converte import convert_to_bytes


def tratar_texto(txt: str) -> str:
    ignore = "!@#$?:;',/"
    for char in ignore:
        txt = txt.replace(char, "")
    return txt.strip().rstrip()


def pdf():
    lista = os.listdir('past')
    lista_foto = natsorted(lista)
    imagem1 = Image.open(os.path.join('past', lista_foto[0])).convert('RGB')

    del lista_foto[0]
    imgs = []
    for l_img in lista_foto:
        fot = Image.open(os.path.join('past', l_img)).convert("RGB")
        imgs.append(fot)
    nome = tratar_texto(values['revistas'])

    imagem1.save(f"{nome}.pdf", save_all=True, append_images=imgs)

    for im in lista:
        os.unlink(os.path.join('past', im))
    return 'PDF Concluido'


head = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
        'Safari/537.36 '
}

r = [t.name for t in Site.select()]
ordenado = natsorted(r)
layout = [
    [Sg.Combo(ordenado, enable_events=True, s=(40, 1), key='titulo'),
        Sg.Combo([], enable_events=True, s=(40, 1), key='revistas'), Sg.Push(), Sg.B('Download')],
    [Sg.B(image_data=convert_to_bytes('atras.png', (40, 60)), k='Voltar'),
        Sg.Image(key='IMAGE'),
        Sg.B(image_data=convert_to_bytes('frente.png', (40, 60)), k='Ir')],
    [Sg.T('', key='END'), Sg.Push(), Sg.T('Página'), Sg.T('', key='N')]

]

janela = Sg.Window('teste', layout, return_keyboard_events=True)
i = 0
while True:
    event, values = janela.read()
    if event == Sg.WIN_CLOSED or event == 'Escape:27':
        break
    if event.startswith('titulo'):
        ft: list[Any] = [f.name for f in Revista.select().join(Site).where(Site.name == f"{values['titulo']}")]

        janela['revistas'].update(values=ft)
    if event.startswith('revistas'):
        foto: list[Any] = [f.fotos for f in Imagens.select().join(Revista).where(Revista.name == f"{values['revistas']}")]

        r = httpx.get(foto[0], headers=head, timeout=None)
        data = base64.b64encode(r.content)
        with open('test.jpg', 'wb') as file:
            file.write(data)
        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))
        janela['N'].update(1)
    if event == 'Ir' or event == 'Right:39':

        if i >= len(foto) - 1:
            i = 0
        else:
            i += 1
        r = httpx.get(foto[i], headers=head, timeout=None)
        data = base64.b64encode(r.content)

        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))
        janela['N'].update(i+1)

    if event == 'Voltar' or event == 'Left:37':
        if i == 0:
            i = len(foto) - 1
        else:
            i -= 1
        r = httpx.get(foto[i], headers=head, timeout=None)
        data = base64.b64encode(r.content)
        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))
        janela['N'].update(i+1)

    if event == 'Download':
        janela['END'].update('')
        for img in foto:
            response = httpx.get(img, headers=head, timeout=None)
            with open(os.path.join('past', os.path.basename(img)), 'wb') as arquivo:
                arquivo.write(response.content)
        janela.perform_long_operation(pdf, 'ACTION')
    elif event == 'ACTION':
        janela['END'].update(f'{values[event]}')

janela.close()
