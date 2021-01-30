from flask import Flask, request
from collections import OrderedDict
from itertools import zip_longest
import json
import math
import sqlite3

app = Flask("Escola_Alf")

@app.route("/cadastro/alunos", methods = ["POST"])
def cadastro_alunos():

    body = request.get_json()
    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    cursor.execute("DELETE FROM respostas")
    cursor.execute("DELETE FROM alunos")
    cursor.execute("CREATE TABLE IF NOT EXISTS alunos (id_aluno integer not null check(id_aluno between 1 AND 100) PRIMARY KEY, aluno text not null)")

    try:

        lista_alunos = []
        for item in range(0, len(body)):
            x = tuple(body[item].values())
            lista_alunos.append(x[0])

            def analisar(N):
                for i in N:
                    if 1 <= i <= 100:
                        lista = []
                        lista.append(i)
                    else:
                        return False

        if analisar(lista_alunos) == None:
            
            for item in range(0, len(body)):
                dados_inseridos = str(tuple(body[item].values()))
                cursor.execute("INSERT INTO alunos VALUES" + dados_inseridos)

            banco.commit()
            banco.close()
            mensagem = {"status": 200, "mensagem": "Aluno(s) cadastrado(s) com sucesso!"}
            mensagem = json.dumps(mensagem, indent=3)
            return mensagem

        else:

            banco.commit()
            banco.close()
            mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
            mensagem = json.dumps(mensagem, indent=3)
            return mensagem

    except sqlite3.IntegrityError:

        banco.commit()
        banco.close()
        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

@app.route("/consulta/alunos", methods = ["GET"])
def consulta_alunos():

    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    try:

        cursor.execute("SELECT * from alunos ORDER BY id_aluno, aluno")
        dados = cursor.fetchall()

        lista = []
        for item in dados:
            dic = {"id_aluno": item[0], "nome": item[1]}
            lista.append(dic)

        dados = json.dumps(lista, indent=3)

        banco.close()

        return dados

    except sqlite3.OperationalError:

        banco.commit()
        banco.close()
        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

@app.route("/cadastro/gabaritos", methods = ["POST"])
def cadastro_gabaritos():

    body = request.get_json()
    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    cursor.execute("DELETE FROM gabaritos")
    cursor.execute("CREATE TABLE IF NOT EXISTS gabaritos (prova integer not null, questao integer not null, resposta text not null, peso integer not null, PRIMARY KEY(prova, questao))")

    try:

        for item in range(0, len(body)):
            dados_inseridos = str(tuple(body[item].values()))
            cursor.execute("INSERT INTO gabaritos VALUES" + dados_inseridos)

        banco.commit()
        banco.close()
        mensagem = {"status": 200, "mensagem": "Gabaritos cadastrados com sucesso!"}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

    except sqlite3.IntegrityError:

        banco.commit()
        banco.close()
        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

@app.route("/consulta/gabaritos", methods = ["GET"])
def consulta_gabaritos():

    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    try:

        cursor.execute("SELECT * from gabaritos ORDER BY prova, questao")

        dados = cursor.fetchall()

        lista = []
        for item in dados:
            dic = {"prova": item[0], "questao": item[1], "resposta": item[2], "peso": item[3]}
            lista.append(dic)

        dados = json.dumps(lista, indent=3)

        banco.close()

        return dados

    except sqlite3.OperationalError:

        banco.commit()

        banco.close()

        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}

        mensagem = json.dumps(mensagem, indent=3)

        return mensagem

@app.route("/cadastro/respostas/<int:id_aluno>", methods = ["POST"])
def cadastro_respostas(id_aluno):

    body = request.get_json()
    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    cursor.execute("DELETE FROM respostas WHERE id_aluno = " + str(id_aluno))
    cursor.execute("CREATE TABLE IF NOT EXISTS respostas (id_aluno integer not null, prova integer not null, questao integer not null, resposta text not null, PRIMARY KEY (id_aluno, prova, questao), FOREIGN KEY (prova, questao) REFERENCES gabaritos (prova, questao), FOREIGN KEY (id_aluno) REFERENCES alunos (id_aluno))")

    try:

        cursor.execute("select * from gabaritos ORDER BY prova, questao")
        dados = cursor.fetchall()

        lista_questoes = []
        for c in dados:
            x = c[1]
            lista_questoes.append(x)

        cursor.execute("select * from alunos ORDER BY id_aluno, aluno")
        dados = cursor.fetchall()

        lista_IDs = []
        for c in dados:
            x = c[0]
            lista_IDs.append(x)

        def analisar2(na, x):
            for i in range(0, len(na)):
                if x != na[i]:
                    lista = []
                    lista.append(i)
                else:
                    return False

        if analisar2(lista_IDs, id_aluno) == False and len(body) == len(lista_questoes):

            for item in range(0, len(body)):
                lista = list(body[item].values())
                lista.insert(0, id_aluno)
                dados_inseridos = str(tuple(lista))
                cursor.execute("INSERT INTO respostas VALUES" + dados_inseridos)
    
            banco.commit()
            banco.close()
            mensagem = {"status": 200, "mensagem": "Respostas cadastradas com sucesso!"}
            mensagem = json.dumps(mensagem, indent=3)
            return mensagem

        else:

            banco.commit()
            banco.close()
            mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
            mensagem = json.dumps(mensagem, indent=3)
            return mensagem

    except sqlite3.IntegrityError:

        banco.commit()
        banco.close()
        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

