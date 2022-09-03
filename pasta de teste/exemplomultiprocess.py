import PySimpleGUI as Sg
from multiprocessing import Process


def button_layout(nome, row, col):
    layout = [

        [Sg.B(nome[r][c], size=(10, 10))for c in range(col)]for r in range(row)

    ]
    window = Sg.Window('Microprocessing Example', layout,  element_justification='center',
                        finalize=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event == Sg.WIN_CLOSED:
            break

    window.close()


def backgroud(nome):
    row, col = 3, 3
    lay = [[]]
    for i in range(row):
        btn = []
        txt = []
        for j in range(col):
            print(nome[i][j])
            btn.append(Sg.Button('', size=(10, 10), key=(i, j), pad=(0, 0), enable_events=True))
            txt.append(Sg.T(nome[i][j], size=(10, 1), justification='c', p=(0,0)))

        lay.append(btn)
        lay.append(txt)
    # layout = [[Sg.Column(lay, scrollable=True)]]
    window = Sg.Window('teste', lay, finalize=True)
    while True:
        event, values = window.read()
        print(event, values)
        if event == Sg.WIN_CLOSED:
            break

    window.close()


def sub_list(biglista, sublista):
    qty_el = len(biglista)

    for i in range(0, qty_el, sublista):
        # Create an index range for l of n items:
        yield biglista[i:i + sublista]


frutas: list = ['maça', 'pera', 'uva', 'laranja', 'morango', 'banana', 'ameixa', 'amora', 'péssego', 'abacaxi', 'mamão', 'melancia', '']
me = sub_list(frutas, 3)
m = [i for i in me]
p1 = Process(target=backgroud, args=(m,))

p2 = Process(target=button_layout, args=(m, 3, 3))



if __name__ == '__main__':
    p1.start()
    p2.start()
