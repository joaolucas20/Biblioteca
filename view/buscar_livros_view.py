# Arquivo: view/buscar_livros_view.py

import tkinter as tk
from tkinter import ttk
from controller.biblioteca_controller import processar_busca_livros # NOVA FUNÇÃO NO CONTROLLER

class BuscarLivrosView(tk.Frame):
    """
    Módulo para o Leitor buscar e visualizar livros no acervo.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        
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

        self.tree = ttk.Treeview(self.tree_frame, columns=('Titulo', 'Autor', 'Genero', 'Estoque'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Genero', text='Gênero')
        self.tree.heading('Estoque', text='Disponibilidade')

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
            
        # Chama a nova função do Controller com o termo de busca
        livros = processar_busca_livros(termo, campo)
        
        if livros:
            for livro in livros:
                estoque = livro['Numero_Exemplares']
                # Define a tag e o texto de estoque
                if estoque > 0:
                    tag = 'disponivel'
                    estoque_text = f"{estoque} (Disponível)"
                else:
                    tag = 'indisponivel'
                    estoque_text = "Indisponível"
                    
                self.tree.insert('', 'end', 
                                 values=(livro['Titulo'], livro['Autor'], livro['genero'], estoque_text), 
                                 tags=(tag,))
                                 
            self.tree.tag_configure('disponivel', foreground='green')
            self.tree.tag_configure('indisponivel', foreground='red', font=('Arial', 9, 'bold'))

        else:
             self.tree.insert('', 'end', values=('Nenhum livro encontrado ou acervo vazio.', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')