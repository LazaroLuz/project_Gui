import time
import sched
from models import Comics, Reflexao, Pensamento
from random import randint
import schedule


def pegarfrase():
    r = [t.tema for t in Reflexao.select()]
    n = randint(0, len(r)-1)
    t = Pensamento.select().join(Reflexao).where(Reflexao.tema == f'{r[n]}')
    n2 = randint(0, len(t)-1)
    print(t[n2].texto)


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
#
# # executing the events
# scheduler.run()

comics = Comics.select().where(Comics.site_name == "https://hqerotico.com/").get()
print(comics.seletor_link)
