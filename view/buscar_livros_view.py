# Arquivo: view/buscar_livros_view.py (ATUALIZADO COM RESERVA)

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import processar_busca_livros, processar_registro_emprestimo, processar_reserva 
# CORREÇÃO: Importa datetime e timedelta
from datetime import datetime, timedelta

class BuscarLivrosView(tk.Frame):
    """
    Módulo para o Leitor buscar e visualizar livros no acervo e solicitar empréstimos/reservas.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        tk.Label(self, text="🔍 BUSCAR LIVROS NO ACERVO", font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.create_search_frame(self)
        
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.create_treeview()
        
        # Frame para os botões de Ação
        action_frame = tk.Frame(self)
        action_frame.grid(row=3, column=0, sticky='w', pady=10, padx=10)

        # Botão de Empréstimo
        tk.Button(action_frame, text="✅ Realizar Empréstimo", 
                  command=self.handle_emprestimo, 
                  bg='#28a745', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        # Botão de Reserva (NOVO)
        tk.Button(action_frame, text="⏳ Solicitar Reserva", 
                  command=self.handle_reserva, 
                  bg='#ffc107', fg='black', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.load_data()

    # ... (create_search_frame e create_treeview - SEM ALTERAÇÃO) ...

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

        self.tree = ttk.Treeview(self.tree_frame, columns=('Id', 'Titulo', 'Autor', 'Genero', 'Estoque'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Id', text='ID')
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Genero', text='Gênero')
        self.tree.heading('Estoque', text='Disponibilidade')

        self.tree.column('Id', width=0, stretch=tk.NO) 
        self.tree.column('Titulo', anchor='w', width=350)
        self.tree.column('Autor', anchor='w', width=180)
        self.tree.column('Genero', anchor='w', width=150)
        self.tree.column('Estoque', anchor='center', width=120)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)


    def load_data(self):
        # ... (código inalterado) ...
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
                    estoque_text = "Indisponível (Reservar)"
                    
                self.tree.insert('', 'end', 
                                 values=(livro['Id_livro'], livro['Titulo'], livro['Autor'], livro['genero'], estoque_text), 
                                 tags=(tag,))
                                 
            self.tree.tag_configure('disponivel', foreground='green')
            self.tree.tag_configure('indisponivel', foreground='red', font=('Arial', 9, 'bold'))

        else:
             self.tree.insert('', 'end', values=('', 'Nenhum livro encontrado ou acervo vazio.', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='blue')


    def handle_emprestimo(self):
        """Lida com a solicitação de empréstimo (só funciona se houver estoque)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para solicitar o empréstimo.")
            return

        values = self.tree.item(selected_item, 'values')
        livro_id = int(values[0])
        titulo = values[1]
        estoque_text = values[4] 

        if "Indisponível" in estoque_text:
            messagebox.showwarning("Atenção", f"O livro '{titulo}' está indisponível para empréstimo. Tente solicitar a reserva.")
            return

        confirm = messagebox.askyesno(
            "Confirmação de Empréstimo",
            f"Deseja confirmar o empréstimo do livro '{titulo}'?"
        )

        if confirm:
            try:
                data_retirada = datetime.now().strftime('%Y-%m-%d')
                data_dev_prev = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d') 
                
                usuario_id = self.user_data['Id_Usuario']
                
                sucesso = processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Empréstimo de '{titulo}' registrado com sucesso!")
                    self.load_data() 
                else:
                    messagebox.showerror("Erro", "Falha ao registrar empréstimo. Verifique regras de empréstimo ou estoque.")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro interno: {e}")

    def handle_reserva(self):
        """NOVO: Lida com a solicitação de reserva (só funciona se não houver estoque)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para solicitar a reserva.")
            return

        values = self.tree.item(selected_item, 'values')
        livro_id = int(values[0])
        titulo = values[1]
        estoque_text = values[4] 

        # A reserva só faz sentido se o livro estiver indisponível
        if "Disponível" in estoque_text:
            messagebox.showwarning("Atenção", "O livro está disponível para empréstimo imediato. Não é necessário reservar.")
            return
            
        confirm = messagebox.askyesno(
            "Confirmação de Reserva",
            f"Deseja confirmar a reserva do livro '{titulo}'?"
        )

        if confirm:
            usuario_id = self.user_data['Id_Usuario']
            # Chama a nova função do Controller
            sucesso, mensagem = processar_reserva(usuario_id, livro_id)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Atenção", mensagem)
