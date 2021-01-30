'''import json

with open('input_respostas2.json', 'r') as json_file:
    gabarito = json.load(json_file)'''
import json

a = [(1, 'Maria Aparecida', 2.9), (2, 'Pedro Eduardo', 0.0), (3, 'Ana Beatriz', 0.0)]

lista = []
for item in a:
    dic = {"id_aluno": item[0], "nome": item[1], "nota": item[2]}
    lista.append(dic)

json = json.dumps(lista, indent=3)

print(json)

# dic = {"id_aluno": x[0], "nome": x[1], "nota": x[2]}

# print(json.dumps(str(dic), indent=3))

try:
    x = 0 / 0
finally:
    print("Erro")

