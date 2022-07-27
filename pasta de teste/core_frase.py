import httpx
from bs4 import BeautifulSoup as Bs
import unidecode


def frase_de_reflexao(nome):
    base_url = 'https://www.pensador.com/'
    n = unidecode.unidecode(nome)
    n = n.lower()
    n = n.replace(' ', '_')
    books: list = []
    for i in range(1, 2):  # 36
        if i == 1:
            url = f'{base_url}{n}/'
        else:
            url = f'{base_url}{n}/{i}/'
        response = httpx.get(url)
        soup = Bs(response.text, 'html5lib')
        texto = soup.select('p.frase.fr')
        for txt in texto:
            print(txt.getText())


frase_de_reflexao('Frases de Pensadores Importantes')

