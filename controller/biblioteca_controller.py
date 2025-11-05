# Arquivo: controller/biblioteca_controller.py
from model.usuario_model import verificar_login, cadastrar_usuario
from model.livro_model import get_livros_emprestados, registrar_emprestimo, registrar_devolucao
from model.usuario_model import verificar_login, cadastrar_usuario

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def processar_login(email, senha):
    """
    Orquestrador de login. Retorna o dicionário do usuário logado ou None.
    """
    usuario = verificar_login(email, senha)
    return usuario

def processar_cadastro(nome, tipo, telefone, email, senha):
    """
    Orquestrador de cadastro. Retorna True/False.
    """
    if not nome or not email or not senha:
        return False 
        
    return cadastrar_usuario(nome, tipo, telefone, email, senha)



# --- FUNÇÕES DE EMPRÉSTIMO ---

def processar_busca_emprestados():
    """Retorna a lista de todos os livros atualmente emprestados."""
    return get_livros_emprestados()

def processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev):
    """Orquestra o registro de um novo empréstimo."""
    # Adicionar aqui LÓGICA DE NEGÓCIO (ex: verificar disponibilidade do livro)
    # Por enquanto, apenas registra:
    return registrar_emprestimo(usuario_id, livro_id, data_retirada, data_devolucao_prev)

def processar_registro_devolucao(livro_id, usuario_id, data_devolucao_efetiva):
    """Orquestra o registro de uma devolução."""
    # Adicionar aqui LÓGICA DE NEGÓCIO (ex: calcular multa)
    return registrar_devolucao(livro_id, usuario_id, data_devolucao_efetiva)

# ... Aqui ficariam as funções para Empréstimo, Devolução, etc.