import time
import sched
from models import Comics, Reflexao, Pensamento
from random import randint, choice, choices
import schedule


def pegarfrase():
    r = [t.tema for t in Reflexao.select()]
    ale = choices(r, k=len(r)-1)
    n = choice(ale)
    tf = [i.texto for i in Pensamento.select().join(Reflexao).where(Reflexao.tema == f'{n}')]
    # n2 = randint(0, len(tf)-1)
    print(ale)
    print(r)
    print(n)
    print(choice(tf))


# schedule.every(10).minutes.do(pegarfrase)
# while True:
#     # Checks whether a scheduled task
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)


#
# # instance is created
# scheduler = sched.scheduler(time.time, time.sleep)
#
# # function to print time
# # and name of the event
# def print_event(name):
# 	print('EVENT:', time.time(), name)
#
# # printing starting time
# print ('START:', time.time())
#
# # first event with delay of
# # 1 second
# e1 = scheduler.enter(5, 3, print_event, ('1 st', ))
#
# # second event with delay of
# # 2 seconds
# e1 = scheduler.enter(5, 2, pegarfrase)
# #
# # # executing the events
# scheduler.run()

# comics = Comics.select().where(Comics.site_name == "https://hqerotico.com/").get()
# print(comics.seletor_link)
import datetime



while True:
    now = datetime.datetime.now().second
    time.sleep(1)
    if now == 00:
        pegarfrase()
    else:
        print(now)

