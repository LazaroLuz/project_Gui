import peewee  # type: ignore

# Criamos o banco de dados
db = peewee.SqliteDatabase('comics.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = db


class Site(BaseModel):
    name = peewee.CharField(unique=True)


class Revista(BaseModel):
    """
    Classe que representa a tabela Author
    """
    # A tabela possui apenas o campo 'name', que receberá o nome do autor sera unico
    name = peewee.CharField(unique=True)
    site = peewee.ForeignKeyField(Site)


class Imagens(BaseModel):
    fotos = peewee.CharField()
    allporn = peewee.ForeignKeyField(Revista)


if __name__ == '__main__':
    try:
        Site.create_table()
        Revista.create_table()
        Imagens.create_table()
        print('tabelas criadas com sucesso')
    except peewee.OperationalError:
        print('tabelas já criadas')
