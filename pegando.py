from models import Reflexao, Pensamento
from random import randint

r = [t.tema for t in Reflexao.select()]
n = randint(0, len(r)-1)
print(n)
print(r[n])
t = Pensamento.select().where(Pensamento.reflexao_id == r[0]).get()
print(t[0])
