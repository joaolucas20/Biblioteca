# Arquivo: model/usuario_model.py

import bcrypt 
# Importação ABSOLUTA:
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
        # Caso o hash armazenado não esteja no formato correto (ex: se foi salvo em texto puro antes)
        return False


# --- FUNÇÃO: CADASTRO ---
def cadastrar_usuario(nome, tipo, telefone, email, senha_clara):
    """Cadastra um novo usuário, armazenando a senha em hash."""
    
    senha_hash = hash_password(senha_clara)
    
    query = """
    INSERT INTO Usuario (Nome, Tipo, Telefone, Email, Senha) 
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (nome, tipo, telefone, email, senha_hash)
    
    linhas_afetadas = execute_query(query, params)
    
    return linhas_afetadas == 1

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
    
    # Se o usuário foi encontrado e tem a coluna 'Senha'
    if usuario and 'Senha' in usuario:
        senha_hash_armazenada = usuario['Senha']
        
        # 2. Compara a senha (texto puro) com o hash
        if check_password(senha_clara, senha_hash_armazenada):
            del usuario['Senha'] # Remove o hash antes de retornar ao Controller/View
            return usuario
            
    return None