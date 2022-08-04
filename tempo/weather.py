import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests


def get_weather_data(location):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    url = f'https://www.google.com/search?q=weather+{location.replace(" ", "")}'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    html = session.get(url)

    # create a new soup
    soup = bs(html.text, "html.parser")
    name = soup.find("div", attrs={'id': 'wob_loc'}).text
    time = soup.find("div", attrs={'id': 'wob_dts'}).text
    weather = soup.find("span", attrs={'id': 'wob_dc'}).text
    temp = soup.find("span", attrs={'id': 'wob_tm'}).text
    return name, time, weather, temp


weather_column = sg.Column([
    [sg.Image('', key='-IMAGE-', background_color='#FFFFFF', )]],
    key='-LEFT-',
    background_color='#FFFFFF')

info_column = sg.Column([
    [sg.Text('', key='-LOCATION-', font='Calibri 30', background_color='#FF0000', pad=0, visible=False)],
    [sg.Text('', key='-TIME-', font='Calibri 16', background_color='#000000', text_color='#FFFFFF', pad=0,
             visible=False)],
    [sg.Text('', key='-TEMP-', font='Calibri 16', pad=(0, 10), background_color='#FFFFFF', text_color='#000000',
             justification='center', visible=False)]
], key='-RIGHT-',
    background_color='#FFFFFF')

main_layout = [
    [sg.Input(key='-INPUT-', expand_x=True), sg.Button('submit', button_color='#000000')],
    [weather_column, info_column]
]

sg.theme('reddit')
window = sg.Window('Weather', main_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'submit':
        name, time, weather, temp = get_weather_data(values['-INPUT-'])

        window['-LOCATION-'].update(name, visible=True)
        window['-TIME-'].update(time.split(' ')[0], visible=True)
        window['-TEMP-'].update(f'{temp} \u2103 ({weather})', visible=True)

        # sun
        if weather in ('Sol', 'Ensolarado', 'Claro', 'Claro com nuvens periódicas', 'Principalmente ensolarado'):
            window['-IMAGE-'].update('symbols/sun.png')

        # part sun
        if weather in ('Parcialmente ensolarado', 'Muito ensolarado', 'Parcialmente nublado', 'Muito nublado', 'Nublado'):
            window['-IMAGE-'].update('symbols/part sun.png')

        # rain
        if weather in ('Chuva', 'Chance de Chuva', 'Chuva leve', 'chuveiros', 'chuveiros dispersos', 'chuva e neve', 'granizo'):
            window['-IMAGE-'].update('symbols/rain.png')

        # thunder
        if weather in ('Tempestades dispersas', 'Chance de tempestade', 'Tempestade', 'Chance of TStorm'):
            window['-IMAGE-'].update('symbols/thunder.png')

        # foggy
        if weather in ('Névoa', 'Poeira', 'Névoa', 'Fumaça', 'Névoa', 'Rajadas'):
            window['-IMAGE-'].update('symbols/fog.png')

        # snow
        if weather in ('Garoa congelante', 'Chance de Neve', 'Granizo', 'Neve', 'Gelo', 'Chuvas de neve'):
            window['-IMAGE-'].update('symbols/snow.png')

window.close()