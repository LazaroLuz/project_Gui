import json
import os

import youtube_dl
import requests
from bs4 import BeautifulSoup as BS

import converte


def down(name, urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{name}.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([urls])


def download_videos(janela, url):
    response = requests.get(url)
    soup = BS(response.text, 'html5lib')

    script = soup.find("script", type="application/ld+json")
    resultado = str(script)
    reslt = resultado.split('>')[1].split('<')[0]

    js = json.loads(reslt)
    if type(js['thumbnailUrl']) == list:
        foto = js['thumbnailUrl'][0]
    else:
        foto = js['thumbnailUrl']
    r = requests.get(foto).content
    janela['img_v'].update(converte.convert_to_bytes(r, (300, 300)))
    try:
        if js['contentUrl']:
            down(js['name'], js['contentUrl'])
    except KeyError:
        down(js['name'], js['embedUrl'])
    janela['baixar_video'].update(disabled=False)
    janela['url-site'].update('')


