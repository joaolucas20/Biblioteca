# Arquivo: model/biblioteca_model.py

from model.db_connector import execute_query

# --- FUNÇÕES GENÉRICAS DE USUÁRIO (CRUD) ---

def db_list_usuarios():
    """Busca todos os usuários (leitores, bibl., adm)."""
    query = "SELECT Id_Usuario, Nome, Tipo, Telefone, Email, Endereco FROM usuario"
    return execute_query(query, fetch_all=True)

def db_get_usuario_by_email(email):
    """Busca um usuário por email, usada para login."""
    query = "SELECT Id_Usuario, Nome, Tipo, Telefone, Email, Senha FROM usuario WHERE Email = %s"
    return execute_query(query, (email,), fetch_all=False)

def db_add_usuario(nome, tipo, telefone, email, senha_hashed, endereco):
    """Cria um novo usuário."""
    query = "INSERT INTO usuario (Nome, Tipo, Telefone, Email, Senha, Endereco) VALUES (%s, %s, %s, %s, %s, %s)"
    params = (nome, tipo, telefone, email, senha_hashed, endereco)
    return execute_query(query, params)

def db_update_usuario(user_id, nome, tipo, telefone, email, endereco):
    """Atualiza dados de um usuário existente."""
    query = "UPDATE usuario SET Nome = %s, Tipo = %s, Telefone = %s, Email = %s, Endereco = %s WHERE Id_Usuario = %s"
    params = (nome, tipo, telefone, email, endereco, user_id)
    return execute_query(query, params)

def db_delete_usuario(user_id):
    """Exclui um usuário pelo ID."""
    query = "DELETE FROM usuario WHERE Id_Usuario = %s"
    return execute_query(query, (user_id,))
    
def db_update_usuario_senha(user_id, senha_hashed):
    """Atualiza a senha de um usuário."""
    query = "UPDATE usuario SET Senha = %s WHERE Id_Usuario = %s"
    return execute_query(query, (senha_hashed, user_id))

# --- FUNÇÕES GENÉRICAS DE EDITORA (CRUD) ---

def db_list_editoras():
    """Busca todas as editoras."""
    query = "SELECT Id_Editora, Nome, Endereco, Telefone FROM editora"
    return execute_query(query, fetch_all=True)

def db_add_editora(nome, endereco, telefone):
    """Cria uma nova editora."""
    query = "INSERT INTO editora (Nome, Endereco, Telefone) VALUES (%s, %s, %s)"
    params = (nome, endereco, telefone)
    return execute_query(query, params)

def db_update_editora(editora_id, nome, endereco, telefone):
    """Atualiza dados de uma editora."""
    query = "UPDATE editora SET Nome = %s, Endereco = %s, Telefone = %s WHERE Id_Editora = %s"
    params = (nome, endereco, telefone, editora_id)
    return execute_query(query, params)

def db_delete_editora(editora_id):
    """Exclui uma editora."""
    query = "DELETE FROM editora WHERE Id_Editora = %s"
    return execute_query(query, (editora_id,))

def db_get_editora_by_id(editora_id):
    """Busca uma editora pelo ID."""
    query = "SELECT Id_Editora FROM editora WHERE Id_Editora = %s"
    return execute_query(query, (editora_id,), fetch_all=False)
    
# --- FUNÇÕES GENÉRICAS DE LIVRO (CRUD) ---

def db_list_livros():
    """Busca todos os livros (Acervo)."""
    query = "SELECT Id_livro, Titulo, Autor, Editora_ID, ISBN, Ano_Publicacao, genero, classificacao, Numero_Exemplares FROM livro"
    return execute_query(query, fetch_all=True)

def db_add_livro(titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao):
    """Adiciona um novo livro."""
    query = "INSERT INTO livro (Titulo, Autor, ISBN, Ano_Publicacao, Numero_Exemplares, Editora_ID, genero, classificacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    params = (titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao)
    return execute_query(query, params)

