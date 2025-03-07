import sys
import sqlite3 as lite
from datetime import datetime
import pandas as pd


con = lite.connect("personal.db")

#=========================================================================================
#Inserindo categoria
def insert_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query, i)
        

#Inserindo receita
def insert_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em,valor) VALUES (?,?,?)"
        cur.execute(query, i)


#Inserindo gastos
def insert_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria,retirado_em,valor) VALUES (?,?,?)"
        cur.execute(query, i)        

#====================================================================================
#Deletar receitas
def delete_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)
        
#Deletar gastos        
def delete_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)
#====================================================================================
#Ver categoria
def view_categoria():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for i in linha:
            lista_itens.append(i)
    return lista_itens   
     
#Ver receitas
def view_receitas():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for i in linha:
            lista_itens.append(i)
    return lista_itens   
     
#Ver gastos
def view_gastos():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for i in linha:
            lista_itens.append(i)
    return lista_itens   
     
def tabela():
    gastos = view_gastos()
    receitas = view_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista

def bar_valores():
    # Receita Total 
    receitas = view_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesas Total 
    receitas = view_gastos()
    despesas_lista = []

    for i in receitas:
        despesas_lista.append(i[3])

    despesas_total = sum(despesas_lista)

    # Despesas Total 
    saldo_total = receita_total - despesas_total

    return[receita_total,despesas_total,saldo_total]

def percentagem_valor():

    # Receita Total 
    receitas = view_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesas Total 
    receitas = view_gastos()
    despesas_lista = []

    for i in receitas:
        despesas_lista.append(i[3])

    despesas_total = sum(despesas_lista)

    # Despesas Total 
    total =  ((receita_total - despesas_total) / receita_total) * 100

    return[total]


def pie_valores():
    gastos = view_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista,columns = ['id', 'Categoria', 'Data', 'valor'])

    dataframe = dataframe.groupby('Categoria')['valor'].sum()
   
    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias,lista_quantias])