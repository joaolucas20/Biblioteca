# Arquivo: view/meus_emprestimos_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import db_list_emprestimos_ativos # Usamos a função do Model/Controller
from datetime import datetime

class MeusEmprestimosView(tk.Frame):
    """
    Módulo para o Leitor visualizar seus empréstimos ativos.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        self.user_id = user_data['Id_Usuario'] # ID do Leitor logado
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título
        tk.Label(self, text="📚 MEUS EMPRÉSTIMOS ATIVOS", font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        # Frame do Treeview
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview (Tabela)
        self.create_treeview()
        
        # Botão de Atualizar
        tk.Button(self, text="Atualizar Lista", command=self.load_data).grid(row=2, column=0, pady=10)

        # Carregar dados
        self.load_data()

    def create_treeview(self):
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('Titulo', 'Retirada', 'DevolucaoPrev'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Titulo', text='Livro (Título)')
        self.tree.heading('Retirada', text='Data Retirada')
        self.tree.heading('DevolucaoPrev', text='Devolução Prevista')

        self.tree.column('Titulo', anchor='w', width=450)
        self.tree.column('Retirada', anchor='center', width=150)
        self.tree.column('DevolucaoPrev', anchor='center', width=150)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca empréstimos filtrando pelo ID do Leitor logado
        # A função db_list_emprestimos_ativos foi ajustada no Model para aceitar o filtro.
        emprestimos = db_list_emprestimos_ativos(self.user_id) 
        
        if emprestimos:
            for item in emprestimos:
                data_retirada_str = item['Data_Retirada'].strftime('%d/%m/%Y')
                data_dev_prev_str = item['Data_Devolucao_Prev'].strftime('%d/%m/%Y')
                
                # Verifica se está atrasado para aplicar cor
                is_overdue = datetime.now().date() > item['Data_Devolucao_Prev']
                tag = 'atrasado' if is_overdue else ''

                self.tree.insert('', 'end', 
                                 values=(item['Titulo'], data_retirada_str, data_dev_prev_str), 
                                 tags=(tag,))
            
            # Configura a tag de atraso
            self.tree.tag_configure('atrasado', background='#f7dcdc', foreground='red')
            
        else:
             self.tree.insert('', 'end', values=('Você não possui livros emprestados no momento.', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')