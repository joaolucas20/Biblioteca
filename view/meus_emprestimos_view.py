# Arquivo: view/meus_emprestimos_view.py (ATUALIZADO PARA HISTÓRICO COMPLETO)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.biblioteca_controller import processar_historico_leitor # NOVO: Usa a função de histórico do leitor

class MeusEmprestimosView(tk.Frame):
    """
    Módulo para o Leitor visualizar seu histórico COMPLETO de empréstimos.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        self.user_id = user_data['Id_Usuario']
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título alterado para Histórico
        tk.Label(self, text="📜 MEU HISTÓRICO DE EMPRÉSTIMOS", 
                 font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.create_treeview()
        
        tk.Button(self, text="Atualizar Histórico", command=self.load_data).grid(row=2, column=0, pady=10)

        self.load_data()

    def create_treeview(self):
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Colunas adicionadas: Autor e Data_Devolucao_efet
        self.tree = ttk.Treeview(self.tree_frame, columns=('Titulo', 'Autor', 'Retirada', 'DevolucaoPrev', 'DevolucaoEfet'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Titulo', text='Livro (Título)')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Retirada', text='Data Retirada')
        self.tree.heading('DevolucaoPrev', text='Devolução Prevista')
        self.tree.heading('DevolucaoEfet', text='Data Devolução')

        self.tree.column('Titulo', anchor='w', width=250)
        self.tree.column('Autor', anchor='w', width=180)
        self.tree.column('Retirada', anchor='center', width=120)
        self.tree.column('DevolucaoPrev', anchor='center', width=120)
        self.tree.column('DevolucaoEfet', anchor='center', width=120)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Chama a nova função que retorna o histórico completo
        historico = processar_historico_leitor(self.user_id)
        
        if historico:
            for item in historico:
                data_retirada_str = item['Data_Retirada'].strftime('%d/%m/%Y')
                data_dev_prev_str = item['Data_Devolucao_Prev'].strftime('%d/%m/%Y')
                
                # Checa se o livro ainda está ativo/atrasado ou se foi devolvido
                if item['Data_Devolucao_efet']:
                    data_efet_str = item['Data_Devolucao_efet'].strftime('%d/%m/%Y')
                    tag = 'devolvido'
                else:
                    data_efet_str = 'ATIVO'
                    is_overdue = datetime.now().date() > item['Data_Devolucao_Prev']
                    tag = 'atrasado' if is_overdue else 'ativo'

                self.tree.insert('', 'end', 
                                 values=(item['Titulo'], item['Autor'], data_retirada_str, data_dev_prev_str, data_efet_str), 
                                 tags=(tag,))
            
            # Configura os estilos para visualização
            self.tree.tag_configure('devolvido', foreground='#333')
            self.tree.tag_configure('ativo', foreground='blue', font=('Arial', 9, 'bold'))
            self.tree.tag_configure('atrasado', background='#f7dcdc', foreground='red', font=('Arial', 9, 'bold'))
            
        else:
             self.tree.insert('', 'end', values=('Você não possui histórico de empréstimos.', '', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')
