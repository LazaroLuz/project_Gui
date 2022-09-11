from PIL import Image
import asyncio
import os
import shutil


def Pdf(pasta, nome, lista_foto):
    cwd = os.getcwd()
    try:
        os.chdir(pasta)

        imagem1 = Image.open(lista_foto[0]).convert('RGB')

        del lista_foto[0]
        imgs = []
        for img in lista_foto:
            fot = Image.open(img).convert("RGB")
            imgs.append(fot)

        imagem1.save(f"../{nome}.pdf", save_all=True, append_images=imgs)
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    finally:
        os.chdir(cwd)


async def pdf(base, pasta, titulo, lista_foto):
    print(f'{base}/{titulo}')
    imagem1 = Image.open(os.path.join(pasta, lista_foto[0])).convert('RGB')

    del lista_foto[0]
    imgs = []
    for img in lista_foto:
        fot = Image.open(os.path.join(pasta, img)).convert("RGB")
        imgs.append(fot)

    imagem1.save(f"{base}/{titulo}.pdf", save_all=True, append_images=imgs)

