# Arquivo: view/usuario_view.py
# --------------------------------------------------------------
# CRUD completo de Usuários (Administrador)
# --------------------------------------------------------------

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
    """Módulo de gerenciamento de usuários – apenas para Adm."""
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Cabeçalho + botões
        self._create_header_and_actions()

        # 2. Frame da Treeview
        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # 3. Treeview
        self._create_treeview()

        # 4. Carrega dados
        self.load_data()

    # ------------------------------------------------------------------
    # 1. Cabeçalho + botões
    # ------------------------------------------------------------------
    def _create_header_and_actions(self):
        header = tk.Frame(self)
        header.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        tk.Label(header, text="GERENCIAMENTO DE USUÁRIOS",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        btns = tk.Frame(header)
        btns.pack(side=tk.RIGHT)

        tk.Button(btns, text="Adicionar Novo", command=self.open_add_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Editar Selecionado", command=self.open_edit_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Excluir Selecionado", command=self.handle_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Resetar Senha", command=self.handle_reset_password).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Atualizar Lista", command=self.load_data).pack(side=tk.LEFT, padx=5)

    # ------------------------------------------------------------------
    # 2. Treeview
    # ------------------------------------------------------------------
    def _create_treeview(self):
        columns = ("ID", "Nome", "Tipo", "Telefone", "Email", "Endereço")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='w')
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

    # ------------------------------------------------------------------
    # 3. Carregar dados
    # ------------------------------------------------------------------
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        usuarios = processar_lista_usuarios() or []
        for u in usuarios:
            self.tree.insert("", "end", values=(
                u["Id_Usuario"], u["Nome"], u["Tipo"],
                u["Telefone"], u["Email"], u["Endereco"]
            ))

    # ------------------------------------------------------------------
    # 4. Diálogos (Add / Edit)
    # ------------------------------------------------------------------
    def _dialog_crud(self, title, is_edit=False, user=None):
        dlg = tk.Toplevel(self.master)
        dlg.title(title)
        dlg.geometry("400x400")
        dlg.transient(self.master)
        dlg.grab_set()

        entries = {}
        campos = ["Nome", "Tipo", "Telefone", "Email", "Endereço"]
        for i, campo in enumerate(campos):
            tk.Label(dlg, text=f"{campo}:").grid(row=i, column=0, sticky='w', padx=10, pady=5)
            ent = tk.Entry(dlg, width=40)
            ent.grid(row=i, column=1, padx=10, pady=5)
            entries[campo] = ent
            if is_edit and user:
                ent.insert(0, user.get(campo, ""))

        def salvar():
            dados = {k: v.get().strip() for k, v in entries.items()}
            if not all(dados.values()):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return
            if is_edit:
                sucesso = processar_edicao_usuario(user["Id_Usuario"], **dados)
            else:
                sucesso = processar_adicao_usuario(**dados)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário {'atualizado' if is_edit else 'cadastrado'}!")
                self.load_data()
                dlg.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao salvar. Verifique os dados.")

        btn_txt = "SALVAR ALTERAÇÕES" if is_edit else "CADASTRAR"
        tk.Button(dlg, text=btn_txt, command=salvar, width=30).grid(row=len(campos), column=0,
                                                                    columnspan=2, pady=15)
        dlg.wait_window()

    def open_add_dialog(self):
        self._dialog_crud("Adicionar Usuário")

    def open_edit_dialog(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um usuário para editar.")
            return
        values = self.tree.item(sel, "values")
        user = {
            "Id_Usuario": values[0], "Nome": values[1], "Tipo": values[2],
            "Telefone": values[3], "Email": values[4], "Endereço": values[5]
        }
        self._dialog_crud("Editar Usuário", is_edit=True, user=user)

    # ------------------------------------------------------------------
    # 5. Excluir
    # ------------------------------------------------------------------
    def handle_delete(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")
            return
        uid = self.tree.item(sel, "values")[0]
        nome = self.tree.item(sel, "values")[1]
        if not messagebox.askyesno("Confirmação",
                                   f"Excluir usuário '{nome}' (ID {uid})?\n"
                                   "Esta ação é irreversível!"):
            return
        if processar_exclusao_usuario(uid):
            messagebox.showinfo("Sucesso", f"Usuário {nome} excluído.")
            self.load_data()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir (empréstimos ativos?).")

    # ------------------------------------------------------------------
    # 6. Reset de senha
    # ------------------------------------------------------------------
    def handle_reset_password(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um usuário.")
            return
        uid = self.tree.item(sel, "values")[0]
        nova = tk.simpledialog.askstring("Reset de Senha", "Nova senha:", show='*')
        if nova and nova.strip():
            if processar_reset_senha(uid, nova.strip()):
                messagebox.showinfo("Sucesso", "Senha redefinida.")
            else:
                messagebox.showerror("Erro", "Falha ao redefinir senha.")
        else:
            messagebox.showwarning("Atenção", "Senha não pode ser vazia.")