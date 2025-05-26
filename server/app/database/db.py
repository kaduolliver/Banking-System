from psycopg2 import pool
from dotenv import load_dotenv
import sys
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

try:
    connection_pool = pool.SimpleConnectionPool(
        1, 10,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    if connection_pool:
        print("Pool de conexões criado com sucesso!")

except Exception as error:
    print("Erro ao criar pool de conexões.", error)
    sys.exit(1)

def get_conn():
    try:
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        print("Erro ao pegar conexão:", e)
        return None
    
def release_conn(conn):
    try:
        connection_pool.putconn(conn)
    except Exception as e:
        print("Erro ao liberar conexão:", e)

def close_all():
    connection_pool.closeall()
    print("Todas as conexões foram fechadas.")

db_pool = connection_pool