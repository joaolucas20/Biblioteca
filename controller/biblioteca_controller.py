# Arquivo: controller/biblioteca_controller.py

from model.usuario_model import verificar_login, cadastrar_usuario, buscar_todos_usuarios, atualizar_usuario, deletar_usuario, atualizar_senha
from model.livro_model import (
    get_livros_emprestados, registrar_emprestimo, registrar_devolucao,
    buscar_livros, adicionar_livro, atualizar_livro, deletar_livro
)
# NOVO: Importa funções do Model de Editora
from model.editora_model import (
    adicionar_editora, buscar_todas_editoras, atualizar_editora, deletar_editora
)


# --- FUNÇÕES DE AUTENTICAÇÃO ---

def processar_login(email, senha):
    usuario = verificar_login(email, senha)
    return usuario

# --- FUNÇÕES DE AUTENTICAÇÃO (ATUALIZADAS) ---

def processar_cadastro(nome, tipo, telefone, email, senha):
    """
    Orquestrador de cadastro (para o LoginView). Retorna True/False.
    Define um endereço padrão para atender à restrição NOT NULL.
    """
    if not nome or not email or not senha:
        return False 
        
    # Endereço padrão para cadastros via tela de Login (Leitor)
    endereco_default = "Endereço Não Informado (via cadastro inicial)"
        
    return cadastrar_usuario(nome, 'Leitor', telefone, email, senha, endereco_default)
# ... (outras funções CRUD de Empréstimo) ...

# --- FUNÇÕES DE EMPRÉSTIMO ---

def processar_busca_emprestados():
    return get_livros_emprestados()

def processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev):
    return registrar_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev)

def processar_registro_devolucao(livro_id, usuario_id, data_devolucao_efetiva):
    return registrar_devolucao(livro_id, usuario_id, data_devolucao_efetiva)


# --- FUNÇÕES CRUD DE USUÁRIO ---

def processar_lista_usuarios():
    return buscar_todos_usuarios()

# C de CRUD: Adição de Usuário pelo Admin (ATUALIZADA)
def processar_adicao_usuario(nome, tipo, telefone, email, senha, endereco):
    """Orquestra a adição de um novo usuário (usado pelo Admin), incluindo Endereco."""
    if not nome or not email or not senha or not tipo:
        return False
        
    return cadastrar_usuario(nome, tipo, telefone, email, senha, endereco)

# U de CRUD: Edição de Usuário pelo Admin (ATUALIZADA)
def processar_edicao_usuario(id_usuario, nome, tipo, telefone, email, endereco):
    """Orquestra a edição dos dados de um usuário, incluindo Endereco."""
    if not nome or not email or not tipo:
        return False
    
    return atualizar_usuario(id_usuario, nome, tipo, telefone, email, endereco)

def processar_reset_senha(id_usuario, nova_senha):
    if not nova_senha:
        return False
    return atualizar_senha(id_usuario, nova_senha)

def processar_exclusao_usuario(id_usuario):
    return deletar_usuario(id_usuario)


# --- FUNÇÕES CRUD DE LIVRO (ACERVO) ---

def processar_lista_livros():
    return buscar_livros()

def processar_adicao_livro(titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao):
    if not titulo or not autor or not numero_exemplares or not editora_id or not genero or not classificacao or not ano_publicacao:
        return False
    
    try:
        numero_exemplares = int(numero_exemplares)
        editora_id = int(editora_id)
        classificacao = int(classificacao)
        ano_publicacao = int(ano_publicacao)
    except ValueError:
        return False
        
    return adicionar_livro(titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao)

def processar_edicao_livro(id_livro, titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao):
    if not titulo or not autor or not numero_exemplares or not editora_id or not genero or not classificacao or not ano_publicacao:
        return False
        
    try:
        numero_exemplares = int(numero_exemplares)
        editora_id = int(editora_id)
        classificacao = int(classificacao)
        ano_publicacao = int(ano_publicacao)
    except ValueError:
        return False
        
    return atualizar_livro(id_livro, titulo, autor, isbn, ano_publicacao, numero_exemplares, editora_id, genero, classificacao)

def processar_exclusao_livro(id_livro):
    return deletar_livro(id_livro)
    
# --- NOVAS FUNÇÕES CRUD DE EDITORA ---

def processar_lista_editoras():
    """Chama o Model para buscar todas as editoras."""
    return buscar_todas_editoras()

def processar_adicao_editora(nome, endereco, telefone):
    """Orquestra a adição de uma nova editora."""
    if not nome:
        return False
    return adicionar_editora(nome, endereco, telefone)

def processar_edicao_editora(id_editora, nome, endereco, telefone):
    """Orquestra a edição dos dados de uma editora."""
    if not nome:
        return False
    return atualizar_editora(id_editora, nome, endereco, telefone)

def processar_exclusao_editora(id_editora):
    """Orquestra a exclusão de uma editora."""
    # Lógica de Negócio: Deve-se verificar se há livros associados antes de excluir.
    return deletar_editora(id_editora)
# Adicigit push --force-with-lease origin mainonar ao final de biblioteca_controller.py

from model.emprestimo_model import get_emprestimos_usuario, buscar_livros_disponiveis

def processar_meus_emprestimos(usuario_id):
    """Orquestra busca de empréstimos do usuário logado."""
    return get_emprestimos_usuario(usuario_id)

def processar_buscar_livros(termo_busca=None):
    """Orquestra busca de livros disponíveis."""
    return buscar_livros_disponiveis(termo_busca)