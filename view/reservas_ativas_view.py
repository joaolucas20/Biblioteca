# Arquivo: view/reservas_ativas_view.py (FINAL COM AÇÕES)

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import (
    processar_lista_reservas_ativas,
    processar_atendimento_reserva,   # NOVO
    processar_cancelamento_reserva   # NOVO
)
from datetime import datetime, timedelta

class ReservasAtivasView(tk.Frame):
    """
    Módulo para Adm/Biblioteca visualizar e gerenciar reservas ativas.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Linha 3 agora é o tree_frame

        # 1. Título
        tk.Label(self, text="⏳ GERENCIAMENTO DE RESERVAS ATIVAS", 
                 font=("Arial", 16, "bold"), fg='#ff8c00').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        ttk.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='ew', padx=10)
        
        # 2. Botões de Ação
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, sticky='w', padx=10, pady=(10, 10))
        
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)
        
        # Botões de Ação de Gerenciamento
        ttk.Button(btn_frame, text="✅ Atender Reserva", command=self.handle_atendimento).pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(btn_frame, text="❌ Cancelar Reserva", command=self.handle_cancelamento).pack(side=tk.LEFT, padx=5)
        
        # 3. Frame e Treeview
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.create_treeview()
        self.load_data()

    def create_treeview(self):
        # ... (Código da Treeview - Sem alteração) ...
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Livro', 'Leitor', 'DataReserva'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID Reserva', anchor='center')
        self.tree.heading('Livro', text='Livro (Título)')
        self.tree.heading('Leitor', text='Leitor')
        self.tree.heading('DataReserva', text='Data da Reserva')

        self.tree.column('ID', anchor='center', width=80)
        self.tree.column('Livro', anchor='w', width=350)
        self.tree.column('Leitor', anchor='w', width=200)
        self.tree.column('DataReserva', anchor='center', width=150)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca dados no Controller
        reservas = processar_lista_reservas_ativas()
        
        if reservas:
            for item in reservas:
                data_reserva_str = item['Data_Reserva'].strftime('%d/%m/%Y')
                
                self.tree.insert('', 'end', values=(
                    item['Id_Reserva'], 
                    item['Titulo'], 
                    item['Leitor'], 
                    data_reserva_str
                ))
        else:
             self.tree.insert('', 'end', values=('', 'Nenhuma reserva ativa no momento.', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')

    def handle_atendimento(self):
        """Lida com a ação de atender uma reserva, transformando-a em empréstimo."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma reserva para atender.")
            return

        reserva_id = self.tree.item(selected_item, 'values')[0]
        livro_titulo = self.tree.item(selected_item, 'values')[1]

        confirm = messagebox.askyesno(
            "Confirmar Atendimento",
            f"Tem certeza que deseja ATENDER a reserva do livro '{livro_titulo}' (ID: {reserva_id})?\n\nIsso irá registrá-lo como um novo empréstimo."
        )

        if confirm:
            try:
                # 15 dias de prazo padrão para o empréstimo gerado
                data_retirada = datetime.now().strftime('%Y-%m-%d')
                data_dev_prev = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d') 

                sucesso, mensagem = processar_atendimento_reserva(reserva_id, data_retirada, data_dev_prev)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.load_data() # Recarrega a lista
                else:
                    messagebox.showerror("Erro de Atendimento", mensagem)

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    def handle_cancelamento(self):
        """Lida com a ação de cancelar uma reserva."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma reserva para cancelar.")
            return

        reserva_id = self.tree.item(selected_item, 'values')[0]
        livro_titulo = self.tree.item(selected_item, 'values')[1]

        confirm = messagebox.askyesno(
            "Confirmar Cancelamento",
            f"Tem certeza que deseja CANCELAR a reserva do livro '{livro_titulo}' (ID: {reserva_id})?"
        )

        if confirm:
            sucesso, mensagem = processar_cancelamento_reserva(reserva_id)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.load_data() # Recarrega a lista
            else:
                messagebox.showerror("Erro de Cancelamento", mensagem)