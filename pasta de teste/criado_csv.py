import csv


# with open('teste.csv', 'a+') as csvfile:
#     for i in range(10):
#         csv.writer(csvfile, delimiter=',').writerow(['João', '30'])

with open('historico.csv') as csvfile:
    for x in csv.reader(csvfile):
        if x:
            print(x)
