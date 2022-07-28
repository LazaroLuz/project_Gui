import PySimpleGUI as Sg
from converte import convert_to_bytes


DarkGrey8 = {'BACKGROUND': '#19232D',
              'TEXT': '#ffffff',
              'INPUT': '#32414B',
              'TEXT_INPUT': '#ffffff',
              'SCROLL': '#505F69',
              'BUTTON': ('#ffffff', '#32414B'),
              'PROGRESS': ('#505F69', '#32414B'),
              'BORDER': 1, 'SLIDER_DEPTH': 2, 'PROGRESS_DEPTH': 2,
              }

Sg.theme_add_new('DarkGrey8', DarkGrey8)

Sg.theme('DarkGrey8')


def foto_to_pdf():
    title = 'Foto Para Pdf'
    layout =[
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Frame('', [
            [
                Sg.T('Coloque a Url: '),
                Sg.In(key='url-site', expand_x=True),
                Sg.B(image_data=convert_to_bytes('icones/download.png', (40, 50)), key='baixar_revista')
            ],
            [Sg.T('Numero de Pagínas'), Sg.Spin(values=[i for i in range(1, 150)], initial_value=1, size=(6, 1), key='n_pag')]
        ], expand_x=True)],
        [Sg.Push(), Sg.T('', key='titulo', font='Any 20', text_color='#ffffff'), Sg.Push()],
        [Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='capa')]
        ]), Sg.Im(data=convert_to_bytes('icones/setas.png', (80, 80))), Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='revista')]
        ])]
    ]
    return Sg.Window('', layout, finalize=True, location=(0, 0))


def video_download():
    title = 'Download Video'
    layout = [
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
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
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Push(), Sg.Text('', key='horas', font='Any 33'), Sg.Push()],
        [Sg.T('', key='data', font='Any 18')]
    ]

    return Sg.Window('Horas e Data', layout, finalize=True, location=(959, 0))


def registro():
    headings = ['Site download', 'Nome do Arquivo', 'horas']
    title = 'Registros de Downloads'
    layout = [
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
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
    return Sg.Window('', layout, finalize=True, location=(959, 614))


def reflexao():
    temas_site = [
        'Frases de Pensadores Importantes', 'Mensagens de Reflexão', 'Frases de Motivação', 'Frases Curtas',
    'Frases de Vida', 'Frases de Amizade', 'Frases Inteligentes', 'Frases para Refletir', 'Frases Curtas de Sabedoria',
    'Provérbio Chinês de Sabedoria', 'Sexo', 'Ousadia', 'Ódio', 'Frases de Quem Sou Eu'
    ]
    title = 'Reflexão'
    Frase = [
        [Sg.Push(), Sg.T('', size=(40, 20), justification='c', font='Any 14', key='frase'), Sg.Push()],
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
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.TabGroup([[Sg.Tab('Reflexão', Frase), Sg.Tab('Frase do Site', Conf_frase)]])]

    ]
    return Sg.Window('', layout, finalize=True, location=(961, 170))


def save_config():
    title = 'Configuração dos Sites'
    layout = [
        [Sg.Titlebar(title, Sg.CUSTOM_TITLEBAR_ICON)],
        [Sg.Push(), Sg.T('Add Site ao Banco de Dados'), Sg.Push()],
        [Sg.T('Site '), Sg.In(key='lsite')],
        [Sg.T('Url 1'), Sg.In(key='lurl1')],
        [Sg.T('Img 1'), Sg.In(key='limg1')],
        [Sg.T('Img 2'), Sg.In(key='limg2')],
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/save_db.jpg', (40, 40)), key='save_db'), Sg.Push()]
    ]
    return Sg.Window('', layout, finalize=True, location=(1474, 447))
