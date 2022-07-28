# models.py

import peewee

# Criamos o banco de dados
db = peewee.SqliteDatabase('P_gui.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = db


class Comics(BaseModel):
    """
    Classe que representa a tabela Author
    """
    # A tabela possui apenas o campo 'name', que receberá o nome do autor sera unico
    site_name = peewee.CharField(unique=True)
    seletor_link = peewee.CharField()
    seletor_img_1 = peewee.CharField()
    seletor_img_2 = peewee.CharField()


class Reflexao(BaseModel):
    tema = peewee.CharField(unique=True)


class Pensamento(BaseModel):
    texto = peewee.CharField()
    reflexao = peewee.ForeignKeyField(Reflexao)


if __name__ == '__main__':
    try:
        Comics.create_table()
        Reflexao.create_table()
        Pensamento.create_table()
        print("Tabelas criada com sucesso!")
    except peewee.OperationalError:
        print("Tabelas  ja existente!")
