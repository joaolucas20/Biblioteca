# Arquivo: controller/biblioteca_controller.py

from model.usuario_model import verificar_login, cadastrar_usuario, buscar_todos_usuarios, atualizar_usuario, deletar_usuario, atualizar_senha
from model.livro_model import get_livros_emprestados, registrar_emprestimo, registrar_devolucao

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def processar_login(email, senha):
    """
    Orquestrador de login. Retorna o dicionário do usuário logado ou None.
    """
    usuario = verificar_login(email, senha)
    return usuario

def processar_cadastro(nome, tipo, telefone, email, senha):
    """
    Orquestrador de cadastro (para a tela de Login/Cadastro). Retorna True/False.
    """
    if not nome or not email or not senha:
        return False 
        
    # Leitor é o tipo padrão para auto-cadastro
    return cadastrar_usuario(nome, 'Leitor', telefone, email, senha)

# --- FUNÇÕES DE EMPRÉSTIMO (já existiam) ---

def processar_busca_emprestados():
    return get_livros_emprestados()

def processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev):
    return registrar_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev)

def processar_registro_devolucao(livro_id, usuario_id, data_devolucao_efetiva):
    return registrar_devolucao(livro_id, usuario_id, data_devolucao_efetiva)


# --- NOVAS FUNÇÕES CRUD DE USUÁRIO ---

def processar_lista_usuarios():
    """Chama o Model para buscar todos os usuários."""
    return buscar_todos_usuarios()

def processar_adicao_usuario(nome, tipo, telefone, email, senha):
    """Orquestra a adição de um novo usuário (usado pelo Admin)."""
    if not nome or not email or not senha or not tipo:
        return False
        
    # Tipo é variável aqui (diferente do auto-cadastro)
    return cadastrar_usuario(nome, tipo, telefone, email, senha)

def processar_edicao_usuario(id_usuario, nome, tipo, telefone, email):
    """Orquestra a edição dos dados de um usuário."""
    if not nome or not email or not tipo:
        return False
    
    return atualizar_usuario(id_usuario, nome, tipo, telefone, email)

def processar_reset_senha(id_usuario, nova_senha):
    """Orquestra o reset da senha de um usuário."""
    if not nova_senha:
        return False
        
    return atualizar_senha(id_usuario, nova_senha)

def processar_exclusao_usuario(id_usuario):
    """Orquestra a exclusão de um usuário."""
    return deletar_usuario(id_usuario)