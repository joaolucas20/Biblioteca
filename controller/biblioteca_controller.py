# Arquivo: controller/biblioteca_controller.py (FINAL E COMPLETO)

from datetime import datetime
import re
# Importa a lógica BCRYPT e CRUD de Usuário do arquivo modularizado
from model.usuario_model import (
    verificar_login, cadastrar_usuario, buscar_todos_usuarios, atualizar_usuario, 
    deletar_usuario, atualizar_senha
)
# Importa todas as funções de Model genéricas (Livro, Editora, Empréstimo, Limpeza)
from model.biblioteca_model import (
    db_get_usuario_by_email, db_get_editora_by_id, 
    db_list_livros, db_add_livro, db_update_livro, db_delete_livro, 
    db_update_exemplares, db_get_estoque, db_list_livros_com_filtro,
    db_list_editoras, db_add_editora, db_update_editora, db_delete_editora,
    db_list_emprestimos_ativos, db_add_emprestimo, db_update_devolucao,
    db_add_reserva, db_check_existing_reservation, db_list_reservas,
    db_check_admin_exists, db_clear_table,db_get_livro_historico,db_get_usuario_historico,
    db_list_emprestimos_usuario,db_processar_reserva, db_cancelar_reserva, db_get_reserva_detalhe
)

# --- CONTROLLER: LOGIN/CADASTRO/USUARIO (Usa BCRYPT via usuario_model) ---

def processar_login(email, senha):
    """Controla o fluxo de login, chamando o BCRYPT no usuario_model."""
    return verificar_login(email, senha)

def processar_cadastro(nome, tipo, telefone, email, senha, endereco="Não Informado"):
    """
    Controla o fluxo de cadastro, verifica duplicidade de email.
    A função cadastrar_usuario (do usuario_model) já faz o hashing BCRYPT.
    """
    # 1. VERIFICAÇÃO DE DUPLICIDADE DE EMAIL
    if db_get_usuario_by_email(email): 
        return False, "Erro: O e-mail fornecido já está cadastrado no sistema." 
    
    # 2. Executa o cadastro (a função do Model já faz o hashing)
    sucesso = cadastrar_usuario(nome, tipo or 'Leitor', telefone, email, senha, endereco)
    
    if sucesso:
        return True, "Cadastro realizado com sucesso."
    else:
        return False, "Falha ao cadastrar usuário no banco de dados."


def processar_lista_usuarios():
    return buscar_todos_usuarios() # Chama a função do usuario_model.py

def processar_adicao_usuario(nome, tipo, telefone, email, senha, endereco):
    # Reusa a lógica de cadastro, que verifica a duplicidade e faz o hashing BCRYPT
    sucesso, mensagem = processar_cadastro(nome, tipo, telefone, email, senha, endereco)
    return sucesso # Retorna apenas o status de sucesso para a View Admin
        
def processar_edicao_usuario(user_id, nome, tipo, telefone, email, endereco):
    try:
        return atualizar_usuario(user_id, nome, tipo, telefone, email, endereco) # BCRYPT
    except Exception:
        return False
        
def processar_exclusao_usuario(user_id):
    try:
        return deletar_usuario(user_id) # BCRYPT
    except Exception:
        return False

def processar_reset_senha(user_id, nova_senha):
    try:
        return atualizar_senha(user_id, nova_senha) # BCRYPT
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

def processar_busca_livros(termo_busca, campo_busca):
    return db_list_livros_com_filtro(termo_busca, campo_busca)
        
# --- CONTROLLER: CONSULTA DE STATUS/HISTÓRICO DE LIVRO ---

def processar_historico_livro(livro_id):
    """
    Retorna o histórico de empréstimos e o status atual de um livro.
    """
    historico = db_get_livro_historico(livro_id)
    status_atual = {"ativo": False, "leitor": "N/A", "atrasado": False}

    if historico:
        # O primeiro registro na lista DESC (mais recente) indica o status atual
        for registro in historico:
            if registro['Data_Devolucao_efet'] is None:
                status_atual['ativo'] = True
                status_atual['leitor'] = registro['Leitor']

                # Verifica atraso
                hoje = datetime.now().date()
                data_prevista = registro['Data_Devolucao_Prev']

                if hoje > data_prevista:
                    status_atual['atrasado'] = True
                    status_atual['status_msg'] = f"ATRASADO desde {data_prevista.strftime('%d/%m/%Y')}"
                else:
                    status_atual['status_msg'] = f"Com {registro['Leitor']} (Dev. Prev: {data_prevista.strftime('%d/%m/%Y')})"
                break # Encontramos o registro ativo, paramos.

    return historico, status_atual  

# --- CONTROLLER: CONSULTA DE HISTÓRICO DE USUÁRIO ---

def processar_historico_usuario(usuario_id):
    """
    Retorna o histórico de empréstimos (livros lidos) de um usuário.
    """
    historico = db_get_usuario_historico(usuario_id)
    return historico      
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
    

def processar_busca_emprestados():
    # Esta função ainda atende a View Adm/Bib (apenas ativos)
    return db_list_emprestimos_ativos() 

