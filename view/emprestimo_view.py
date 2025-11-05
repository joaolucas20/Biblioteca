# Arquivo: view/emprestimo_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.biblioteca_controller import processar_busca_emprestados, processar_registro_emprestimo, processar_registro_devolucao

class EmprestimoView(tk.Frame):
    """
    Módulo de visualização e gerenciamento de empréstimos e devoluções.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Título e Botões de Ação
        self.create_header_and_actions()
        
        # 2. Frame do Treeview
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # 3. Treeview (Tabela)
        self.create_treeview()
        
        # 4. Carregar dados
        self.load_data()

    def create_header_and_actions(self):
        header_frame = tk.Frame(self)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        
        tk.Label(header_frame, text="GERENCIAMENTO DE EMPRÉSTIMOS", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Novo Empréstimo", command=self.open_emprestimo_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Registrar Devolução", command=self.open_devolucao_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        # Treeview com Scrollbar
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam") # Estilo moderno

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('Titulo', 'Leitor', 'Retirada', 'DevolucaoPrev'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('Titulo', text='Livro (Título)')
        self.tree.heading('Leitor', text='Leitor')
        self.tree.heading('Retirada', text='Data Retirada')
        self.tree.heading('DevolucaoPrev', text='Devolução Prevista')

        # Configurar larguras das colunas
        self.tree.column('Titulo', anchor='w', width=300)
        self.tree.column('Leitor', anchor='w', width=200)
        self.tree.column('Retirada', anchor='center', width=150)
        self.tree.column('DevolucaoPrev', anchor='center', width=150)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca dados no Controller
        emprestimos = processar_busca_emprestados()
        
        if emprestimos:
            for item in emprestimos:
                # Formata as datas para exibição
                data_retirada_str = item['Data_Retirada'].strftime('%d/%m/%Y')
                data_dev_prev_str = item['Data_Devolucao_Prev'].strftime('%d/%m/%Y')
                
                self.tree.insert('', 'end', values=(
                    item['Titulo'], 
                    item['Leitor'], 
                    data_retirada_str, 
                    data_dev_prev_str
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhum livro emprestado no momento.', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')


    # --- Diálogos de Operação ---
    
    def open_emprestimo_dialog(self):
        """Abre a janela para registrar um novo empréstimo."""
        # Garante a importação local de timedelta, caso falhe na global
        from datetime import datetime, timedelta 
        
        # Janela Toplevel para modal
        dialog = tk.Toplevel(self.master)
        dialog.title("Registrar Novo Empréstimo")
        dialog.geometry("300x350")
        dialog.transient(self.master)
        dialog.grab_set() 
        
        # --- Campos de Entrada ---
        tk.Label(dialog, text="ID do Usuário:").pack(pady=5)
        user_id_entry = tk.Entry(dialog)
        user_id_entry.pack(pady=2)

        tk.Label(dialog, text="ID do Livro:").pack(pady=5)
        livro_id_entry = tk.Entry(dialog)
        livro_id_entry.pack(pady=2)

        tk.Label(dialog, text="Data Retirada (DD/MM/AAAA):").pack(pady=5)
        data_retirada_entry = tk.Entry(dialog)
        data_retirada_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        data_retirada_entry.pack(pady=2)
        
        tk.Label(dialog, text="Devolução Prevista (DD/MM/AAAA):").pack(pady=5)
        data_dev_prev_entry = tk.Entry(dialog)
        # Exemplo de 7 dias de prazo
        next_week = datetime.now().date() + timedelta(days=7) 
        data_dev_prev_entry.insert(0, next_week.strftime('%d/%m/%Y'))
        data_dev_prev_entry.pack(pady=2)

        # --- Handler de Registro ---
        def handle_registro():
            try:
                usuario_id = int(user_id_entry.get())
                livro_id = int(livro_id_entry.get())
                # Converte o formato de exibição para o formato de BD
                data_retirada = datetime.strptime(data_retirada_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                data_dev_prev = datetime.strptime(data_dev_prev_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                
                # Chama o Controller para registrar no BD
                sucesso = processar_registro_emprestimo(usuario_id, livro_id, data_retirada, data_dev_prev)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
                    self.load_data()
                    dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Falha ao registrar empréstimo. Verifique os IDs ou a conexão.")

            except ValueError:
                messagebox.showerror("Erro", "IDs devem ser números inteiros e as datas devem estar no formato DD/MM/AAAA.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        # --- BOTÃO QUE CHAMA O REGISTRO ---
        tk.Button(dialog, text="REGISTRAR", command=handle_registro, width=20).pack(pady=15)
        
        # Garante que o diálogo fique visível
        dialog.wait_window()
        
    def open_devolucao_dialog(self):
        """Abre a janela para registrar uma devolução."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Registrar Devolução")
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set() 
        
        tk.Label(dialog, text="ID do Livro:").pack(pady=5)
        livro_id_entry = tk.Entry(dialog)
        livro_id_entry.pack(pady=2)

        tk.Label(dialog, text="ID do Usuário (quem pegou):").pack(pady=5)
        user_id_entry = tk.Entry(dialog)
        user_id_entry.pack(pady=2)

        tk.Label(dialog, text="Data Devolução (DD/MM/AAAA):").pack(pady=5)
        data_dev_entry = tk.Entry(dialog)
        data_dev_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        data_dev_entry.pack(pady=2)

        def handle_registro():
            try:
                livro_id = int(livro_id_entry.get())
                usuario_id = int(user_id_entry.get())
                data_devolucao = datetime.strptime(data_dev_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                
                sucesso = processar_registro_devolucao(livro_id, usuario_id, data_devolucao)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
                    self.load_data()
                    dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Falha ao registrar devolução. Verifique os IDs ou o empréstimo ativo.")

            except ValueError:
                messagebox.showerror("Erro", "IDs devem ser números inteiros e a data deve estar no formato DD/MM/AAAA.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        tk.Button(dialog, text="REGISTRAR DEVOLUÇÃO", command=handle_registro, width=25).pack(pady=15)