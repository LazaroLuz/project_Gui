import json
import os

import youtube_dl
import requests
from bs4 import BeautifulSoup as BS


url_x = 'https://www.xvideos.com/video63347751/madrasta_precisa_de_ajuda_para_tirar_fotos_sujas_-_brianna_beach_-_mamae_vem_primeiro_-_alex_adams'
url_nx = 'https://www.xnxx.com/video-z6vqxa5/petite_ebony_chanel_skye_faz_anal_depois_da_massagem'
url_p = 'https://pt.pornhub.com/view_video.php?viewkey=ph5f483ea43bcb5'


def down(name, urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{name}.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([urls])


def download_videos(url):
    response = requests.get(url)
    soup = BS(response.text, 'html5lib')
    # script = soup.find_all('script')
    script = soup.find("script", type="application/ld+json")
    resultado = str(script)
    reslt = resultado.split('>')[1].split('<')[0]

    js = json.loads(reslt)
    if type(js['thumbnailUrl']) == list:
        foto = js['thumbnailUrl'][0]
    else:
        foto = js['thumbnailUrl']
    print(foto)
    try:
        if js['contentUrl']:
            down(js['name'], js['contentUrl'])
    except KeyError:
        down(js['name'], js['embedUrl'])


download_videos(url_x)


# with youtube_dl.YoutubeDL() as ydl:
#     ydl.download(['https://pt.pornhub.com/embed/ph5f483ea43bcb5'])


