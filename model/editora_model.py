# Arquivo: model/editora_model.py

from model.db_connector import execute_query

# --- CRUD DE EDITORA ---

# C de CRUD: Adicionar Editora
def adicionar_editora(nome, endereco, telefone):
    """Insere uma nova editora."""
    query = """
    INSERT INTO Editora (Nome, Endereco, Telefone)
    VALUES (%s, %s, %s)
    """
    params = (nome, endereco, telefone)
    return execute_query(query, params)

# R de CRUD: Buscar Todas Editoras
def buscar_todas_editoras():
    """Busca todas as editoras."""
    query = """
    SELECT 
        Id_Editora, Nome, Endereco, Telefone
    FROM 
        Editora
    ORDER BY 
        Nome
    """
    return execute_query(query, fetch_all=True)

# U de CRUD: Atualizar Editora
def atualizar_editora(id_editora, nome, endereco, telefone):
    """Atualiza os dados de uma editora."""
    query = """
    UPDATE Editora
    SET Nome = %s, Endereco = %s, Telefone = %s
    WHERE Id_Editora = %s
    """
    params = (nome, endereco, telefone, id_editora)
    return execute_query(query, params)

# D de CRUD: Deletar Editora
def deletar_editora(id_editora):
    """Deleta uma editora pelo ID."""
    query = """
    DELETE FROM Editora
    WHERE Id_Editora = %s
    """
    params = (id_editora,)
    return execute_query(query, params)