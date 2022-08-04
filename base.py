from random import choice, choices

import PySimpleGUI as Sg
from converte import convert_to_bytes


# DarkGrey8 = {'BACKGROUND': '#19232D',
#               'TEXT': '#ffffff',
#               'INPUT': '#32414B',
#               'TEXT_INPUT': '#ffffff',
#               'SCROLL': '#505F69',
#               'BUTTON': ('#ffffff', '#32414B'),
#               'PROGRESS': ('#505F69', '#32414B'),
#               'BORDER': 1, 'SLIDER_DEPTH': 2, 'PROGRESS_DEPTH': 2,
#               }
#
# Sg.theme_add_new('DarkGrey8', DarkGrey8)
from models import Reflexao, Pensamento

Sg.theme('random')


def foto_to_pdf():
    title = 'Foto Para Pdf'
    layout =[
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Frame('', [
            [
                Sg.T('Coloque a Url: '),
                Sg.In(key='url-site', expand_x=True),
                Sg.B(image_data=convert_to_bytes('icones/download.png', (40, 50)), key='baixar_revista')
            ],
            [Sg.T('Numero de Pagínas'), Sg.Spin(values=[i for i in range(1, 150)], initial_value=1, size=(6, 1), key='n_pag')]
        ], expand_x=True)],
        [Sg.T('', key='titulo', font='Any 20', text_color='#ffffff'), Sg.Push(), Sg.T('', key='titulo2', font='Any 20', text_color='#ffffff')],
        [Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='capa')]
        ]), Sg.Im(data=convert_to_bytes('icones/setas.png', (80, 80))), Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='revista')]
        ])],
        [Sg.T('', k='m_mostra')]
    ]
    return Sg.Window('', layout, finalize=True, location=(0, 0), resizable=True)


def video_download():
    title = 'Download Video'
    layout = [
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Frame('', [
            [
                Sg.T('Coloque a Url: '),
                Sg.In(key='url-site', expand_x=True),
                Sg.B(image_data=convert_to_bytes('icones/download_video.png', (40, 50)), key='baixar_video')
            ]
        ], expand_x=True)],
        [Sg.Frame('', [
            [Sg.Push(), Sg.Im(key='img_v', size=(400, 400)), Sg.Push()]
        ], expand_x=True)]
    ]
    return Sg.Window('', layout, finalize=True, location=(1369, 0))


def relogio():
    title = 'Relogio'
    layout =[
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Push(), Sg.Text('', key='horas', font='Any 33'), Sg.Push()],
        [Sg.T('', key='data', font='Any 18')]
    ]

    return Sg.Window('Horas e Data', layout, finalize=True, location=(959, 0), resizable=True)


def registro():
    headings = ['Site download', 'Nome do Arquivo', 'horas']
    title = 'Registros de Downloads'
    layout = [
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [
            Sg.Table(values=[], headings=headings,
                     auto_size_columns=True,
                     # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                     justification='center',
                     # col_widths=[60, 60],
                     # num_rows=15,
                     # alternating_row_color='purple',
                     key='-TABLE-',
                     # selected_row_colors='red on yellow',
                     enable_events=True,
                     expand_x=True,
                     expand_y=True,
                     # vertical_scroll_only=False,
                     # enable_click_events=True,  # Comment out to not enable header and other clicks
                     tooltip='Registro de Download')],
    ]
    return Sg.Window('', layout, finalize=True, location=(959, 614), resizable=True)


def pegarfrase():
    r = [t.tema for t in Reflexao.select()]
    ale = choices(r, k=len(r) - 1)
    n = choice(ale)
    tf = [i.texto for i in Pensamento.select().join(Reflexao).where(Reflexao.tema == f'{n}')]

    return n, choice(tf)


def reflexao():
    tit, frase = pegarfrase()
    temas_site = [t.tema for t in Reflexao.select()]
    title = 'Reflexão'
    Frase = [
        [Sg.Push(), Sg.T(tit, justification='c', font='Any 14', key='tt_frase'), Sg.Push()],
        [Sg.Push(), Sg.T(frase, size=(40, 20), pad=(1,2), justification='c', font='Any 14', key='frase'), Sg.Push()],
        [Sg.VPush()],
        [Sg.Push(), Sg.B('Reflexão'), Sg.Push()]
    ]
    Conf_frase = [
        [Sg.T('Tema da Frase: '), Sg.In(key='t_frase')],
        [Sg.T('Download do Site https://www.pensador.com/')],
        [Sg.Push(), Sg.Combo(values=temas_site, enable_events=True, p=(5, 10), key='list_tema'), Sg.Push()],
        [Sg.VPush()],
        [Sg.Push(), Sg.T('', key='complete'), Sg.Push()],
        [Sg.Push(), Sg.B('Download'), Sg.Push()]
    ]

    layout = [
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.TabGroup([[Sg.Tab('Reflexão', Frase), Sg.Tab('Frase do Site', Conf_frase)]])]

    ]
    return Sg.Window('', layout, finalize=True, location=(961, 170))


def save_config():
    title = 'Configuração dos Sites'
    layout = [
        # [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Push(), Sg.T('Add Site ao Banco de Dados'), Sg.Push()],
        [Sg.T('Site '), Sg.In(key='lsite')],
        [Sg.T('Url 1'), Sg.In(key='lurl1')],
        [Sg.T('Img 1'), Sg.In(key='limg1')],
        [Sg.T('Img 2'), Sg.In(key='limg2')],
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/save_db.jpg', (40, 40)), key='save_db'), Sg.Push()]
    ]
    return Sg.Window('', layout, finalize=True, location=(1474, 447))


def clima():
    col1 = Sg.Col([
        [Sg.Im('icones/tempo/Temperature.png'), Sg.T('Max/Min'), Sg.Push(), Sg.T(key='maxmin')],
        [Sg.Im('icones/tempo/Humidity.png'), Sg.T('Umidade'), Sg.Push(), Sg.T(key='umidade')],
        [Sg.Im('icones/tempo/Pressure.png'), Sg.T('Pressão'), Sg.Push(), Sg.T(key='pressao')],
        [Sg.Im(convert_to_bytes('icones/tempo/Visibility.png', (24, 24))), Sg.T('Vísibilidade'), Sg.Push(),
            Sg.T(key='visib')]
    ])
    col2 = Sg.Col([
        [Sg.Im('icones/tempo/Wind.png'), Sg.T('Vento'), Sg.Push(), Sg.T(key='vento')],
        [Sg.Im('icones/tempo/Dew Point.png'), Sg.T('P. de Orvalho'), Sg.Push(), Sg.T(key='p_orv')],
        [Sg.Im('icones/tempo/UV Level.png'), Sg.T('Indice UV'), Sg.Push(), Sg.T(key='uv')],
        [Sg.Im('icones/tempo/Moon Phase.png'), Sg.T('Fase da Lua'), Sg.Push(),
            Sg.T(key='f_lua')]
    ])
    layout = [
        [Sg.T(key='clima')],
        [Sg.T(key='temp', font='Any 38'), Sg.Push(), Sg.Im(convert_to_bytes('icones/tempo/semi-circulo-rosa.webp', (140, 100)))],
        [
            Sg.T(key='sens'),
            Sg.Push(),
            Sg.Im(filename='icones/tempo/Sun Rise.png'),
            Sg.T(key='nasce'),
            Sg.Im(filename='icones/tempo/Sunset.png'),
            Sg.T(key='morre')],
        [col1,col2]
    ]
    return Sg.Window('Clima e Tempo', layout, finalize=True)