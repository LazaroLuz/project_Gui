import datetime
import locale
import sched
import time
from random import randint

from cores import *
from base import *
from models import Comics, Reflexao, Pensamento
from converte import convert_to_bytes
from urllib.parse import urlparse


# def lerbanco(site):
#     try:
#         comics = Comics.select().where(Comics.site_name == f'{site}').get()
#         return comics.seletor_link, comics.seletor_img_1, comics.seletor_img_2
#     except:
#         Sg.PopupError('Site não está Cadastrado')


# def procurando_next(link):
#     def not_lacie(href):
#         return href and re.compile("page").search(href)
#     with httpx.Client() as client:
#         response = client.get(link)
#         soup = BeautifulSoup(response.text, 'html5lib')
#         texto = soup.find_all(href=not_lacie)
#         return texto[-1].get('href')


# def pegarfrase():
#     r = [t.tema for t in Reflexao.select()]
#     n = randint(0, len(r)-1)
#     t = Pensamento.select().join(Reflexao).where(Reflexao.tema == f'{r[n]}')
#     n2 = randint(0, len(t)-1)
#     return t[n2].texto
# def chamada_de_revista():
#     janela_foto['baixar_revista'].update(disabled=True)
#     base = urlparse(values['url-site'])
#     url_ = ''
#     try:
#         sel_li, sel_im, sel_im2 = lerbanco(f'{base.scheme}://{base.netloc}/')
#         for p in range(1, int(values['n_pag']) + 1):
#             if p == 1:
#                 url = values['url-site']
#                 url_ = url
#             else:
#                 page = procurando_next(url_)
#                 url_ = page
#
#             janela_foto.perform_long_operation(lambda: coremain(janela_foto, url_, sel_li, sel_im), 'Comics')
#             # coremain(janela_foto, url_, sel_li, sel_im)
#     except:
#         Sg.popup_error('Ocorreu um erro')
#         janela_foto['baixar_revista'].update(disabled=False)


def main():
    title = 'Menu Inicial'
    layout =[
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [
            Sg.Btn('', image_data=convert_to_bytes('icones/f_pdf.png', (60, 60)), key='1', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/Video_down.webp', (60, 60)), key='2', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/relogio.png', (60, 60)), key='3', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/registro.png', (60, 60)), key='4', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/reflexao.png', (60, 60)), key='5', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/config.png', (60, 60)), key='6', pad=(0, 0)),
            Sg.Btn('', image_data=convert_to_bytes('icones/sair.png', (60, 60)), key='sair', pad=(0, 0))
        ]
    ]
    return Sg.Window('Projeto', layout, keep_on_top=True, finalize=True, location=(0, 773))


janela, janela_foto, janela_video, janela_relogio, janela_registro, janela_reflexao, janela_conf = main(), None, None, None, None, None, None


while True:
    windows, event, values = Sg.read_all_windows(timeout=1000)

    if event == Sg.WIN_CLOSED or event == 'sair':
        windows.close()
        if windows == janela:
            break
        elif windows == janela_relogio:
            janela_relogio = None
        elif windows == janela_foto:
            janela_foto = None
        elif windows == janela_video:
            janela_video = None
        elif windows == janela_registro:
            janela_registro = None
        elif windows == janela_reflexao:
            janela_reflexao = None
        elif windows == janela_conf:
            janela_conf = None

    elif event == '1':
        if not janela_foto:
            janela_foto = foto_to_pdf()

    elif event == '2':
        if not janela_video:
            janela_video = video_download()

    elif event == '3':
        if not janela_relogio:
            janela_relogio = relogio()

    elif event == '4':
        if not janela_registro:
            janela_registro = registro()

    elif event == '5':
        if not janela_reflexao:
            janela_reflexao = reflexao()

    elif event == '6':
        if not janela_conf:
            janela_conf = save_config()

    elif event == 'baixar_video':
        janela_video['baixar_video'].update(disabled=True)
        janela_video.perform_long_operation(lambda: download_videos(janela_video, values['url-site']), 'Video')

    elif event == 'baixar_revista':
        janela_foto.perform_long_operation(lambda: asi(janela_foto, values['url-site'], int(values['n_pag'])), 'Comics')

    elif event == 'save_db':
        Comics.create(
            site_name=values['lsite'],
            seletor_link=values['lurl1'],
            seletor_img_1=values['limg1'],
            seletor_img_2=values['limg2']
        )
        janela_conf['lsite'].update('')
        janela_conf['lurl1'].update('')
        janela_conf['limg1'].update('')
        janela_conf['limg2'].update('')
        Sg.Popup('Cadastro realizado', auto_close=True)

    elif janela_registro:
        v_base = []
        try:
            with open('historico.csv') as csvfile:
                for x in csv.reader(csvfile):
                    if x:
                        v_base.append(x)
            janela_registro['-TABLE-'].Update(values=v_base)
        except FileNotFoundError:
            pass

    elif event == 'Download':
        if values['t_frase'] == '':
            print('Campo Tema da Frase não pode esta vazio')
        else:
            janela_reflexao.perform_long_operation(lambda: frase_de_reflexao(janela_reflexao, values['t_frase']), 'Reflexão')
            janela_reflexao['Download'].update(disabled=True)
            janela_reflexao['complete'].update('')
    elif event.startswith('list_tema'):
        janela_reflexao['t_frase'].update(values['list_tema'])

    elif event == 'Reflexão':
        t, p = pegarfrase()
        janela_reflexao['tt_frase'].update(t)
        janela_reflexao['frase'].update(p)

    if janela_relogio:
        now = datetime.datetime.now()
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
        horas = now.strftime("%X")
        data = now.strftime('%A, %d de %B de %Y')
        janela_relogio['horas'].update(horas)
        janela_relogio['data'].update(data)


janela.close()
