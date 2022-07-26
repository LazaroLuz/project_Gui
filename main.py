import datetime
import locale

from base import *
from converte import convert_to_bytes


def main():
    layout =[
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
    return Sg.Window('Projeto', layout, keep_on_top=True, finalize=True, location=(0, 773), no_titlebar=True)


janela, janela_foto, janela_video, janela_relogio, janela_registro, janela_reflexao, janela_conf = main(), None, None, None, None, None, None

while True:
    windows, event, values = Sg.read_all_windows(timeout=60)

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
        janela_foto = foto_to_pdf()
        print(janela_foto.get_screen_dimensions())
    elif event == '2':
        janela_video = video_download()

    elif event == '3':
        janela_relogio = relogio()

    elif event == '4':
        janela_registro = registro()

    elif event == '5':
        janela_reflexao = reflexao()

    elif event == '6':
        janela_conf = save_config()

    elif event == 'exit':
        print(windows.current_location())
        windows.close()

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
