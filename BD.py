import sqlite3 as lite

con = lite.connect('pessoal.db')


#Tabela de Categoria
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

#Tabela de Receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")

#Tabela de Gastos
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")
    