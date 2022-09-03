import base64
import os
from PIL import Image  # type: ignore
import asyncio


async def pdf(pasta, titulo, lista_foto):
    # lista_foto = [arq for arq in os.listdir('pasta de teste/past/')]
    # print(lista_foto)

    imagem1 = Image.open(os.path.join(pasta, lista_foto[0])).convert('RGB')

    del lista_foto[0]
    imgs = []
    for img in lista_foto:
        fot = Image.open(os.path.join(pasta, img)).convert("RGB")
        imgs.append(fot)

    imagem1.save(f"{titulo}.pdf", save_all=True, append_images=imgs)


async def main():
    pasta = 'pasta de teste/past/'
    lista_foto = [arq for arq in os.listdir(pasta)]
    print(lista_foto)
    titulo = 'sogro'
    await pdf(pasta, titulo, lista_foto)
    # await asyncio.gather(
    #     pdf(), return_exceptions=False
    # )

asyncio.run(main())
# with open('pasta de teste/past/01-1-9.jpg', 'rb') as file:
#     data = file.read()
#     # encod = base64.b16encode(data)
#     encod = base64.encodebytes(data)
    # print(encod)
# with open('teste.png', 'wb') as f:
#     decod = base64.b16decode(encod)
#     f.write(decod)