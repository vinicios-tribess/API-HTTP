import math

def analisar(N):
    for i in N:
        if 1 <= i <= 100:
            lista = []
            lista.append(i)
        else:
            return False

def analisar2(na, x):
    for i in range(0, len(na)):
        if x != na[i]:
            lista = []
            lista.append(i)
        else:
            return False

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
