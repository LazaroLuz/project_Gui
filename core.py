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

# import PySimpleGUI as sg
#
# import converte
#
# layout = [
#     [sg.Text('Window normal', size=(30, 1), key='Status')],
#     [sg.Im(data=converte.convert_to_bytes('icones/relogio.png', (100, 100)), key='Image')]
# ]
# window = sg.Window('Title', layout, resizable=True, finalize=True)
# window.bind('<Configure>', "Configure")
# status = window['Status']
# image = window['Image']
#
# while True:
#
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED:
#         break
#     elif event == 'Configure':
#         if window.TKroot.state() == 'zoomed':
#             status.update(value='Window zoomed and maximized !')
#             image.update(data=converte.convert_to_bytes('icones/relogio.png', (512, 512)))
#         else:
#             status.update(value='Window normal')
#             image.update(data=converte.convert_to_bytes('icones/relogio.png', (100, 100)))
#
# window.close()

import asyncio
import httpx
from bs4 import BeautifulSoup
import PySimpleGUI as sg
import converte
from pegando import pegarfrase
import re


def two_list(link, n):
    def not_lacie(href):
        return href and re.compile(f"/{n}").search(href)
    with httpx.Client() as client:
        response = client.get(link)
        soup = BeautifulSoup(response.text, 'html5lib')
        texto = soup.find_all(href=not_lacie)
        return texto[-1].get('href')
        # links = soup.select('li > div.thumb-conteudo a')
        # x = int(len(links)/2)
        # final_list = lambda test_list, x: [test_list[i:i + x] for i in range(0, len(test_list), x)]
        # output = final_list(links, x)
        # return output[0], output[1]





# soup = two_list('https://horahentai.net/', 2)
soup = two_list('https://www.quadrinhoseroticos.blog/', 2)
print(soup)
#
# async def primeira(links):
#     # window.bind('<Configure>', "Configure")
#     async with httpx.AsyncClient() as client:
#         for link in links:
#             res = await client.get(link.get('href'))
#             soup = BeautifulSoup(res.text, 'html5lib')
#             imgs = soup.select('li > a > img')
#             texto = soup.select_one('h1')
#             for img in imgs:
#                 print(f"primeiro:  {img.get('src')}")
#
#
# async def segundo(links):
#     # window.bind('<Configure>', "Configure")
#     async with httpx.AsyncClient() as client:
#         for link in links:
#             res = await client.get(link.get('href'))
#             soup = BeautifulSoup(res.text, 'html5lib')
#             imgs = soup.select('li > a > img')
#             texto = soup.select_one('h1')
#             for img in imgs:
#
#                 print(f"segundo:  {img.get('src')}")
#
#
# async def main():
#     l1, l2 = two_list()
#     await asyncio.gather(
#         primeira(l1),
#         segundo(l2)
#     )
#
# def chamada():
#     asyncio.run(main())
#
#
# layout = [
#     [sg.Text('Window normal', size=(30, 1), key='Status')],
#     [sg.Im(key='Image'), sg.Im(key='Image2')],
#     [sg.B('inicia'), sg.B('1'), sg.B('2')]
# ]
# window = sg.Window('Title', layout, resizable=True, finalize=True)
# window.bind('<Configure>', "Configure")
# status = window['Status']
# image = window['Image']
# image2 = window['Image2']
#
# while True:
#
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED:
#         break
#     elif event == 'Configure':
#         if window.TKroot.state() == 'zoomed':
#             status.update(font='Arial 32')
#     #         # image.update(data=converte.convert_to_bytes(r.content, (300, 300)))
#         else:
#             status.update(font='Arial 14')
#             # image.update(data=converte.convert_to_bytes('icones/relogio.png', (100, 100)))
#     elif event == 'inicia':
#
#         window.perform_long_operation(chamada(), "Asyncio")
#     # window.perform_long_operation(lambda: asi(window, event), "Asyncio")
#
#
# window.close()

