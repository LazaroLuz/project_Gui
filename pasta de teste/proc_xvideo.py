import base64
import re
import threading
import time
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import requests
import io
import PySimpleGUI as Sg
import vlc
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError


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
        except Exception:
            dataBytesIO: BytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)
        except UnidentifiedImageError:
            pass
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


titulo: list = []
link_down: list = []


def o_link(url):
    titulo.clear()
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    ser = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(url)
    s = BeautifulSoup(driver.page_source, features='lxml')
    nome_titulo = s.select_one("h2.page-title")
    titulo.append(nome_titulo.getText().split('.')[0])
    script = s.select('div#video-player-bg script')
    texto = re.findall('html5player.setVideoUrlLow+.*', str(script))
    atividade = str(texto).split("'")[1]
    driver.close()

    return atividade


def get_xvideos(n):
    xv_link: list = []
    xv_imagem: list = []
    if n == 1:
        url = 'https://xvideos.com'
    else:
        url = f'https://xvideos.com/new/{str(n)}'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    ser=Service("chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features='lxml')
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, features='lxml')
    # links = soup.select('div.thumb-inside > div.videopv > a')
    links = soup.select('div.thumb-inside > div.thumb > a')
    imagens = soup.select('div.thumb-inside > div.thumb > a > img')
    # page = soup.select_one('.next-page')
    # print(f"https://xvideos.com{page.get('href')}")
    for i in range(len(links)):
        xv_link.append(f"https://xvideos.com{links[i].get('href')}")
        xv_imagem.append(requests.get(imagens[i].get('src')).content)
    driver.close()

    return xv_imagem, xv_link


def create_sublists(big_list, sublist_size):
    qty_el = len(big_list)

    for i in range(0, qty_el, sublist_size):
        # Create an index range for l of n items:
        yield big_list[i:i + sublist_size]


def tela(b):
    Sg.theme('Reddit')
    lay = [[]]
    for i in range(len(b)):
        botao = []
        for j in range(len(b[i])):
            botao.append(Sg.Button(image_data=convert_to_bytes(b[i][j], (150, 150)), size=(0, 0),
                                   key=(i, j), pad=(0, 0), enable_events=True))
        lay.append(botao)
    layout = [[Sg.Column(lay, scrollable=True)],
              [Sg.Button('Exit'), Sg.Button('Prev'), Sg.Button('Next'), Sg.Push(), Sg.Text('Página'),
               Sg.Text('1', k='pag')]]
    return Sg.Window('Quadrinho', layout,  finalize=True, resizable=True)


def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return Sg.Button(name, size=(6, 1), pad=(1, 1))


def view_video():
    layout = [[Sg.Image('', size=(500, 240), key='-VID_OUT-')],
              [Sg.Slider(range=(0, 1000), resolution=1, key='slider_time',
                         expand_x=True, orientation='h', enable_events=True, border_width=1, p=(0, 0))],
              [btn('Play'), btn('Pause'), btn('Stop'), btn('Download')],
              [Sg.Text('00:00 / 00:00', key='-MESSAGE_AREA-')]
              ]
    return Sg.Window('Mini Player', layout, element_justification='center', finalize=True, resizable=True)


def display_images(files):
    currently_displaying = {}
    for i in range(len(files)):
        for j in range(len(files[i])):
            if i + 1 > len(files):
                break
            f = files[i][j]
            currently_displaying[(i, j)] = f
    return currently_displaying


def down_video(title, down):
    r = requests.get(down)
    with open(f'{title}.mp4', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


n = 1
x_imag, x_link = get_xvideos(n)
x_l = create_sublists(x_link, 4)
x_i = create_sublists(x_imag, 4)
link = [b for b in x_l]
img = [t for t in x_i]

janela, janela_2 = tela(img), None
currently_displaying = display_images(link)

# creating a vlc instance
vlc_instance = vlc.Instance()
# creating a media player
player = vlc_instance.media_player_new()
timeslider_last_val = ""
timeslider_last_update = time.time()

while True:
    win, event, values = Sg.read_all_windows(timeout=1000)
    # if win == Sg.WIN_CLOSED:
    #     break
    if event in (Sg.WIN_CLOSED, 'Exit'):
        break
    if isinstance(event, tuple):
        link_down.clear()
        link_down.append(currently_displaying.get(event))
        link_video = o_link(currently_displaying.get(event))
        janela_2 = view_video()
        janela_2['-VID_OUT-'].expand(True, True)
        media = vlc_instance.media_new(link_video)
        player.set_media(media)
        player.audio_set_volume(200)
        player.set_hwnd(janela_2['-VID_OUT-'].Widget.winfo_id())
    elif event == 'Play':
        player.play()
    elif event == 'Pause':
        player.pause()
    elif event == 'Stop':
        player.stop()
        janela_2.hide()
        janela_2.Close()
    elif player.is_playing():
        janela_2['-MESSAGE_AREA-'].update(
            "{:02d}:{:02d} / {:02d}:{:02d}".format(*divmod(player.get_time() // 1000, 60),
                                                   *divmod(player.get_length() // 1000, 60)))

        length = player.get_length()
        dbl = length * 0.001
        janela_2['slider_time'].update(range=(0, dbl))
        tyme = player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        timeslider_last_val = ("%.0f" % dbl) + ".0"

        if time.time() > (timeslider_last_update + 2.0):
            janela_2['slider_time'].update(dbl)

        if values is None:
            pass
        else:
            nval = values['slider_time']
            sval = str(nval)
            if timeslider_last_val != sval:
                timeslider_last_update = time.time()
                mval = "%.0f" % (nval * 1000)
                player.set_time(int(mval))

    elif event == 'Download':
        threading.Thread(target=down_video, args=(titulo[0], link_down[0]))

    if event == 'Next':
        n = n + 1
        x_imag, x_link = get_xvideos(n)
        x_l = create_sublists(x_link, 4)
        x_i = create_sublists(x_imag, 4)

        link = [b for b in x_l]
        img = [t for t in x_i]
        janela.hide()
        # janela = None
        janela = tela(img)
        currently_displaying = display_images(link)
        janela['pag'].update(n)
    if event == 'Prev':
        n = n - 1
        if n <= 1:
            n = 1
        x_imag, x_link = get_xvideos(n)
        x_l = create_sublists(x_link, 4)
        x_i = create_sublists(x_imag, 4)

        link = [b for b in x_l]
        img = [t for t in x_i]
        janela.close()
        # janela = None
        janela = tela(img)
        currently_displaying = display_images(link)
        janela['pag'].update(n)

win.close()