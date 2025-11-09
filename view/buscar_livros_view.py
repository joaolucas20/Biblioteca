# Arquivo: view/buscar_livros_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import processar_busca_livros, processar_registro_emprestimo 
from datetime import datetime, timedelta

class BuscarLivrosView(tk.Frame):
    """
    Módulo para o Leitor buscar e visualizar livros no acervo e solicitar empréstimos.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data # Usado para pegar o Id_Usuario
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Título
        tk.Label(self, text="🔍 BUSCAR LIVROS NO ACERVO", font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        # 2. Frame de Busca
        self.create_search_frame(self)
        
        # 3. Frame e Treeview de Resultados
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.create_treeview()
        
        # NOVO: Botão de Ação para Empréstimo
        tk.Button(self, text="Realizar Empréstimo do Livro Selecionado", 
                  command=self.handle_emprestimo, 
                  bg='#008CBA', fg='white', font=('Arial', 10, 'bold')).grid(row=3, column=0, pady=10)
        
        # Carregar todos os livros ao iniciar
        self.load_data()

    def create_search_frame(self, parent):
        search_frame = tk.Frame(parent)
        search_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        tk.Label(search_frame, text="Busca:").pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar(value="Titulo")
        tk.Label(search_frame, text="Filtrar por:").pack(side=tk.LEFT, padx=10)
        ttk.Combobox(search_frame, textvariable=self.search_var, values=['Titulo', 'Autor', 'Gênero'], state='readonly', width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="BUSCAR", command=self.load_data).pack(side=tk.LEFT, padx=15)
        
    def create_treeview(self):
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Adicionando 'Id_livro' como primeira coluna (oculta)
        self.tree = ttk.Treeview(self.tree_frame, columns=('Id', 'Titulo', 'Autor', 'Genero', 'Estoque'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Id', text='ID')
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Genero', text='Gênero')
        self.tree.heading('Estoque', text='Disponibilidade')

        # Configurando a coluna ID para ficar oculta (width=0, stretch=NO)
        self.tree.column('Id', width=0, stretch=tk.NO) 
        self.tree.column('Titulo', anchor='w', width=350)
        self.tree.column('Autor', anchor='w', width=180)
        self.tree.column('Genero', anchor='w', width=150)
        self.tree.column('Estoque', anchor='center', width=120)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        termo = self.search_entry.get()
        campo = self.search_var.get()
            
        livros = processar_busca_livros(termo, campo)
        
        if livros:
            for livro in livros:
                estoque = livro['Numero_Exemplares']
                
                if estoque > 0:
                    tag = 'disponivel'
                    estoque_text = f"{estoque} (Disponível)"
                else:
                    tag = 'indisponivel'
                    estoque_text = "Indisponível"
                    
                self.tree.insert('', 'end', 
                                 # Inserindo o ID do livro no início
                                 values=(livro['Id_livro'], livro['Titulo'], livro['Autor'], livro['genero'], estoque_text), 
                                 tags=(tag,))
                                 
            self.tree.tag_configure('disponivel', foreground='green')
            self.tree.tag_configure('indisponivel', foreground='red', font=('Arial', 9, 'bold'))

        else:
             self.tree.insert('', 'end', values=('', 'Nenhum livro encontrado ou acervo vazio.', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')

    def handle_emprestimo(self):
        """Lida com a solicitação de empréstimo pelo Leitor."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para solicitar o empréstimo.")
            return

        # Recupera valores (Id_livro está no índice 0)
        values = self.tree.item(selected_item, 'values')
        livro_id = int(values[0])
        titulo = values[1]
        estoque_text = values[4] # Texto que indica disponibilidade

        if "Indisponível" in estoque_text:
            messagebox.showwarning("Atenção", f"O livro '{titulo}' está indisponível no momento.")
            return

        confirm = messagebox.askyesno(
            "Confirmação de Empréstimo",
            f"Deseja confirmar o empréstimo do livro '{titulo}'?"
        )

        if confirm:
            try:
                # Datas de empréstimo (15 dias de prazo padrão)
                data_retirada = datetime.now().strftime('%Y-%m-%d')
                data_dev_prev = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d') 
                
                # O ID do Leitor é o usuário logado
                usuario_id = self.user_data['Id_Usuario']
                
                # Chama o Controller para registrar o empréstimo e atualizar o estoque (-1)
                sucesso = processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Empréstimo de '{titulo}' registrado com sucesso! Devolução prevista para {data_dev_prev}.")
                    self.load_data() # Recarrega a lista para atualizar o estoque
                    # (Opcional: chamar o recarregamento de MeusEmprestimosView se estiver aberto)
                else:
                    messagebox.showerror("Erro", "Falha ao registrar empréstimo. Verifique se o livro já não está emprestado para você ou se há estoque disponível.")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro interno ao processar o empréstimo. Contate a administração. Detalhes: {e}")