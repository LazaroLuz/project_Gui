import httpx
from bs4 import BeautifulSoup as Bs
from models import Reflexao, Pensamento
import unidecode


def frase_de_reflexao(janela, nome):
    try:
        base_url = 'https://www.pensador.com/'
        author_1 = Reflexao.create(tema=f'{nome}')
        n = unidecode.unidecode(nome)
        n = n.lower()
        n = n.replace(' ', '_')
        books: list = []
        for i in range(1, 50):  # 36
            if i == 1:
                url = f'{base_url}{n}/'
            else:
                url = f'{base_url}{n}/{i}/'
            response = httpx.get(url)
            soup = Bs(response.text, 'html5lib')
            texto = soup.select('p.frase.fr')
            for txt in texto:
                book = {
                    'texto': txt.getText(),
                    'reflexao_id': author_1
                }
                books.append(book)
        Pensamento.insert_many(books).execute()
        janela['complete'].update('Download Realizado com Sucesso')
        janela['t_frase'].update('')
        janela['Download'].update(disabled=False)
    except:
        janela['complete'].update('Tema já baixado')
        janela['Download'].update(disabled=False)




