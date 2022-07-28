from PIL import Image
import os
import shutil


def Pdf(pasta, nome, lista_foto):
    os.chdir(pasta)
    imagem1 = Image.open(lista_foto[0])
    img1 = imagem1.convert('RGB')
    del lista_foto[0]
    imgs = []
    for img in lista_foto:
        fot = Image.open(img)
        if fot.mode == "RGBA":
            fot = fot.convert('RGB')
        imgs.append(fot)

    imagem1.save(f"../{nome}.pdf", save_all=True, format="pdf", append_images=imgs)
    os.chdir(f'../../')
    shutil.rmtree(pasta)



