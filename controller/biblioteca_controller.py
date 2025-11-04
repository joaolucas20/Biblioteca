# Arquivo: controller/biblioteca_controller.py

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
    # Exemplo de validação simples antes de chamar o Model (lógica do Controller)
    if not nome or not email or not senha:
        return False 
        
    return cadastrar_usuario(nome, tipo, telefone, email, senha)

# ... Aqui ficariam as funções para Empréstimo, Devolução, etc.