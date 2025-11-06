# Arquivo: view/usuario_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.biblioteca_controller import (
    processar_lista_usuarios, 
    processar_adicao_usuario, 
    processar_edicao_usuario, 
    processar_exclusao_usuario, 
    processar_reset_senha
)

class UsuarioView(tk.Frame):
    """
    Módulo de visualização e gerenciamento de Usuários (CRUD).
    Disponível apenas para perfis Administradores.
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
        
        tk.Label(header_frame, text="GERENCIAMENTO DE USUÁRIOS", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
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

        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Nome', 'Tipo', 'Telefone', 'Email'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Nome', text='Nome Completo')
        self.tree.heading('Tipo', text='Perfil')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Email', text='Email')

        self.tree.column('ID', anchor='center', width=50)
        self.tree.column('Nome', anchor='w', width=200)
        self.tree.column('Tipo', anchor='center', width=80)
        self.tree.column('Telefone', anchor='w', width=120)
        self.tree.column('Email', anchor='w', width=200)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca dados no Controller (R de CRUD)
        usuarios = processar_lista_usuarios()
        
        if usuarios:
            for user in usuarios:
                self.tree.insert('', 'end', values=(
                    user['Id_Usuario'], 
                    user['Nome'], 
                    user['Tipo'], 
                    user['Telefone'], 
                    user['Email']
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhum usuário cadastrado.', '', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')

    
    # --- Diálogos de Operação ---
    
    def open_add_dialog(self):
        """Abre a janela para adicionar um novo usuário."""
        self._open_user_dialog(title="Adicionar Novo Usuário", is_edit=False)

    def open_edit_dialog(self):
        """Abre a janela para editar um usuário existente."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para editar.")
            return

        # Pega os dados atuais do item selecionado
        current_values = self.tree.item(selected_item, 'values')
        user_data = {
            'Id_Usuario': current_values[0],
            'Nome': current_values[1],
            'Tipo': current_values[2],
            'Telefone': current_values[3],
            'Email': current_values[4]
        }
        self._open_user_dialog(title=f"Editar Usuário ID: {user_data['Id_Usuario']}", is_edit=True, data=user_data)
        
    
    def _open_user_dialog(self, title, is_edit, data=None):
        """Função auxiliar para criar os diálogos de Adicionar/Editar."""
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("400x450" if not is_edit else "400x400")
        dialog.transient(self.master)
        dialog.grab_set() 
        
        # Tipos de perfil disponíveis
        TIPOS = ['Leitor', 'Biblioteca', 'Adm']

        # --- CAMPOS ---
        fields = {}
        row = 0

        # Nome
        tk.Label(dialog, text="Nome:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Nome'] = tk.Entry(dialog, width=40)
        fields['Nome'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Email
        tk.Label(dialog, text="Email:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Email'] = tk.Entry(dialog, width=40)
        fields['Email'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Telefone
        tk.Label(dialog, text="Telefone:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Telefone'] = tk.Entry(dialog, width=40)
        fields['Telefone'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Tipo
        tk.Label(dialog, text="Perfil (Tipo):").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
        fields['Tipo'] = ttk.Combobox(dialog, values=TIPOS, state='readonly', width=38)
        fields['Tipo'].set(TIPOS[0]) # Default Leitor
        fields['Tipo'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Senha (Apenas em Adicionar)
        if not is_edit:
            tk.Label(dialog, text="Senha Inicial:").grid(row=row, column=0, sticky='w', padx=10, pady=5); row+=1
            fields['Senha'] = tk.Entry(dialog, show="*", width=40)
            fields['Senha'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Preencher dados se for Edição
        if is_edit and data:
            fields['Nome'].insert(0, data['Nome'])
            fields['Email'].insert(0, data['Email'])
            fields['Telefone'].insert(0, data['Telefone'])
            fields['Tipo'].set(data['Tipo'])
            
        # --- HANDLERS E BOTÕES ---
        
        def handle_action():
            nome = fields['Nome'].get()
            email = fields['Email'].get()
            telefone = fields['Telefone'].get()
            tipo = fields['Tipo'].get()
            
            if not nome or not email or not tipo:
                messagebox.showerror("Erro", "Nome, Email e Perfil são obrigatórios.")
                return

            sucesso = False
            
            if is_edit:
                # U de CRUD
                user_id = data['Id_Usuario']
                sucesso = processar_edicao_usuario(user_id, nome, tipo, telefone, email)
                
            else:
                # C de CRUD
                senha = fields['Senha'].get()
                if not senha:
                    messagebox.showerror("Erro", "A Senha Inicial é obrigatória para novos usuários.")
                    return
                sucesso = processar_adicao_usuario(nome, tipo, telefone, email, senha)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário {'atualizado' if is_edit else 'adicionado'} com sucesso!")
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", f"Falha ao {'atualizar' if is_edit else 'adicionar'} usuário. Verifique os dados.")
        
        # Botão Principal
        action_text = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR USUÁRIO"
        tk.Button(dialog, text=action_text, command=handle_action, width=25).grid(row=row+1, column=0, columnspan=2, pady=15)
        
        # Botão Resetar Senha (Apenas em Edição)
        if is_edit:
            tk.Button(dialog, text="Resetar Senha", command=lambda: self.open_reset_senha_dialog(data['Id_Usuario']), width=25, bg='orange').grid(row=row+2, column=0, columnspan=2, pady=5)
            
        dialog.wait_window()

    def handle_delete(self):
        """Lida com a exclusão de um usuário selecionado (D de CRUD)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para excluir.")
            return

        user_id = self.tree.item(selected_item, 'values')[0]
        user_nome = self.tree.item(selected_item, 'values')[1]
        
        confirm = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja EXCLUIR o usuário '{user_nome}' (ID: {user_id})?\n\nEsta ação é irreversível!"
        )

        if confirm:
            sucesso = processar_exclusao_usuario(user_id)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário {user_nome} excluído com sucesso.")
                self.load_data()
            else:
                messagebox.showerror("Erro", "Falha ao excluir. Verifique se o usuário possui empréstimos ou reservas ativas (dependendo das regras do BD).")

    def open_reset_senha_dialog(self, user_id):
        """Abre o diálogo para redefinir a senha do usuário."""
        reset_dialog = tk.Toplevel(self.master)
        reset_dialog.title(f"Resetar Senha (ID: {user_id})")
        reset_dialog.geometry("300x150")
        reset_dialog.transient(self.master)
        reset_dialog.grab_set()

        tk.Label(reset_dialog, text="Nova Senha:").pack(pady=5)
        nova_senha_entry = tk.Entry(reset_dialog, show="*")
        nova_senha_entry.pack(pady=2)

        def handle_reset():
            nova_senha = nova_senha_entry.get()
            if not nova_senha:
                messagebox.showerror("Erro", "A nova senha não pode ser vazia.")
                return

            sucesso = processar_reset_senha(user_id, nova_senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Senha redefinida com sucesso.")
                reset_dialog.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao redefinir a senha.")

        tk.Button(reset_dialog, text="SALVAR NOVA SENHA", command=handle_reset, width=20, bg='green', fg='white').pack(pady=10)
        reset_dialog.wait_window()