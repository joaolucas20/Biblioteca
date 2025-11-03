# Arquivo: model/livro_model.py

from model.db_connector import execute_query

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