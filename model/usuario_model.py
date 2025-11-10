# Arquivo: model/usuario_model.py (COMPLETO BCRYPT)

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


# --- FUNÇÃO: CADASTRO (C de CRUD) ---
def cadastrar_usuario(nome, tipo, telefone, email, senha_clara, endereco):
    """Cadastra um novo usuário, armazenando a senha em hash BCRYPT."""
    senha_hash = hash_password(senha_clara)
    
    query = """
    INSERT INTO Usuario (Nome, Tipo, Telefone, Email, Senha, Endereco) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (nome, tipo, telefone, email, senha_hash, endereco)
    
    linhas_afetadas = execute_query(query, params)
    
    return linhas_afetadas is not None and linhas_afetadas > 0

# --- FUNÇÃO: VERIFICAÇÃO DE LOGIN ---
def verificar_login(email, senha_clara):
    """
    Busca o usuário pelo email e verifica a senha (texto puro) contra o hash BCRYPT.
    Retorna o dicionário do usuário logado ou None.
    """
    query_busca = """
    SELECT 
        Id_Usuario, Nome, Tipo, Telefone, Email, Endereco, Senha 
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
    
    
# --- NOVAS FUNÇÕES CRUD ---

# R de CRUD: Buscar Todos
def buscar_todos_usuarios():
    """Busca todos os usuários, incluindo Endereco."""
    query = """
    SELECT 
        Id_Usuario, Nome, Tipo, Telefone, Email, Endereco
    FROM 
        Usuario
    ORDER BY 
        Nome
    """
    return execute_query(query, fetch_all=True)

# U de CRUD: Atualizar
def atualizar_usuario(id_usuario, nome, tipo, telefone, email, endereco):
    """Atualiza dados do usuário, exceto a senha."""
    query = """
    UPDATE Usuario
    SET Nome = %s, Tipo = %s, Telefone = %s, Email = %s, Endereco = %s
    WHERE Id_Usuario = %s
    """
    params = (nome, tipo, telefone, email, endereco, id_usuario)
    return execute_query(query, params)

# U de CRUD: Atualizar Senha
def atualizar_senha(id_usuario, nova_senha_clara):
    """Atualiza a senha do usuário, usando hash BCRYPT."""
    senha_hash = hash_password(nova_senha_clara)
    query = """
    UPDATE Usuario
    SET Senha = %s
    WHERE Id_Usuario = %s
    """
    params = (senha_hash, id_usuario)
    return execute_query(query, params)

# D de CRUD: Deletar
def deletar_usuario(id_usuario):
    """Deleta um usuário pelo ID."""
    query = """
    DELETE FROM Usuario
    WHERE Id_Usuario = %s
    """
    params = (id_usuario,)
    return execute_query(query, params)