@app.route("/consulta/respostas/<int:id_aluno>", methods = ["GET"])
def consulta_respostas(id_aluno):

    banco = sqlite3.connect('Escola_Alf.db')

    cursor = banco.cursor()

    id_aluno_string = str(id_aluno)

    try:

        cursor.execute("SELECT * from respostas WHERE id_aluno = " + id_aluno_string + " ORDER BY prova, questao")

        dados = cursor.fetchall()

        lista = []
        for item in dados:
            dic = {"id_aluno": item[0], "prova": item[1], "questao": item[2], "resposta": item[3]}
            lista.append(dic)

        dados = json.dumps(lista, indent=3)

        banco.close()

        return dados

    except sqlite3.OperationalError:

        banco.commit()

        banco.close()

        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado."}

        mensagem = json.dumps(mensagem, indent=3)

        return mensagem
        
@app.route("/consulta/notas_finais", methods = ["GET"])
def consulta_notas_finais():

    banco = sqlite3.connect('Escola_Alf.db')
    cursor = banco.cursor()

    try:

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

        cursor.execute("select * from respostas ORDER BY id_aluno, prova, questao")
        dados = cursor.fetchall()

        lista_provas = []
        for c in dados:
            x = c[1]
            lista_provas.append(x)

        lista_provas = list(OrderedDict(zip_longest(lista_provas, [])))

        cursor.execute("DROP TABLE IF EXISTS notas_finais")

        for i in range(1, (len(lista_IDs) + 1)):
            lista_notas = []
            for p in range(1, (len(lista_provas) + 1)):

                # Separa todas as alternativas corretas de uma prova:

                banco = sqlite3.connect('Escola_Alf.db')

                cursor = banco.cursor()
        
                cursor.execute("SELECT * FROM gabaritos WHERE prova = " + str(p) + " ORDER BY prova, questao")

                dados = cursor.fetchall()

                lista1 = []
                for item in dados:
                    dado = item[2]
                    lista1.append(dado)

                tamanho = len(lista1)

                # Separa os pesos de uma prova:

                cursor.execute("SELECT * FROM gabaritos WHERE prova = " + str(p) + " ORDER BY prova, questao")

                dados = cursor.fetchall()

                lista2 = []
                for item in dados:
                    dado = item[3]
                    lista2.append(dado)

                # Separa as alternativas de um aluno para uma prova:

                cursor.execute("SELECT * FROM respostas WHERE id_aluno = " + str(i) + " and prova = " + str(p) + " ORDER BY id_aluno, prova, questao")

                dados = cursor.fetchall()

                lista3 = []
                for item in dados:
                    dado = item[3]
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

                def truncate(number, digits) -> float:
                    stepper = pow(10.0, digits)
                    return math.trunc(stepper * number) / stepper

                nota = round(float(truncate((soma_dos_pesos / sum(lista2)), 2) * 10), 2)

                lista_notas.append(nota)

            soma_das_notas = sum(lista_notas)

            qtd_de_provas = len(lista_notas)

            media_final = soma_das_notas / qtd_de_provas

            cursor.execute("CREATE TABLE IF NOT EXISTS notas_finais (id_aluno integer not null check(id_aluno between 1 AND 100), aluno text not null, nota real not null)")

            dados_inseridos = str(( i, lista_nomes[i - 1], media_final))

            cursor.execute("INSERT INTO notas_finais VALUES" + dados_inseridos)
    
            lista_notas.clear()

            banco.commit()

        cursor.execute("SELECT * from notas_finais ORDER BY id_aluno")

        dados = cursor.fetchall()

        lista = []
        for item in dados:
            dic = {"id_aluno": item[0], "nome": item[1], "nota": item[2]}
            lista.append(dic)

        alunos = json.dumps(lista, indent=3)

        banco.close()

        return str(alunos)

    except IndexError:

        banco.commit()
        banco.close()
        mensagem = {"status": 500, "mensagem": "Ops! Algo deu errado. Verifique os dados e tente novamente."}
        mensagem = json.dumps(mensagem, indent=3)
        return mensagem

@app.route("/consulta/aprovados", methods = ["GET"])
def consulta_aprovados():

    banco = sqlite3.connect('Escola_Alf.db')

    cursor = banco.cursor()

    cursor.execute("SELECT * from notas_finais WHERE nota >=7")

    dados = cursor.fetchall()

    lista = []
    for item in dados:
        dic = {"id_aluno": item[0], "nome": item[1], "nota": item[2]}
        lista.append(dic)

    dados = json.dumps(lista, indent=3)

    return(dados)

app.run(debug=True)
