import PySimpleGUI as Sg
from converte import convert_to_bytes


Sg.theme('Darkblue6')


def foto_to_pdf():
    layout =[
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [Sg.Frame('', [
            [
                Sg.T('Coloque a Url: '),
                Sg.In(key='url-site', expand_x=True),
                Sg.B(image_data=convert_to_bytes('icones/download.png', (40, 50)), key='baixar_revista')
            ]
        ], expand_x=True)],
        [Sg.Push(), Sg.T('', key='titulo'), Sg.Push()],
        [Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='capa')]
        ]), Sg.Im(data=convert_to_bytes('icones/setas.png', (80, 80))), Sg.Frame('', [
            [Sg.Im(size=(400, 600), key='revista')]
        ])]
    ]
    return Sg.Window('', layout, finalize=True, location=(0, 0), no_titlebar=True)


def video_download():
    layout = [
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [Sg.Frame('', [
            [
                Sg.T('Coloque a Url: '),
                Sg.In(key='url-site', expand_x=True),
                Sg.B(image_data=convert_to_bytes('icones/download_video.png', (40, 50)), key='baixar_video')
            ]
        ], expand_x=True)],
        [Sg.Frame('', [
            [Sg.Im(key='img_v', size=(300, 300))]
        ], expand_x=True)]
    ]
    return Sg.Window('', layout, finalize=True, location=(1369, 0), no_titlebar=True)


def relogio():
    layout =[
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [Sg.Push(), Sg.Text('', key='horas', font='Any 33'), Sg.Push()],
        [Sg.T('', key='data', font='Any 18')]
    ]

    return Sg.Window('Horas e Data', layout, finalize=True, location=(959, 0), no_titlebar=True)


def registro():
    headings = ['Site download', 'Nome do Arquivo', 'horas']
    layout = [
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [
            Sg.Table(values=[['www.quadrinhoseroticos.blog', 'ESPOSA ORIENTAL VIDA OCIDENTAL 1', '11:04:00']], headings=headings,
                     auto_size_columns=True,
                     # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                     justification='center',
                     col_widths=[60, 60],
                     num_rows=15,
                     alternating_row_color='purple',
                     key='-TABLE-',
                     selected_row_colors='red on yellow',
                     enable_events=True,
                     expand_x=True,
                     expand_y=True,
                     # vertical_scroll_only=False,
                     # enable_click_events=True,  # Comment out to not enable header and other clicks
                     tooltip='Registro de Download')],
    ]
    return Sg.Window('', layout, finalize=True, location=(959, 614), no_titlebar=True)


def reflexao():
    layout = [
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [Sg.T('Muitas vezes ri dos fracotes que se creem bons porque têm patas aleijadas!',
                size=(40, 20), justification='c', font='Any 12', key='frase')]
    ]
    return Sg.Window('', layout, finalize=True, location=(961, 170), no_titlebar=True)


def save_config():
    layout = [
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/exit.png', (20, 20)), key='exit')],
        [Sg.Push(), Sg.T('Add Site ao Banco de Dados'), Sg.Push()],
        [Sg.T('Site '), Sg.In(key='lsite')],
        [Sg.T('Url 1'), Sg.In(key='lurl1')],
        [Sg.T('Url 2'), Sg.In(key='lurl2')],
        [Sg.T('Img 1'), Sg.In(key='limg1')],
        [Sg.T('Img 2'), Sg.In(key='limg2')],
        [Sg.T('Next '), Sg.In(key='lnext')],
        [Sg.Push(), Sg.B('', image_data=convert_to_bytes('icones/save_db.jpg', (40, 40)), key='save_db'), Sg.Push()]
    ]
    return Sg.Window('', layout, finalize=True, location=(1474, 447), no_titlebar=True)
