# Arquivo: model/db_connector.py

import mysql.connector
from mysql.connector import Error

# --- CONFIGURAÇÕES DO BD ---
CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rooot', # <<<< VERIFIQUE SUA SENHA AQUI!
    'database': 'biblioteca' # Usando o schema 'biblioteca'
}
# ---------------------------

def get_connection():
    """Tenta estabelecer e retornar uma conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}") 
        return None

def execute_query(query, params=None, fetch_all=False):
    """
    Função centralizada para executar qualquer consulta SQL.
    """
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True) 
    resultado = None
    
    try:
        cursor.execute(query, params or ())

        if query.strip().upper().startswith('SELECT'):
            resultado = cursor.fetchall() if fetch_all else cursor.fetchone()
        else:
            conn.commit()
            if query.strip().upper().startswith('INSERT'):
                 resultado = cursor.lastrowid
            else:
                 resultado = cursor.rowcount

    except Error as e:
        if not query.strip().upper().startswith('SELECT'):
            conn.rollback()
        resultado = None

    finally:
        if cursor and cursor.nextset():
            pass 
            
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
        return resultado