# Arquivo: model/livro_model.py

from model.db_connector import execute_query

# --- FUNÇÕES DE EMPRÉSTIMO (Já Existentes) ---

def get_livros_emprestados():
    """
    Busca no BD todos os livros que estão atualmente emprestados.
    """
    query = """
    SELECT
        L.Titulo,
        U.Nome AS Leitor,
        E.Data_Retirada,
        E.Data_Devolucao_Prev
    FROM
        Emprestimo E
    JOIN
        livro L ON E.Livro_ID = L.Id_livro
    JOIN
        Usuario U ON E.Usuario_ID = U.Id_Usuario
    WHERE
        E.Data_Devolucao_efet IS NULL
    ORDER BY
        E.Data_Devolucao_Prev ASC;
    """
    
    # Passamos fetch_all=True porque queremos todos os registros
    return execute_query(query, fetch_all=True)

def registrar_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev):
    """
    Insere um novo registro de empréstimo.
    """
    query = """
    INSERT INTO Emprestimo (Usuario_ID, Livro_ID, Data_Retirada, Data_Devolucao_Prev)
    VALUES (%s, %s, %s, %s)
    """
    params = (usuario_id, livro_id, data_retirada, data_devolucao_prev)
    
    return execute_query(query, params)

def registrar_devolucao(livro_id, usuario_id, data_devolucao_efetiva):
    """
    Atualiza um registro de empréstimo marcando a data de devolução efetiva.
    """
    query = """
    UPDATE Emprestimo
    SET Data_Devolucao_efet = %s
    WHERE Livro_ID = %s
      AND Usuario_ID = %s
      AND Data_Devolucao_efet IS NULL; -- Apenas o empréstimo ativo
    """
    params = (data_devolucao_efetiva, livro_id, usuario_id)
    
    return execute_query(query, params)

# --- NOVAS FUNÇÕES CRUD DE LIVRO (ATUALIZADAS) ---

# R de CRUD: Listar Livros (Atualizada para refletir nome da coluna)
def buscar_livros():
    """Busca todos os livros (acervo completo)."""
    query = """
    SELECT 
        Id_livro, Titulo, Autor, ISBN, Ano_Publicacao, Numero_Exemplares, genero, classificacao, Editora_ID
    FROM 
        Livro
    ORDER BY 
        Titulo
    """
    return execute_query(query, fetch_all=True)

# C de CRUD: Adicionar Livro (CORRIGIDA E ATUALIZADA)
def adicionar_livro(titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao):
    """Insere um novo livro no acervo, incluindo campos obrigatórios do BD."""
    query = """
    INSERT INTO Livro (Titulo, Autor, ISBN, Ano_Publicacao, Numero_Exemplares, Editora_ID, genero, classificacao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao)
    return execute_query(query, params)

# U de CRUD: Atualizar Livro (CORRIGIDA E ATUALIZADA)
def atualizar_livro(id_livro, titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao):
    """Atualiza os dados de um livro existente."""
    query = """
    UPDATE Livro
    SET Titulo = %s, Autor = %s, ISBN = %s, Ano_Publicacao = %s, Numero_Exemplares = %s, Editora_ID = %s, genero = %s, classificacao = %s
    WHERE Id_livro = %s
    """
    params = (titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao, id_livro)
    return execute_query(query, params)

# D de CRUD: Deletar Livro (SEM ALTERAÇÃO)
def deletar_livro(id_livro):
    """Deleta um livro pelo ID."""
    query = """
    DELETE FROM Livro
    WHERE Id_livro = %s
    """
    params = (id_livro,)
    return execute_query(query, params)
# Completar livro_model.py após as funções existentes

def buscar_livros(genero=None, classificacao=None):
    """Busca livros com filtros opcionais (para View de Buscar Livros)."""
    query = """
    SELECT Id_livro, Titulo, Autor, ISBN, Ano_Publicacao, Numero_Exemplares, genero, classificacao, Editora_ID
    FROM Livro
    """
    params = []
    if genero:
        query += " WHERE genero = %s"
        params.append(genero)
    if classificacao:
        if 'WHERE' in query:
            query += " AND classificacao = %s"
        else:
            query += " WHERE classificacao = %s"
        params.append(classificacao)
    query += " ORDER BY Titulo"
    return execute_query(query, params, fetch_all=True)