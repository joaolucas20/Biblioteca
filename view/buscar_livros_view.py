# Arquivo: view/buscar_livros_view.py
# --------------------------------------------------------------
# Busca de livros disponíveis (para perfil Leitor)
# --------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import processar_buscar_livros

class BuscarLivrosView(tk.Frame):
    """Módulo de busca de livros disponíveis para empréstimo."""
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_search_bar()
        self._create_treeview()
        self._load_all()               # carrega todos ao abrir

    # ------------------------------------------------------------------
    # Barra de pesquisa
    # ------------------------------------------------------------------
    def _create_search_bar(self):
        bar = tk.Frame(self)
        bar.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        tk.Label(bar, text="Buscar (título / autor):").pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(bar, width=40)
        self.entry_busca.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entry_busca.bind("<Return>", lambda e: self.search())

        tk.Button(bar, text="Pesquisar", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(bar, text="Limpar", command=self._load_all).pack(side=tk.LEFT, padx=5)

    # ------------------------------------------------------------------
    # Treeview
    # ------------------------------------------------------------------
    def _create_treeview(self):
        cols = ("ID", "Título", "Autor", "ISBN", "Ano", "Exemplares", "Gênero", "Classificação")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110, anchor='w')
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        vsb.grid(row=1, column=1, sticky='ns')

    # ------------------------------------------------------------------
    # Carregar todos / resultado da busca
    # ------------------------------------------------------------------
    def _load_all(self):
        self.entry_busca.delete(0, tk.END)
        self._populate(processar_buscar_livros())

    def search(self):
        termo = self.entry_busca.get().strip()
        self._populate(processar_buscar_livros(termo))

    def _populate(self, livros):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not livros:
            messagebox.showinfo("Resultado", "Nenhum livro encontrado.")
            return
        for l in livros:
            self.tree.insert("", "end", values=(
                l["Id_livro"], l["Titulo"], l["Autor"], l["ISBN"],
                l["Ano_Publicacao"], l["Numero_Exemplares"],
                l["genero"], l["classificacao"]
            ))