def db_update_livro(livro_id, titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao):
    """Atualiza dados de um livro existente."""
    query = "UPDATE livro SET Titulo = %s, Autor = %s, ISBN = %s, Ano_Publicacao = %s, Numero_Exemplares = %s, Editora_ID = %s, genero = %s, classificacao = %s WHERE Id_livro = %s"
    params = (titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao, livro_id)
    return execute_query(query, params)

def db_delete_livro(livro_id):
    """Exclui um livro."""
    query = "DELETE FROM livro WHERE Id_livro = %s"
    return execute_query(query, (livro_id,))

def db_update_exemplares(livro_id, mudanca):
    """Ajusta o número de exemplares após empréstimo/devolução."""
    query = "UPDATE livro SET Numero_Exemplares = Numero_Exemplares + %s WHERE Id_livro = %s AND Numero_Exemplares + %s >= 0"
    return execute_query(query, (mudanca, livro_id, mudanca))

def db_get_estoque(livro_id):
    """Busca o número de exemplares disponíveis."""
    query = "SELECT Numero_Exemplares FROM livro WHERE Id_livro = %s"
    result = execute_query(query, (livro_id,), fetch_all=False)
    return result['Numero_Exemplares'] if result else -1

def db_list_livros_com_filtro(termo_busca, campo_busca):
    """Busca livros com filtro no BD."""
    base_query = "SELECT Id_livro, Titulo, Autor, Editora_ID, ISBN, Ano_Publicacao, genero, classificacao, Numero_Exemplares FROM livro"
    params = []

    if termo_busca and campo_busca:
        # Garante que o campo existe no BD
        if campo_busca == 'Titulo':
            coluna = 'Titulo'
        elif campo_busca == 'Autor':
            coluna = 'Autor'
        elif campo_busca == 'Gênero':
            coluna = 'genero'
        else:
            coluna = 'Titulo' # Padrão

        base_query += f" WHERE {coluna} LIKE %s"
        params.append(f'%{termo_busca}%')

    return execute_query(base_query, params, fetch_all=True)

# --- FUNÇÕES GENÉRICAS DE EMPRÉSTIMO ---

def db_list_emprestimos_ativos(usuario_id=None):
    """Lista empréstimos ativos, filtrando por usuário se o ID for fornecido."""
    query = """
        SELECT 
            e.Id_Emprestimo, l.Titulo, u.Nome AS Leitor, e.Data_Retirada, e.Data_Devolucao_Prev, 
            e.Usuario_ID, e.Livro_ID 
        FROM emprestimo e
        JOIN livro l ON e.Livro_ID = l.Id_livro
        JOIN usuario u ON e.Usuario_ID = u.Id_Usuario
        WHERE e.Data_Devolucao_efet IS NULL
    """
    params = []
    if usuario_id is not None:
        query += " AND e.Usuario_ID = %s"
        params.append(usuario_id)
        
    query += " ORDER BY e.Data_Devolucao_Prev ASC"
    
    return execute_query(query, params, fetch_all=True)

def db_add_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev):
    """Registra um novo empréstimo."""
    query = "INSERT INTO emprestimo (Usuario_ID, Livro_ID, Data_Retirada, Data_Devolucao_Prev, Status) VALUES (%s, %s, %s, %s, 'Emprestado')"
    params = (usuario_id, livro_id, data_retirada, data_dev_prev)
    return execute_query(query, params)

def db_update_devolucao(livro_id, usuario_id, data_devolucao):
    """Atualiza o registro de empréstimo para indicar devolução."""
    query = """
        UPDATE emprestimo 
        SET Data_Devolucao_efet = %s, Status = 'Devolvido' 
        WHERE Livro_ID = %s AND Usuario_ID = %s AND Data_Devolucao_efet IS NULL 
        ORDER BY Data_Retirada DESC LIMIT 1
    """
    params = (data_devolucao, livro_id, usuario_id)
    return execute_query(query, params)