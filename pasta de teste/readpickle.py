import pickle
import PySimpleGUI as Sg
from converte import convert_to_bytes


with open('revista.pkl', 'rb') as arquivo:
    lista_revista = pickle.load(arquivo)
ordenado = [lr['titulo']for lr in lista_revista]
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
        num = ordenado.index(values['titulo'])
        rev = [ft['fotos'] for ft in lista_revista]

        janela['IMAGE'].update(data=convert_to_bytes(rev[num][0], (800, 900)))
    if event == 'Ir' or event == 'Right:39':

        if i >= len(rev) - 1:
            i = 0
        else:
            i += 1
        janela['IMAGE'].update(data=convert_to_bytes(rev[num][i], (800, 900)))
    #
    if event == 'Voltar' or event == 'Left:37':
        if i == 0:
            i = len(rev) - 1
        else:
            i -= 1

        janela['IMAGE'].update(data=convert_to_bytes(rev[num][i], (800, 900)))


janela.close()
