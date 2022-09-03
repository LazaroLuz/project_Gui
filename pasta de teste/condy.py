# import base64
#
# import httpx
#
# file = 'https://cdn.allporncomic.com/wp-content/uploads/WP-manga/data/manga_5eb5b169ec3ae/e96fc17d2a55f6d4eb0a44e3dfed03fe/000.jpg'
# head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
#
# r = httpx.get(file, headers=head)
# data = r.content
# print(data)
# with open('file.jpg', 'wb') as f:
#     f.write(data)

import json

with open('personagem.json', 'r') as data:
    load = json.load(data)
    print(load['revista'][0]['title'])
    print(load['revista'][0]['Fotos'][0])