# --- NOVO: HISTÓRICO DE LEITOR ---
def processar_historico_leitor(usuario_id):
    """Retorna o histórico COMPLETO (ativos e devolvidos) do leitor."""
    return db_list_emprestimos_usuario(usuario_id)
    
# --- CONTROLLER: RESERVA ---

def processar_reserva(usuario_id, livro_id):
    """Lógica para registrar uma reserva."""
    try:
        estoque = db_get_estoque(livro_id)
        if estoque > 0:
            return False, "O livro está disponível para empréstimo imediato. Reserva não é necessária."
            
        if db_check_existing_reservation(usuario_id, livro_id):
            return False, "Você já possui uma reserva ativa para este livro."
            
        data_reserva = datetime.now().strftime('%Y-%m-%d')
        sucesso = db_add_reserva(usuario_id, livro_id, data_reserva)
        
        if sucesso:
            return True, "Reserva registrada com sucesso! Você será notificado quando o livro estiver disponível."
        else:
            return False, "Falha ao registrar reserva devido a um erro no banco de dados."
            
    except Exception as e:
        return False, f"Erro inesperado: {e}"

def processar_lista_reservas_ativas():
    return db_list_reservas()

def processar_atendimento_reserva(reserva_id, data_retirada, data_dev_prev):
    """
    Tenta registrar o empréstimo com base na reserva e finaliza a reserva.
    """
    detalhes = db_get_reserva_detalhe(reserva_id)
    
    if not detalhes:
        return False, "Reserva não encontrada ou já atendida/cancelada."
        
    usuario_id = detalhes['Usuario_ID']
    livro_id = detalhes['Livro_ID']
    
    # 1. Tenta Registrar o Empréstimo (Ele deve falhar se não houver estoque)
    # Reutilizamos a lógica de empréstimo, que já gerencia o estoque (-1)
    sucesso_emprestimo = db_add_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev)
    
    if sucesso_emprestimo:
        # 2. Atualiza o estoque (já feito pelo db_add_emprestimo)
        db_update_exemplares(livro_id, -1)
        
        # 3. Finaliza a Reserva
        db_processar_reserva(reserva_id)
        
        return True, "Empréstimo realizado e reserva finalizada com sucesso."
    else:
        # Se o empréstimo falhar, a reserva não é finalizada.
        return False, "Falha ao registrar empréstimo. O livro pode ter sido emprestado por outro meio ou o estoque está incorreto."


def processar_cancelamento_reserva(reserva_id):
    """
    Cancela uma reserva ativa.
    """
    sucesso = db_cancelar_reserva(reserva_id)
    if sucesso:
        return True, "Reserva cancelada com sucesso."
    else:
        return False, "Falha ao cancelar reserva."

# --- CONTROLLER: ADMIN CHECK E LIMPEZA DE DADOS ---

def processar_check_admin_exists():
    """Chama o Model para verificar se há algum Admin cadastrado."""
    return db_check_admin_exists()

def processar_limpeza_tabela(table_name):
    """
    Chama o Model para limpar a tabela, com verificações de segurança.
    """
    # 1. Tabela de alto risco (FKs apontam para ela)
    if table_name == 'usuario':
        return False, "Erro: Não é seguro limpar a tabela USUARIO. Limpe EMPRESTIMO e RESERVA primeiro, ou use o botão 'Limpar Tudo'."
    
    # 2. Tabela com FKs apontando para ela
    if table_name == 'livro':
        return False, "Erro: Não é seguro limpar a tabela LIVRO. Limpe EMPRESTIMO e RESERVA primeiro, ou use o botão 'Limpar Tudo'."

    # 3. Tabela segura para limpar individualmente
    if table_name in ['emprestimo', 'reserva', 'editora']:
        sucesso = db_clear_table(table_name)
        if sucesso is not None and sucesso is not False:
            return True, f"Tabela '{table_name.upper()}' limpa com sucesso!"
        else:
            return False, f"Falha ao limpar a tabela '{table_name.upper()}'. Verifique restrições de integridade."

    return False, "Tabela inválida ou não suportada para limpeza individual."

def processar_limpeza_total_bd():
    """Limpa as tabelas na ordem segura (para evitar falhas de FKs)."""
    tabelas_limpeza_ordenada = [
        'emprestimo', 
        'reserva', 
        'livro', 
        'editora', 
        'usuario'
    ]
    
    erros = []
    
    for table in tabelas_limpeza_ordenada:
        sucesso = db_clear_table(table)
        if sucesso is None or sucesso is False:
            erros.append(f"Falha ao limpar {table.upper()}")
            
    if not erros:
        return True, "LIMPEZA TOTAL DO BANCO DE DADOS CONCLUÍDA COM SUCESSO."
    else:
        return False, f"Limpeza concluída com erros: {', '.join(erros)}. Verifique as restrições de FK."

# --- FUNÇÕES INICIAIS (Para o app.py) ---
def cadastrar_usuario_inicial(nome, tipo, telefone, email, senha, endereco):
    """Usada para criar o usuário Admin inicial no app.py (BCRYPT)."""
    return cadastrar_usuario(nome, tipo, telefone, email, senha, endereco)