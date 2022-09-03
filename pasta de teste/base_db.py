import peewee  # type: ignore

# Criamos o banco de dados
db = peewee.SqliteDatabase('quadrinho.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = db


# class Allporn(BaseModel):
#     """
#     Classe que representa a tabela Author
#     """
#     # A tabela possui apenas o campo 'name', que receberá o nome do autor sera unico
#     name = peewee.CharField()
#
#
# class Photo(BaseModel):
#     fotos = peewee.CharField(unique=True)
#     allporn = peewee.ForeignKeyField(Allporn)


class Quadrinho(BaseModel):
    """
    Classe que representa a tabela Author
    """
    # A tabela possui apenas o campo 'name', que receberá o nome do autor sera unico
    name = peewee.CharField()


class Imagens(BaseModel):
    fotos = peewee.CharField()
    allporn = peewee.ForeignKeyField(Quadrinho)


if __name__ == '__main__':
    try:
        Quadrinho.create_table()
        Imagens.create_table()
        print('tabelas criadas com sucesso')
    except peewee.OperationalError:
        print('tabelas já criadas')
