import math

def maior_nquestoes(body):
    lista = []
    c = 0
    while c < len(body):
        lista.append(len(body[c]))
        c = c + 1
    return max(lista) - 1

def qtd_colunas(body):

    lista = []
    c = 0
    while c < len(body):
        lista.append(len(body[c]))
        c = c + 1

    print(max(lista))    
    y = max(lista)

    lista_colunas = ["prova varchar(20)"]
    for c in range(1, y):
        x = 'quest_' + str(c) + ' varchar(20)'
        lista_colunas.append(x)
    colunas = str(tuple(lista_colunas)).replace("'", "")
    return colunas

def qtd_colunas2(numero):
    lista_colunas = ["prova varchar(20)"]
    for c in range(1, numero):
        x = 'quest_' + str(c) + ' varchar(20)'
        lista_colunas.append(x)
    colunas = str(tuple(lista_colunas)).replace("'", "")
    return colunas

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

print(truncate(1.3333333333333333333, 2))