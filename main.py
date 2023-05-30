import sqlite3

db_connection = sqlite3.connect("calculadora.db")
cursor = db_connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS historico (id INTEGER PRIMARY KEY AUTOINCREMENT, expressao TEXT, resultado REAL)"
)

db_connection.commit()
db_connection.close()
