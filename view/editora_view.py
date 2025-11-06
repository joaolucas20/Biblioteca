# Arquivo: view/editora_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import (
    processar_lista_editoras, 
    processar_adicao_editora, 
    processar_edicao_editora, 
    processar_exclusao_editora
)

class EditoraView(tk.Frame):
    """
    Módulo de visualização e gerenciamento do CRUD de Editoras.
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
        
        tk.Label(header_frame, text="GERENCIAMENTO DE EDITORAS", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Adicionar Nova", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Editar Selecionada", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Excluir Selecionada", command=self.handle_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        style = ttk.Style(self.tree_frame)
        style.theme_use("clam")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Nome', 'Endereco', 'Telefone'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Endereco', text='Endereço')
        self.tree.heading('Telefone', text='Telefone')

        self.tree.column('ID', anchor='center', width=50)
        self.tree.column('Nome', anchor='w', width=200)
        self.tree.column('Endereco', anchor='w', width=350)
        self.tree.column('Telefone', anchor='center', width=120)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca dados no Controller (R de CRUD)
        editoras = processar_lista_editoras()
        
        if editoras:
            for editora in editoras:
                self.tree.insert('', 'end', values=(
                    editora['Id_Editora'], 
                    editora['Nome'], 
                    editora['Endereco'], 
                    editora['Telefone']
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhuma editora cadastrada.', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')

    
    # --- Diálogos de Operação ---
    
    def open_add_dialog(self):
        """Abre a janela para adicionar uma nova editora."""
        self._open_editora_dialog(title="Adicionar Nova Editora", is_edit=False)

    def open_edit_dialog(self):
        """Abre a janela para editar uma editora existente."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma editora na lista para editar.")
            return

        # Pega os dados atuais do item selecionado
        current_values = self.tree.item(selected_item, 'values')
        editora_data = {
            'Id_Editora': current_values[0],
            'Nome': current_values[1],
            'Endereco': current_values[2],
            'Telefone': current_values[3]
        }
        self._open_editora_dialog(title=f"Editar Editora ID: {editora_data['Id_Editora']}", is_edit=True, data=editora_data)
        
    
    def _open_editora_dialog(self, title, is_edit, data=None):
        """Função auxiliar para criar os diálogos de Adicionar/Editar Editora."""
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("400x350")
        dialog.transient(self.master)
        dialog.grab_set() 
        
        # --- CAMPOS ---
        fields = {}
        row = 0

        # Nome
        tk.Label(dialog, text="Nome (*):").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Nome'] = tk.Entry(dialog, width=40)
        fields['Nome'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Endereço
        tk.Label(dialog, text="Endereço:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Endereco'] = tk.Entry(dialog, width=40)
        fields['Endereco'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Telefone
        tk.Label(dialog, text="Telefone:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Telefone'] = tk.Entry(dialog, width=40)
        fields['Telefone'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Preencher dados se for Edição
        if is_edit and data:
            fields['Nome'].insert(0, data['Nome'])
            fields['Endereco'].insert(0, data['Endereco'] if data['Endereco'] else "")
            fields['Telefone'].insert(0, data['Telefone'] if data['Telefone'] else "")
            
        # --- HANDLERS E BOTÕES ---
        
        def handle_action():
            nome = fields['Nome'].get()
            endereco = fields['Endereco'].get() or None # O BD aceita NULL
            telefone = fields['Telefone'].get() or None # O BD aceita NULL
            
            if not nome:
                messagebox.showerror("Erro", "O Nome da Editora é obrigatório.")
                return

            sucesso = False
            
            if is_edit:
                # U de CRUD
                editora_id = data['Id_Editora']
                sucesso = processar_edicao_editora(editora_id, nome, endereco, telefone)
                
            else:
                # C de CRUD
                sucesso = processar_adicao_editora(nome, endereco, telefone)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Editora {'atualizada' if is_edit else 'adicionada'} com sucesso!")
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", f"Falha ao {'atualizar' if is_edit else 'adicionar'} editora.")
        
        # Botão Principal
        action_text = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR EDITORA"
        tk.Button(dialog, text=action_text, command=handle_action, width=25).grid(row=row+1, column=0, columnspan=2, pady=15)
            
        dialog.wait_window()

    def handle_delete(self):
        """Lida com a exclusão de uma editora selecionada (D de CRUD)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma editora na lista para excluir.")
            return

        editora_id = self.tree.item(selected_item, 'values')[0]
        editora_nome = self.tree.item(selected_item, 'values')[1]
        
        confirm = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja EXCLUIR a editora '{editora_nome}' (ID: {editora_id})?\n\nATENÇÃO: Isso falhará se houver livros cadastrados que dependem desta editora (Regra de integridade do BD)."
        )

        if confirm:
            sucesso = processar_exclusao_editora(editora_id)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Editora '{editora_nome}' excluída com sucesso.")
                self.load_data()
            else:
                messagebox.showerror("Erro", "Falha ao excluir. Esta editora está associada a um ou mais livros no acervo, impedindo a exclusão (Chave Estrangeira).")