# Arquivo: view/admin_clear_data_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import processar_limpeza_tabela, processar_limpeza_total_bd

class AdminClearDataView(tk.Frame):
    """
    Módulo administrativo para limpeza e reset de dados.
    Apenas para perfil 'Adm'.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master, padx=20, pady=20)
        self.controller = controller
        
        tk.Label(self, text="⚠️ GERENCIAMENTO DE LIMPEZA DE DADOS (ADM)", 
                 font=("Arial", 16, "bold"), fg='darkred').pack(pady=(0, 20), anchor='w')

        tk.Label(self, text="Use estas ferramentas com EXTREMA CAUTELA! As ações são irreversíveis.", 
                 font=("Arial", 12), fg='red').pack(pady=(0, 30), anchor='w')

        # --- Frame para Limpeza Individual ---
        frame_individual = tk.LabelFrame(self, text="Limpeza de Tabela Individual", padx=15, pady=15)
        frame_individual.pack(pady=10, fill='x')
        
        tk.Label(frame_individual, text="Selecione a tabela que deseja limpar completamente (excluindo todos os registros):", anchor='w').pack(fill='x', pady=5)
        
        # Tabelas que são relativamente seguras para limpeza individual
        self.tabelas = ['emprestimo', 'reserva', 'editora']
        self.tabela_var = tk.StringVar(value=self.tabelas[0])
        
        ttk.Combobox(frame_individual, textvariable=self.tabela_var, values=self.tabelas, state='readonly', width=30).pack(pady=10)
        
        tk.Button(frame_individual, text="LIMPAR TABELA SELECIONADA", 
                  command=self.handle_limpeza_individual, 
                  bg='#ffc107', fg='black', font=("Arial", 10, "bold")).pack(pady=10)

        # --- Frame para Limpeza Total ---
        frame_total = tk.LabelFrame(self, text="Limpeza Total (Reset de BD)", padx=15, pady=15, bg='#f8d7da')
        frame_total.pack(pady=30, fill='x')
        
        tk.Label(frame_total, text="Esta ação limpa TODAS as tabelas de dados na ordem correta: Empréstimo, Reserva, Livro, Editora, Usuário.", 
                 font=("Arial", 10, "bold"), fg='darkred', bg='#f8d7da').pack(fill='x', pady=5)
                 
        tk.Button(frame_total, text="!!! EXECUTAR LIMPEZA TOTAL DO BANCO DE DADOS !!!", 
                  command=self.handle_limpeza_total, 
                  bg='red', fg='white', font=("Arial", 12, "bold")).pack(pady=10)


    def handle_limpeza_individual(self):
        tabela = self.tabela_var.get()
        confirm = messagebox.askyesno(
            "Confirmação de Limpeza",
            f"Você tem certeza absoluta que deseja LIMPAR todos os dados da tabela '{tabela.upper()}'? Esta ação não pode ser desfeita."
        )
        
        if confirm:
            sucesso, mensagem = processar_limpeza_tabela(tabela)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro de Limpeza", mensagem)

    def handle_limpeza_total(self):
        confirm = messagebox.askyesno(
            "CONFIRMAÇÃO FINAL DE RESET DE BD",
            "ATENÇÃO: Você está prestes a apagar TODOS os dados de TODAS as tabelas. Deseja prosseguir?"
        )

        if confirm:
            sucesso, mensagem = processar_limpeza_total_bd()
            if sucesso:
                messagebox.showinfo("Sucesso Total", mensagem + " Será necessário recriar o usuário Admin na próxima execução.")
            else:
                messagebox.showerror("Falha Parcial/Total", mensagem)