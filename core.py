# import httpx
# from bs4 import BeautifulSoup
#
#
# res = httpx.get('https://hqerotico.com/')
# soup = BeautifulSoup(res.text, 'html5lib')
# links = soup.select('li > div.thumb-conteudo a')
# for link in links:
#     res = httpx.get(link.get('href'))
#     soup = BeautifulSoup(res.text, 'html5lib')
#     imgs = soup.select('li > a > img')
#     for img in imgs:
#         print(img.get('src'))

import PySimpleGUI as sg

import converte

layout = [
    [sg.Text('Window normal', size=(30, 1), key='Status')],
    [sg.Im(data=converte.convert_to_bytes('icones/relogio.png', (100, 100)), key='Image')]
]
window = sg.Window('Title', layout, resizable=True, finalize=True)
window.bind('<Configure>', "Configure")
status = window['Status']
image = window['Image']

while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Configure':
        if window.TKroot.state() == 'zoomed':
            status.update(value='Window zoomed and maximized !')
            image.update(data=converte.convert_to_bytes('icones/relogio.png', (512, 512)))
        else:
            status.update(value='Window normal')
            image.update(data=converte.convert_to_bytes('icones/relogio.png', (100, 100)))

window.close()



