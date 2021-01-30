from flask import Flask, request
from columns_sql import qtd_colunas, qtd_colunas2
import json
import pymysql
import mysql.connector

# Criando um banco de dados: #

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)

cursor = banco.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS escola_alf")

# Banco de dados criado. #

app = Flask("Escola Alf")

@app.route("/cadastro/gabarito", methods = ["POST"])
def cadastro_gabarito():

    body = request.get_json()

    banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "escola_alf")

    cursor = banco.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS gabaritos' + qtd_colunas(body))

    con = pymysql.connect(host = "localhost", user = "root", password = "", db = "escola_alf")
    
    cursor = con.cursor()

    for item in body:
        prova = item.get("prova")
        quest_1 = item.get("quest_1")
        quest_2 = item.get("quest_2")
        quest_3 = item.get("quest_3")
        quest_4 = item.get("quest_4")
        quest_5 = item.get("quest_5")
        quest_6 = item.get("quest_6")
        cursor.execute("insert into gabaritos(prova, quest_1, quest_2, quest_3, quest_4, quest_5, quest_6) value(%s, %s, %s, %s, %s, %s, %s)", (prova, quest_1, quest_2, quest_3, quest_4, quest_5, quest_6))

    con.commit()
    con.close()

    return "Cadastro feito!"

@app.route("/cadastro/respostas", methods = ["POST"])
def cadastro_respostas():

    # body = request.get_json()

    banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "escola_alf")

    cursor = banco.cursor()

    # nomes_alunos = body.keys()
    
    print(cursor.execute("SELECT count(*) FROM information_schema.columns WHERE table_name = 'gabaritos'"))
    
    '''for nome in nomes_alunos:
        cursor.execute('CREATE TABLE IF NOT EXISTS' + str(nome) + qtd_colunas2(num_colunas))'''

    return 'Respostas cadastradas com sucesso!'

app.run()
