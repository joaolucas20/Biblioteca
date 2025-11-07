# Arquivo: controller/biblioteca_controller.py

import re
import hashlib
from model.biblioteca_model import (
    db_get_usuario_by_email, db_add_usuario, db_list_usuarios, db_update_usuario, 
    db_delete_usuario, db_update_usuario_senha, 
    db_list_livros, db_add_livro, db_update_livro, db_delete_livro, 
    db_get_editora_by_id, db_update_exemplares, db_get_estoque,
    db_list_editoras, db_add_editora, db_update_editora, db_delete_editora,
    db_list_emprestimos_ativos, db_add_emprestimo, db_update_devolucao,
    db_list_livros_com_filtro
)

# --- Hashing de Senha ---

def hash_senha(senha):
    """Gera um hash SHA256 para a senha."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()
    
def verificar_senha(senha_digitada, senha_hashed):
    """Verifica se a senha digitada corresponde ao hash salvo."""
    return hash_senha(senha_digitada) == senha_hashed


# --- CONTROLLER: LOGIN/CADASTRO/USUARIO ---

def processar_login(email, senha):
    """Controla o fluxo de login."""
    if not email or not senha:
        return None
        
    usuario = db_get_usuario_by_email(email)
    
    if usuario and verificar_senha(senha, usuario['Senha']):
        usuario.pop('Senha') 
        return usuario
    return None

def processar_cadastro(nome, tipo, telefone, email, senha):
    """Controla o fluxo de cadastro de novos Leitores (via LoginView)."""
    try:
        senha_hashed = hash_senha(senha)
        return db_add_usuario(nome, tipo, telefone, email, senha_hashed, "Endereço não informado no cadastro rápido")
    except Exception as e:
        # print(f"Erro no cadastro: {e}") # Descomente se precisar debuggar
        return False

def processar_lista_usuarios():
    return db_list_usuarios()

def processar_adicao_usuario(nome, tipo, telefone, email, senha, endereco):
    try:
        senha_hashed = hash_senha(senha)
        return db_add_usuario(nome, tipo, telefone, email, senha_hashed, endereco)
    except Exception:
        return False
        
def processar_edicao_usuario(user_id, nome, tipo, telefone, email, endereco):
    try:
        return db_update_usuario(user_id, nome, tipo, telefone, email, endereco)
    except Exception:
        return False
        
def processar_exclusao_usuario(user_id):
    try:
        return db_delete_usuario(user_id)
    except Exception:
        return False

def processar_reset_senha(user_id, nova_senha):
    try:
        senha_hashed = hash_senha(nova_senha)
        return db_update_usuario_senha(user_id, senha_hashed)
    except Exception:
        return False


# --- CONTROLLER: EDITORA ---

def processar_lista_editoras():
    return db_list_editoras()

def processar_adicao_editora(nome, endereco, telefone):
    try:
        return db_add_editora(nome, endereco, telefone)
    except Exception:
        return False

def processar_edicao_editora(editora_id, nome, endereco, telefone):
    try:
        return db_update_editora(editora_id, nome, endereco, telefone)
    except Exception:
        return False

def processar_exclusao_editora(editora_id):
    try:
        return db_delete_editora(editora_id)
    except Exception:
        return False
        
        
# --- CONTROLLER: LIVRO (ACERVO) ---
# Estas são as funções que faltavam no seu controller e causaram o ImportError!

def processar_lista_livros():
    return db_list_livros()

def _validar_dados_livro(titulo, autor, ano, qtd, editora_id):
    if not all([titulo, autor, ano, qtd, editora_id]):
        return False, "Todos os campos obrigatórios devem ser preenchidos."
    try:
        ano = int(ano)
        qtd = int(qtd)
        editora_id = int(editora_id)
        if qtd < 0:
            return False, "Número de exemplares não pode ser negativo."
        if db_get_editora_by_id(editora_id) is None:
            return False, "O ID da Editora informado não existe."
        return True, (titulo, autor, ano, qtd, editora_id)
    except ValueError:
        return False, "Ano, Estoque e ID da Editora devem ser números inteiros."

def processar_adicao_livro(titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao):
    sucesso, dados = _validar_dados_livro(titulo, autor, ano, qtd, editora_id)
    if not sucesso: return False
    
    try:
        classificacao = int(classificacao) 
        isbn_val = int(isbn) if isbn else None
    except ValueError:
        return False 

    try:
        return db_add_livro(titulo, autor, isbn_val, dados[2], dados[3], dados[4], genero, classificacao)
    except Exception:
        return False

def processar_edicao_livro(livro_id, titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao):
    sucesso, dados = _validar_dados_livro(titulo, autor, ano, qtd, editora_id)
    if not sucesso: return False

    try:
        classificacao = int(classificacao)
        isbn_val = int(isbn) if isbn else None
    except ValueError:
        return False
    
    try:
        return db_update_livro(livro_id, titulo, autor, isbn_val, dados[2], dados[3], dados[4], genero, classificacao)
    except Exception:
        return False

def processar_exclusao_livro(livro_id):
    try:
        return db_delete_livro(livro_id)
    except Exception:
        return False
#NOVO: Função para buscar livros com filtro para o Leitor
def processar_busca_livros(termo_busca, campo_busca):
    """Busca livros no acervo com base no termo e campo de filtro."""

    # Chamada ao Model para buscar
    livros = db_list_livros_com_filtro(termo_busca, campo_busca)
    return livros        
        
# --- CONTROLLER: EMPRÉSTIMO/DEVOLUÇÃO ---

def processar_busca_emprestados():
    return db_list_emprestimos_ativos()

def processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev):
    try:
        estoque_atual = db_get_estoque(livro_id)
        
        if estoque_atual <= 0:
            return False 
            
        emprestimo_sucesso = db_add_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev)
        
        if emprestimo_sucesso:
            db_update_exemplares(livro_id, -1)
            return True
        return False

    except Exception:
        return False

def processar_registro_devolucao(livro_id, usuario_id, data_devolucao):
    try:
        devolucao_sucesso = db_update_devolucao(livro_id, usuario_id, data_devolucao)
        
        if devolucao_sucesso > 0: 
            db_update_exemplares(livro_id, 1)
            return True
        
        return False

    except Exception:
        return False

# --- FUNÇÕES INICIAIS (Para o app.py) ---

def cadastrar_usuario(nome, tipo, telefone, email, senha, endereco):
    """Usada para criar o usuário Admin inicial no app.py."""
    senha_hashed = hash_senha(senha)
    # Tenta adicionar. Se falhar (e-mail duplicado), o erro é esperado/silenciado.
    try:
        return db_add_usuario(nome, tipo, telefone, email, senha_hashed, endereco)
    except:
        return True