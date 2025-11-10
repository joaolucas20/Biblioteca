# Arquivo: model/emprestimo_model.py
# APENAS LÓGICA DE BANCO – SEM TKINTER!

from model.db_connector import execute_query

def get_emprestimos_usuario(usuario_id):
    """Busca empréstimos ativos do usuário."""
    query = """
    SELECT 
        E.Id_Emprestimo,
        L.Titulo AS Livro_Titulo,
        E.Data_Retirada,
        E.Data_Devolucao_Prev
    FROM Emprestimo E
    JOIN Livro L ON E.Livro_ID = L.Id_livro
    WHERE E.Usuario_ID = %s 
      AND E.Data_Devolucao_efet IS NULL
    ORDER BY E.Data_Retirada DESC
    """
    return execute_query(query, (usuario_id,), fetch_all=True)

def buscar_livros_disponiveis(termo=None):
    """Busca livros disponíveis para empréstimo."""
    query = """
    SELECT L.*
    FROM Livro L
    LEFT JOIN Emprestimo E ON L.Id_livro = E.Livro_ID AND E.Data_Devolucao_efet IS NULL
    WHERE E.Livro_ID IS NULL
    """
    params = []
    if termo:
        query += " AND (L.Titulo LIKE %s OR L.Autor LIKE %s)"
        params = [f"%{termo}%", f"%{termo}%"]
    query += " ORDER BY L.Titulo"
    return execute_query(query, params, fetch_all=True)