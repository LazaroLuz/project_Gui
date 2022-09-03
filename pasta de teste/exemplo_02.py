# import PySimpleGUI as sg
#
# """
#     Demonstrates how to use the Window.layout_extend method.
#     Layouts can be extended at the Window level or within any container element such as a Column.
#     This demo shows how to extend both.
#     Note that while you can extend, add to, a layout, you cannot delete items from a layout.  Of course you
#     can make them invisible after adding them.
#
#     When using scrollable Columns be sure and call Column.visibility_changed so that the scrollbars will
#         be correctly reposititioned
#
#     Copyright 2020, 2022 PySimpleGUI
# """
#
# layout = [[sg.Text('My Window')],
#           [sg.Text('Click to add a row inside the Frame'), sg.B('+', key='-ADD FRAME-')],
#           [sg.Text('Click to add a row inside the Column'), sg.B('+', key='-ADD COL-')],
#           [sg.Text('Click to add a row inside the Window'), sg.B('+', key='-ADD WIN-')],
#           [sg.Frame('Frame', [[sg.T('Frame')]], key='-FRAME-')],
#           [sg.Col([[sg.T('Column')]], scrollable=True, key='-COL-', s=(400, 400))],
#           [sg.Input(key='-IN-'), sg.Text(size=(12, 1), key='-OUT-')],
#           [sg.Button('Button'), sg.Button('Exit')]]
#
# window = sg.Window('Window Title', layout)
#
# i = 0
#
# while True:  # Event Loop
#     event, values = window.read()
#     print(event, values)
#     if event in (sg.WIN_CLOSED, 'Exit'):
#         break
#     if event == '-ADD FRAME-':
#         window.extend_layout(window['-FRAME-'], [[sg.T('A New Input Line'), sg.I(key=f'-IN-{i}-')]])
#         i += 1
#     elif event == '-ADD COL-':
#         window.extend_layout(window['-COL-'], [[sg.T('A New Input Line'), sg.I(key=f'-IN-{i}-')]])
#         window.visibility_changed()
#         window['-COL-'].contents_changed()
#         i += 1
#     elif event == '-ADD WIN-':
#         window.extend_layout(window, [[sg.T('A New Input Line'), sg.I(key=f'-IN-{i}-')]])
#         i += 1
# window.close()

import PySimpleGUI as sg

num_buttons = 1
layout = [[sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_')],
            [sg.Input(do_not_clear=True, key='_IN_')],
            *[[sg.Button('Button'),] for i in range(num_buttons)],
            [sg.Button('Add Rows'), sg.Button('Delete Rows' ), sg.Button('Exit')]]

location = (600,600)
window = sg.Window('Window Title', location=location).Layout(layout)


num_buttons = 1
while True:             # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Add Rows' or event == 'Delete Rows':
        num_buttons += -1 if event == 'Delete Rows' else 1

        layout = [[sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_')],
                    [sg.Input(do_not_clear=True, key='_IN_')],
                    *[[sg.Button('Button'),] for i in range(num_buttons)],
                  [sg.Button('Add Rows'), sg.Button('Delete Rows'), sg.Button('Exit')]]
        window1 = sg.Window('Window Title', location=location).Layout(layout)
        window.Close()
        window = window1

window.Close()
