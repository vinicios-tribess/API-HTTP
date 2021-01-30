import sqlite3
from collections import OrderedDict
from itertools import zip_longest
import json

banco = sqlite3.connect('Escola_Alf.db')

cursor = banco.cursor()

# Separa uma lista com as IDs dos alunos, outra com os nomes e outra com as provas:

cursor.execute("select * from alunos ORDER BY id_aluno, aluno")

dados = cursor.fetchall()

lista_IDs = []
for c in dados:
    x = c[0]
    lista_IDs.append(x)

lista_nomes = []
for c in dados:
    x = c[1]
    lista_nomes.append(x)

cursor.execute("select * from respostas ORDER BY id_aluno, aluno, prova, questao")

dados = cursor.fetchall()

lista_provas = []
for c in dados:
    x = c[2]
    lista_provas.append(x)

lista_provas = list(OrderedDict(zip_longest(lista_provas, [])))

cursor.execute("DROP TABLE IF EXISTS notas_finais")

for i in range(1, (len(lista_IDs) + 1)):
    lista_notas = []
    for p in range(1, (len(lista_provas) + 1)):

        # Separa todas as alternativas corretas de uma prova:

        banco = sqlite3.connect('Escola_Alf.db')

        cursor = banco.cursor()
        
        cursor.execute("SELECT * FROM gabaritos WHERE prova = " + str(p))

        dados = cursor.fetchall()

        lista1 = []
        for item in dados:
            dado = item[2]
            lista1.append(dado)

        tamanho = len(lista1)

        # Separa os pesos de uma prova:

        cursor.execute("SELECT * FROM gabaritos WHERE prova = " + str(p))

        dados = cursor.fetchall()

        lista2 = []
        for item in dados:
            dado = item[3]
            lista2.append(dado)

        # Separa as alternativas de um aluno para uma prova:

        cursor.execute("SELECT * FROM respostas WHERE id_aluno = " + str(i) + " and prova = " + str(p))

        dados = cursor.fetchall()

        lista3 = []
        for item in dados:
            dado = item[4]
            lista3.append(dado)

        # Separa a pontuação:

        lista4 = []
        for c in range(0, tamanho):
            if lista1[c] == lista3[c]:
                lista4.append(lista2[c])
            elif lista3[c] == "":
                lista4.append(0)
            else:
                lista4.append(0)

        soma_dos_pesos = sum(lista4)

        nota = round(float((soma_dos_pesos / sum(lista2)) * 10), 2)

        lista_notas.append(nota)

    soma_das_notas = sum(lista_notas)

    qtd_de_provas = len(lista_notas)

    media_final = soma_das_notas / qtd_de_provas

    cursor.execute("CREATE TABLE IF NOT EXISTS notas_finais (id_aluno integer not null check(id_aluno between 1 AND 100), aluno text not null, nota real not null)")

    dados_inseridos = str(( i, lista_nomes[i - 1], media_final))

    cursor.execute("INSERT INTO notas_finais VALUES" + dados_inseridos)
    
    lista_notas.clear()

    banco.commit()

cursor.execute("SELECT * from notas_finais as json")

dados = cursor.fetchall()

'''lista_IDs = []
for c in dados:
    x = c[0]
    lista_IDs.append(x)

lista_nomes = []
for c in dados:
    x = c[1]
    lista_nomes.append(x)

lista_notas = []
for c in dados:
    x = c[2]
    lista_notas.append(x)'''

print(dados)

banco.close()
