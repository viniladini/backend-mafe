import pymysql

conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="3006",
    port=3306
)

try:
    with conexao.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS mafe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("Base de dados 'mafe_db' criada com sucesso!")
finally:
    conexao.close()