# Arquivo: view/acervo_view.py (ATUALIZADA COM CAMPOS OBRIGATÓRIOS DO BD)

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import (
    processar_lista_livros, 
    processar_adicao_livro, 
    processar_edicao_livro, 
    processar_exclusao_livro
)

class AcervoView(tk.Frame):
    """
    Módulo de visualização e gerenciamento do Acervo de Livros (CRUD).
    Disponível para perfis Administrador e Biblioteca.
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
        
        tk.Label(header_frame, text="GERENCIAMENTO DO ACERVO DE LIVROS", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Adicionar Novo", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Editar Selecionado", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Excluir Selecionado", command=self.handle_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Colunas ajustadas para refletir o BD
        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Titulo', 'Autor', 'Editora', 'ISBN', 'Ano', 'Genero', 'Classif', 'Exemplares'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Titulo', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Editora', text='Ed. ID') # Mostra apenas o ID por enquanto
        self.tree.heading('ISBN', text='ISBN')
        self.tree.heading('Ano', text='Ano')
        self.tree.heading('Genero', text='Gênero')
        self.tree.heading('Classif', text='Class.')
        self.tree.heading('Exemplares', text='Estoque') # Nome ajustado

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
                    livro['Numero_Exemplares'] # Nome da coluna ajustado
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhum livro cadastrado no acervo.', '', '', '', '', '', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')

    
    # --- Diálogos de Operação ---
    
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
        dialog.geometry("400x600") # Aumentado para caber mais campos
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
        
        # Editora ID * (Assume-se que você sabe o ID de uma editora já cadastrada)
        tk.Label(dialog, text="ID da Editora (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Editora_ID'] = tk.Entry(dialog, width=40)
        fields['Editora_ID'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Gênero *
        tk.Label(dialog, text="Gênero (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['genero'] = tk.Entry(dialog, width=40)
        fields['genero'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Classificação * (Ex: 1 a 5, ou idade)
        tk.Label(dialog, text="Classificação (Int) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['classificacao'] = tk.Entry(dialog, width=40)
        fields['classificacao'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Ano Publicação *
        tk.Label(dialog, text="Ano Publicação (Int) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Ano_Publicacao'] = tk.Entry(dialog, width=40)
        fields['Ano_Publicacao'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Quantidade (Estoque) * (Nome ajustado no código)
        tk.Label(dialog, text="Estoque (Num. Exemplares) (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Numero_Exemplares'] = tk.Entry(dialog, width=40)
        fields['Numero_Exemplares'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # ISBN (Opcional, mas útil)
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
            isbn = fields['ISBN'].get() or None # Permite NULL se vazio
            
            # Validação: Verifica os campos obrigatórios
            if not titulo or not autor or not qtd or not editora_id or not genero or not classificacao or not ano:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios (*).")
                return

            sucesso = False
            
            if is_edit:
                # U de CRUD
                book_id = data['Id_livro']
                sucesso = processar_edicao_livro(book_id, titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao)
                
            else:
                # C de CRUD
                sucesso = processar_adicao_livro(titulo, autor, isbn, ano, qtd, editora_id, genero, classificacao)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Livro {'atualizado' if is_edit else 'adicionado'} com sucesso!")
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", f"Falha ao {'atualizar' if is_edit else 'adicionar'} livro. Verifique se o ID da Editora existe e se todos os números são válidos.")
        
        # Botão Principal
        action_text = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR LIVRO"
        tk.Button(dialog, text=action_text, command=handle_action, width=25).grid(row=row+1, column=0, columnspan=2, pady=15)
            
        dialog.wait_window()

    # ... (handle_delete - SEM ALTERAÇÃO) ...

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