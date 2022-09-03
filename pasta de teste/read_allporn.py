import base64

import httpx
from natsort import natsorted
from base_db import Quadrinho, Imagens
import PySimpleGUI as Sg
from converte import convert_to_bytes


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

r = [t.name for t in Quadrinho.select()]
ordenado = natsorted(r)
layout = [
    [Sg.Combo(ordenado, enable_events=True, s=(20, 1), key='titulo')],
    [Sg.B(image_data=convert_to_bytes('atras.png', (40, 60)), k='Voltar'),
        Sg.Image(key='IMAGE'),
        Sg.B(image_data=convert_to_bytes('frente.png', (40, 60)), k='Ir')]

]

janela = Sg.Window('teste', layout, return_keyboard_events=True)
i = 0
while True:
    event, values = janela.read()
    if event == Sg.WIN_CLOSED or event == 'Escape:27':
        break
    if event.startswith('titulo'):
        foto = [f.fotos for f in Imagens.select().join(Quadrinho).where(Quadrinho.name == f"{values['titulo']}")]
        r = httpx.get(foto[0], headers=head)
        data = base64.b64encode(r.content)
        with open('test.jpg', 'wb') as file:
            file.write(r.content)
        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))
    if event == 'Ir' or event == 'Right:39':

        if i >= len(foto) - 1:
            i = 0
        else:
            i += 1
        r = httpx.get(foto[i], headers=head)
        data = base64.b64encode(r.content)
        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))

    if event == 'Voltar' or event == 'Left:37':
        if i == 0:
            i = len(foto) - 1
        else:
            i -= 1
        r = httpx.get(foto[i], headers=head)
        data = base64.b64encode(r.content)
        janela['IMAGE'].update(data=convert_to_bytes(data, (800, 900)))


janela.close()
