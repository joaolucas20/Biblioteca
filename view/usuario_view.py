# Arquivo: view/usuario_view.py (FINAL COMPLETO COM DIÁLOGOS PADRONIZADOS)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from controller.biblioteca_controller import (
    processar_lista_usuarios, 
    processar_adicao_usuario, 
    processar_edicao_usuario, 
    processar_exclusao_usuario, 
    processar_reset_senha,
    processar_historico_usuario 
)

class UsuarioView(tk.Frame):
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

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
                 text="👥 GERENCIAMENTO DE USUÁRIOS", 
                 font=("Arial", 16, "bold"), fg='#005a8d').grid(row=0, column=0, sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=1, column=0, sticky='ew', padx=10)
        
        btn_frame = tk.Frame(header_frame)
        btn_frame.grid(row=1, column=0, sticky='w', pady=(10, 0))

        # Botões de CRUD e Reset
        ttk.Button(btn_frame, text="Adicionar Novo", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar Selecionado", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Selecionado", command=self.handle_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Resetar Senha", command=self.handle_reset_senha).pack(side=tk.LEFT, padx=5)
        
        # Botão de Histórico 
        ttk.Button(btn_frame, text="📜 Ver Histórico de Livros", command=self.open_historico_dialog).pack(side=tk.LEFT, padx=(20, 5))
        
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(self.tree_frame, columns=('ID', 'Nome', 'Tipo', 'Telefone', 'Email', 'Endereco'), show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID', anchor='center')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Endereco', text='Endereço')

        self.tree.column('ID', anchor='center', width=50)
        self.tree.column('Nome', anchor='w', width=150)
        self.tree.column('Tipo', anchor='center', width=70)
        self.tree.column('Telefone', anchor='center', width=100)
        self.tree.column('Email', anchor='w', width=200)
        self.tree.column('Endereco', anchor='w', width=200)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.tree.yview)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        usuarios = processar_lista_usuarios()
        
        if usuarios:
            for user in usuarios:
                self.tree.insert('', 'end', values=(
                    user['Id_Usuario'], 
                    user['Nome'], 
                    user['Tipo'], 
                    user['Telefone'], 
                    user['Email'],
                    user['Endereco']
                ))
        else:
             self.tree.insert('', 'end', values=('Nenhum usuário cadastrado.', '', '', '', '', ''), tags=('empty',))
             self.tree.tag_configure('empty', foreground='red')
             
    # --- Diálogos de Operação (CRUD) ---
    
    def open_add_dialog(self):
        """Abre a janela para adicionar um novo usuário (C de CRUD)."""
        self._open_user_dialog(title="Adicionar Novo Usuário", is_edit=False)

    def open_edit_dialog(self):
        """Abre a janela para editar um usuário existente (U de CRUD)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para editar.")
            return

        current_values = self.tree.item(selected_item, 'values')
        user_data = {
            'Id_Usuario': current_values[0],
            'Nome': current_values[1],
            'Tipo': current_values[2],
            'Telefone': current_values[3],
            'Email': current_values[4],
            'Endereco': current_values[5],
        }
        self._open_user_dialog(title=f"Editar Usuário ID: {user_data['Id_Usuario']}", is_edit=True, data=user_data)

    def _open_user_dialog(self, title, is_edit, data=None):
        """Função auxiliar para criar os diálogos de Adicionar/Editar Usuário."""
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("400x550")
        dialog.transient(self.master)
        dialog.grab_set() 

        dialog.columnconfigure(0, weight=1)
        dialog.columnconfigure(1, weight=1)
        
        # --- CAMPOS ---
        fields = {}
        row = 0

        tk.Label(dialog, text="Campos Obrigatórios (*)", fg='red').grid(row=row, column=0, columnspan=2, padx=10, pady=5); row+=1

        # Nome *
        tk.Label(dialog, text="Nome (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Nome'] = tk.Entry(dialog, width=40)
        fields['Nome'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Tipo * (Dropdown)
        tk.Label(dialog, text="Tipo (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Tipo'] = ttk.Combobox(dialog, values=['Leitor', 'Biblioteca', 'Adm'], width=38, state='readonly')
        fields['Tipo'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Telefone *
        tk.Label(dialog, text="Telefone (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Telefone'] = tk.Entry(dialog, width=40)
        fields['Telefone'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Email *
        tk.Label(dialog, text="Email (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Email'] = tk.Entry(dialog, width=40)
        fields['Email'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Endereço *
        tk.Label(dialog, text="Endereço (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
        fields['Endereco'] = tk.Entry(dialog, width=40)
        fields['Endereco'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1

        # Senha (apenas para Adição)
        if not is_edit:
            tk.Label(dialog, text="Senha (*):").grid(row=row, column=0, sticky='w', padx=10, pady=2); row+=1
            fields['Senha'] = tk.Entry(dialog, show='*', width=40)
            fields['Senha'].grid(row=row, column=0, columnspan=2, padx=10, pady=2); row+=1
        
        # Preencher dados se for Edição
        if is_edit and data:
            fields['Nome'].insert(0, data['Nome'])
            fields['Tipo'].set(data['Tipo'])
            fields['Telefone'].insert(0, data['Telefone'])
            fields['Email'].insert(0, data['Email'])
            fields['Endereco'].insert(0, data['Endereco'])
            
        # --- HANDLERS E BOTÕES ---
        
        def handle_action():
            nome = fields['Nome'].get()
            tipo = fields['Tipo'].get()
            telefone = fields['Telefone'].get()
            email = fields['Email'].get()
            endereco = fields['Endereco'].get()
            
            if not all([nome, tipo, telefone, email, endereco]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios (*).")
                return

            sucesso = False
            mensagem = ""
            
            if is_edit:
                user_id = data['Id_Usuario']
                sucesso = processar_edicao_usuario(user_id, nome, tipo, telefone, email, endereco)
                
            else:
                senha = fields['Senha'].get()
                if not senha:
                    messagebox.showerror("Erro", "A senha é obrigatória para o cadastro.")
                    return
                sucesso, mensagem = processar_adicao_usuario(nome, tipo, telefone, email, senha, endereco)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário {'atualizado' if is_edit else 'adicionado'} com sucesso!")
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", mensagem or f"Falha ao {'atualizar' if is_edit else 'adicionar'} usuário. Verifique os dados.")
        
        # Botão Principal 
        action_text = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR USUÁRIO"
        ttk.Button(dialog, text=action_text, command=handle_action).grid(row=row+1, column=0, columnspan=2, pady=15)
            
        dialog.wait_window()

    def handle_delete(self):
        """Lida com a exclusão de um usuário selecionado (D de CRUD)."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para excluir.")
            return

        user_id = self.tree.item(selected_item, 'values')[0]
        user_nome = self.tree.item(selected_item, 'values')[1]
        
        if int(user_id) == self.user_data['Id_Usuario']:
            messagebox.showwarning("Erro", "Você não pode excluir sua própria conta enquanto estiver logado.")
            return

        confirm = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja EXCLUIR o usuário '{user_nome}' (ID: {user_id})?\n\nEsta ação pode falhar se houver empréstimos ou reservas ativas associadas a este ID."
        )

        if confirm:
            sucesso = processar_exclusao_usuario(user_id)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário {user_nome} excluído com sucesso.")
                self.load_data()
            else:
                messagebox.showerror("Erro", "Falha ao excluir. O usuário pode possuir empréstimos ou reservas ativas, impedindo a exclusão (regra de integridade do BD).")

    def handle_reset_senha(self):
        """Prepara o ID do usuário para o reset de senha."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para resetar a senha.")
            return
            
        user_id = self.tree.item(selected_item, 'values')[0]
        self.open_reset_senha_dialog(user_id)

    def open_reset_senha_dialog(self, user_id):
        """Abre o diálogo para redefinir a senha do usuário."""
        reset_dialog = tk.Toplevel(self.master)
        reset_dialog.title(f"Resetar Senha (ID: {user_id})")
        reset_dialog.geometry("300x150")
        reset_dialog.transient(self.master)
        reset_dialog.grab_set()

        reset_dialog.columnconfigure(0, weight=1)
        reset_dialog.columnconfigure(1, weight=1)
        row = 0

        tk.Label(reset_dialog, text="Nova Senha:").grid(row=row, column=0, columnspan=2, pady=5); row+=1
        nova_senha_entry = tk.Entry(reset_dialog, show="*")
        nova_senha_entry.grid(row=row, column=0, columnspan=2, pady=2); row+=1

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
                
        ttk.Button(reset_dialog, text="CONFIRMAR RESET", command=handle_reset).grid(row=row+1, column=0, columnspan=2, pady=10)

    # --- NOVO DIÁLOGO: HISTÓRICO DE USUÁRIO ---
    def open_historico_dialog(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário na lista para ver o histórico.")
            return

        current_values = self.tree.item(selected_item, 'values')
        usuario_id = current_values[0]
        nome_usuario = current_values[1]
        
        historico = processar_historico_usuario(usuario_id)

        dialog = tk.Toplevel(self.master)
        dialog.title(f"Histórico de Empréstimos: {nome_usuario} (ID: {usuario_id})")
        dialog.geometry("800x500") 
        dialog.transient(self.master)
        dialog.grab_set() 
        
        tk.Label(dialog, text=f"Livros emprestados por {nome_usuario}", 
                 font=("Arial", 14, "bold"), fg='#005a8d').pack(pady=10)

        hist_frame = tk.Frame(dialog)
        hist_frame.pack(fill='both', expand=True, padx=15, pady=5)
        hist_frame.grid_rowconfigure(0, weight=1)
        hist_frame.grid_columnconfigure(0, weight=1)

        hist_tree = ttk.Treeview(hist_frame, columns=('Titulo', 'Autor', 'Retirada', 'DevolucaoPrev', 'DevolucaoEfet'), show='headings')
        
        hist_tree.heading('Titulo', text='Título do Livro')
        hist_tree.heading('Autor', text='Autor')
        hist_tree.heading('Retirada', text='Retirada')
        hist_tree.heading('DevolucaoPrev', text='Dev. Prevista')
        hist_tree.heading('DevolucaoEfet', text='Dev. Efetiva')
        
        hist_tree.column('Titulo', width=200, anchor='w')
        hist_tree.column('Autor', width=150, anchor='w')
        hist_tree.column('Retirada', width=100, anchor='center')
        hist_tree.column('DevolucaoPrev', width=100, anchor='center')
        hist_tree.column('DevolucaoEfet', width=100, anchor='center')

        hist_tree.grid(row=0, column=0, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=hist_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        hist_tree.configure(yscrollcommand=scrollbar.set)

        # Preencher Histórico
        if historico:
            for item in historico:
                data_retirada = item['Data_Retirada'].strftime('%d/%m/%Y')
                data_prev = item['Data_Devolucao_Prev'].strftime('%d/%m/%Y')
                data_efet = item['Data_Devolucao_efet'].strftime('%d/%m/%Y') if item['Data_Devolucao_efet'] else 'EMPRÉSTIMO ATIVO'
                
                tag = ''
                if item['Data_Devolucao_efet'] is None:
                    tag = 'ativo'
                    hoje = datetime.now().date()
                    if hoje > item['Data_Devolucao_Prev']:
                        tag = 'atrasado'

                hist_tree.insert('', 'end', values=(
                    item['Titulo'], 
                    item['Autor'], 
                    data_retirada, 
                    data_prev, 
                    data_efet
                ), tags=(tag,))
                
            hist_tree.tag_configure('ativo', background='#fff3cd', foreground='#856404')
            hist_tree.tag_configure('atrasado', background='#f8d7da', foreground='#721c24', font=('Arial', 9, 'bold'))
        else:
             tk.Label(hist_frame, text="Este usuário não possui histórico de empréstimos.").grid(row=0, column=0)
             
        dialog.wait_window()