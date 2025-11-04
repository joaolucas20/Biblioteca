# Arquivo: model/usuario_model.py

import bcrypt 
from model.db_connector import execute_query 


# --- FUNÇÕES DE HASH E SEGURANÇA ---
def hash_password(senha):
    """Gera um hash bcrypt para a senha fornecida (em texto puro)."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(senha_clara, senha_hash):
    """Compara a senha em texto puro com o hash armazenado no BD."""
    try:
        return bcrypt.checkpw(senha_clara.encode('utf-8'), senha_hash.encode('utf-8'))
    except ValueError:
        return False


# --- FUNÇÃO: CADASTRO ---
def cadastrar_usuario(nome, tipo, telefone, email, senha_clara, endereco_id=None):
    """Cadastra um novo usuário, armazenando a senha em hash."""
    
    senha_hash = hash_password(senha_clara)
    
    query = """
    INSERT INTO Usuario (Nome, Tipo, Telefone, Email, Senha, Endereco_ID) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (nome, tipo, telefone, email, senha_hash, endereco_id)
    
    # Linhas afetadas (retorna o ID do novo registro, se o db_connector.py estiver atualizado)
    linhas_afetadas = execute_query(query, params)
    
    # Se retornar um ID (int > 0) ou 1 linha afetada (dependendo da versão do db_connector)
    return linhas_afetadas is not None and linhas_afetadas > 0

# --- FUNÇÃO: VERIFICAÇÃO DE LOGIN ---
def verificar_login(email, senha_clara):
    """
    Busca o usuário pelo email e verifica a senha (texto puro) contra o hash.
    Retorna o dicionário do usuário logado ou None.
    """
    query_busca = """
    SELECT 
        Id_Usuario, Nome, Tipo, Senha 
    FROM 
        Usuario 
    WHERE 
        Email = %s
    """
    params_busca = (email,)
    
    usuario = execute_query(query_busca, params_busca, fetch_all=False)
    
    if usuario and 'Senha' in usuario:
        senha_hash_armazenada = usuario['Senha']
        
        if check_password(senha_clara, senha_hash_armazenada):
            del usuario['Senha'] 
            return usuario
            
    return None