# Arquivo: view/acervo_view.py (FINAL COMPLETO E CORRIGIDO)

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import (
    processar_lista_livros, 
    processar_adicao_livro, 
    processar_edicao_livro, 
    processar_exclusao_livro,
    processar_historico_livro 
)

class AcervoView(tk.Frame):
    """
    Módulo de visualização e gerenciamento do Acervo de Livros (CRUD), 
    incluindo consulta de histórico.
    """
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        style = ttk.Style(self)
        style.theme_use("clam")
        
        self.create_header_and_actions()
        
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.create_treeview()
        self.load_data()

    def create_header_and_actions(self):
        header_frame = tk.Frame(self)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(header_frame, 
                 text="📚 GERENCIAMENTO DO ACERVO DE LIVROS", 
                 font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='ew', padx=10)
        
        btn_frame = tk.Frame(header_frame)
        btn_frame.grid(row=1, column=0, sticky='w', pady=(10, 0))

        # Botões de CRUD
        ttk.Button(btn_frame, text="Adicionar Novo", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar Selecionado", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Selecionado", command=self.handle_delete).pack(side=tk.LEFT, padx=5)
        
        # Botão de Consulta de Status/Histórico
        ttk.Button(btn_frame, text="🔍 Ver Status/Histórico", command=self.open_historico_dialog).pack(side=tk.LEFT, padx=(20, 5))
        
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Titulo', 'Autor', 'Editora', 'ISBN', 'Ano', 'Genero', 'Classif', 'Exemplares'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Editora', text='Ed. ID')
        self.tree.heading('ISBN', text='ISBN')
        self.tree.heading('Ano', text='Ano')
        self.tree.heading('Genero', text='Gênero')
        self.tree.heading('Classif', text='Class.')
        self.tree.heading('Exemplares', text='Estoque')

        self.tree.column('ID', anchor='center', width=40)
        self.tree.column('Titulo', anchor='w', width=200)
        self.tree.column('Autor', anchor='w', width=150)
        self.tree.column('Editora', anchor='center', width=50)
        self.tree.column('ISBN', anchor='center', width=100)
        self.tree.column('Ano', anchor='center', width=60)
        self.tree.column('Genero', anchor='w', width=80)
        self.tree.column('Classif', anchor='center', width=60)
        self.tree.column('Exemplares', anchor='center', width=70)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        livros = processar_lista_livros()
        
        if livros:
            for livro in livros:
                self.tree.insert('', 'end', values=(
                    livro['Id_livro'], 
                    livro['Titulo'], 
                    livro['Autor'], 
                    livro['Editora_ID'], 
                    livro['ISBN'], 
                    livro['Ano_Publicacao'], 
                    livro['genero'],
                    livro['classificacao'],
                    livro['Numero_Exemplares']
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhum livro cadastrado no acervo.', '', '', '', '', '', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')

    
    # --- Diálogos de Operação (CRUD) ---
    
    def open_add_dialog(self):
        """Abre a janela para adicionar um novo livro."""
        self._open_book_dialog(title="Adicionar Novo Livro", is_edit=False)

    def open_edit_dialog(self):
        """Abre a janela para editar um livro existente."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para editar.")
            return

        current_values = self.tree.item(selected_item, 'values')
        book_data = {
            'Id_livro': current_values[0],
            'Titulo': current_values[1],
            'Autor': current_values[2],
            'Editora_ID': current_values[3],
            'ISBN': current_values[4],
            'Ano_Publicacao': current_values[5],
            'genero': current_values[6],
            'classificacao': current_values[7],
            'Numero_Exemplares': current_values[8]
        }
        self._open_book_dialog(title=f"Editar Livro ID: {book_data['Id_livro']}", is_edit=True, data=book_data)
        
    
    def _open_book_dialog(self, title, is_edit, data=None):
        """Função auxiliar para criar os diálogos de Adicionar/Editar Livro."""
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("400x600") 
        dialog.transient(self.master)
        dialog.grab_set() 
        
        # --- CAMPOS ---
        fields = {}
        row = 0
        
        tk.Label(dialog, text="Campos Obrigatórios são marcados com (*)", fg='red').grid(row=row, column=0, columnspan=2, padx=10, pady=5); row+=1

        # Título *
        tk.Label(dialog, text="Título (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Titulo'] = tk.Entry(dialog, width=40)
        fields['Titulo'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Autor *
        tk.Label(dialog, text="Autor (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Autor'] = tk.Entry(dialog, width=40)
        fields['Autor'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Editora ID *
        tk.Label(dialog, text="ID da Editora (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Editora_ID'] = tk.Entry(dialog, width=40)
        fields['Editora_ID'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Gênero *
        tk.Label(dialog, text="Gênero (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['genero'] = tk.Entry(dialog, width=40)
        fields['genero'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Classificação *
        tk.Label(dialog, text="Classificação (Int) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['classificacao'] = tk.Entry(dialog, width=40)
        fields['classificacao'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Ano Publicação *
        tk.Label(dialog, text="Ano Publicação (Int) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Ano_Publicacao'] = tk.Entry(dialog, width=40)
        fields['Ano_Publicacao'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Quantidade (Estoque) *
        tk.Label(dialog, text="Estoque (Num. Exemplares) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Numero_Exemplares'] = tk.Entry(dialog, width=40)
        fields['Numero_Exemplares'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # ISBN (Opcional)
        tk.Label(dialog, text="ISBN (Opcional):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['ISBN'] = tk.Entry(dialog, width=40)
        fields['ISBN'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Preencher dados se for Edição
        if is_edit and data:
            fields['Titulo'].insert(0, data['Titulo'])
            fields['Autor'].insert(0, data['Autor'])
            fields['Editora_ID'].insert(0, data['Editora_ID'])
            fields['genero'].insert(0, data['genero'])
            fields['classificacao'].insert(0, data['classificacao'])
            fields['Ano_Publicacao'].insert(0, data['Ano_Publicacao'])
            fields['Numero_Exemplares'].insert(0, data['Numero_Exemplares'])
            fields['ISBN'].insert(0, data['ISBN'])
            
        # --- HANDLERS E BOTÕES ---
        
        def handle_action():
            titulo = fields['Titulo'].get()
            autor = fields['Autor'].get()
            editora_id = fields['Editora_ID'].get()
            genero = fields['genero'].get()
            classificacao = fields['classificacao'].get()
            ano = fields['Ano_Publicacao'].get()
            qtd = fields['Numero_Exemplares'].get()
            isbn = fields['ISBN'].get() or None 
            
            if not titulo or not autor or not qtd or not editora_id or not genero or not classificacao or not ano:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios (*).")
                return

            sucesso = False
            
            if is_edit:
                book_id = data['Id_livro']
                sucesso = processar_edicao_livro(book_id, titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao)
                
            else:
                sucesso = processar_adicao_livro(titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Livro {'atualizado' if is_edit else 'adicionado'} com sucesso!")
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", f"Falha ao {'atualizar' if is_edit else 'adicionar'} livro. Verifique se o ID da Editora existe e se todos os números são válidos.")
        
        # Botão Principal (Usando ttk.Button para estilo)
        action_text = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR LIVRO"
        ttk.Button(dialog, text=action_text, command=handle_action).grid(row=row+1, column=0, columnspan=2, pady=15)
            
        dialog.wait_window()

    def handle_delete(self):
        """Lida com a exclusão de um livro selecionado (D de CRUD)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para excluir.")
            return

        book_id = self.tree.item(selected_item, 'values')[0]
        book_titulo = self.tree.item(selected_item, 'values')[1]
        
        confirm = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja EXCLUIR o livro '{book_titulo}' (ID: {book_id})?\n\nEsta ação pode falhar se houver empréstimos ativos ou pendentes relacionados a este ID."
        )

        if confirm:
            sucesso = processar_exclusao_livro(book_id)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Livro '{book_titulo}' excluído com sucesso.")
                self.load_data()
            else:
                messagebox.showerror("Erro", "Falha ao excluir. O livro pode estar envolvido em empréstimos ativos ou reservas, impedindo a exclusão (regra de integridade do BD).")

    # --- NOVO DIÁLOGO: STATUS E HISTÓRICO ---
    def open_historico_dialog(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na lista para ver o histórico.")
            return

        current_values = self.tree.item(selected_item, 'values')
        livro_id = current_values[0]
        titulo = current_values[1]
        
        # Busca Histórico e Status no Controller
        historico, status_atual = processar_historico_livro(livro_id)

        dialog = tk.Toplevel(self.master)
        dialog.title(f"Status e Histórico: {titulo} (ID: {livro_id})")
        dialog.geometry("700x500") 
        dialog.transient(self.master)
        dialog.grab_set() 
        
        # Frame de Status Atual
        status_frame = tk.LabelFrame(dialog, text="Status Atual", padx=10, pady=10, bg='#e0f7fa')
        status_frame.pack(fill='x', padx=15, pady=15)
        
        # Mensagem de Status
        status_msg = "Disponível em Estoque"
        status_cor = 'green'
        
        if status_atual['ativo']:
            status_msg = status_atual['status_msg']
            status_cor = 'red' if status_atual['atrasado'] else '#005a8d'
        
        tk.Label(status_frame, text=f"Situação: {status_msg}", 
                 font=("Arial", 12, "bold"), fg=status_cor, bg='#e0f7fa').pack(anchor='w')
        
        # Frame do Histórico
        hist_frame = tk.LabelFrame(dialog, text="Histórico de Empréstimos", padx=10, pady=10)
        hist_frame.pack(fill='both', expand=True, padx=15, pady=5)
        hist_frame.grid_rowconfigure(0, weight=1)
        hist_frame.grid_columnconfigure(0, weight=1)

        # Treeview de Histórico
        hist_tree = ttk.Treeview(hist_frame, columns=('Leitor', 'Retirada', 'DevolucaoPrev', 'DevolucaoEfet'), show='headings')
        
        hist_tree.heading('Leitor', text='Leitor')
        hist_tree.heading('Retirada', text='Retirada')
        hist_tree.heading('DevolucaoPrev', text='Dev. Prevista')
        hist_tree.heading('DevolucaoEfet', text='Dev. Efetiva')
        
        hist_tree.column('Leitor', width=150, anchor='w')
        hist_tree.column('Retirada', width=120, anchor='center')
        hist_tree.column('DevolucaoPrev', width=120, anchor='center')
        hist_tree.column('DevolucaoEfet', width=120, anchor='center')

        hist_tree.grid(row=0, column=0, sticky='nsew')

        # Preencher Histórico
        if historico:
            for item in historico:
                # O objeto datetime precisa ser formatado (assumindo que o Model retorna datetime objects)
                from datetime import date 
                
                data_retirada = item['Data_Retirada'].strftime('%d/%m/%Y')
                data_prev = item['Data_Devolucao_Prev'].strftime('%d/%m/%Y')
                data_efet = item['Data_Devolucao_efet'].strftime('%d/%m/%Y') if item['Data_Devolucao_efet'] else 'EMPRÉSTIMO ATIVO'
                
                tag = 'ativo' if item['Data_Devolucao_efet'] is None else ''
                
                hist_tree.insert('', 'end', values=(
                    item['Leitor'], 
                    data_retirada, 
                    data_prev, 
                    data_efet
                ), tags=(tag,))
                
            hist_tree.tag_configure('ativo', background='#fff3cd', foreground='#856404', font=('Arial', 9, 'bold'))
        else:
             tk.Label(hist_frame, text="Nenhum histórico de empréstimo encontrado para este livro.").grid(row=0, column=0)
             
        dialog.wait_window()