# Arquivo: app.py

# IMPORTANTE: Garanta que você criou o arquivo controller/biblioteca_controller.py
# (Se você ainda não criou o controller, vamos importar diretamente do Model por enquanto)

from model.livro_model import get_livros_emprestados

def main():
    """Função principal da aplicação."""
    print("Iniciando o Sistema de Gerenciamento da Biblioteca...")
    
    # 1. Busca os livros emprestados usando a função do Model
    emprestados = get_livros_emprestados()

    print("\n--- Relatório de Livros Atualmente Emprestados ---")
    if emprestados:
        for livro in emprestados:
            # Acessando os campos do dicionário retornado
            print(f"Livro: {livro['Titulo']} | Leitor: {livro['Leitor']} | Data de Retirada: {livro['Data_Retirada']}")
    else:
        print("Nenhum livro encontrado. Todos disponíveis.")


if __name__ == "__main__":
    main()