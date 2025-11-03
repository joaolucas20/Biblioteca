# Arquivo: controller/biblioteca_controller.py

from model.livro_model import get_livros_emprestados

def exibir_emprestados():
    print("\n--- Buscando Livros Emprestados ---")
    emprestados = get_livros_emprestados()
    
    if emprestados:
        for livro in emprestados:
            print(f"Título: {livro['Titulo']} | Leitor: {livro['Leitor']}")
    else:
        print("Nenhum livro encontrado.")