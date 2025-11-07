# Arquivo: view/meus_emprestimos_view.py
# --------------------------------------------------------------
# Módulo: Meus Empréstimos (perfil Leitor)
# Funcionalidades: lista empréstimos ativos com status colorido
# --------------------------------------------------------------
# view/meus_emprsestimos_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from controller.biblioteca_controller import processar_meus_emprestimos


class MeusEmprestimosView(tk.Frame):
    """Exibe os empréstimos ativos do usuário logado com status visual."""
    
    def __init__(self, master, controller, user_data):
        super().__init__(master)
        self.controller = controller
        self.user_data = user_data

        # Layout responsivo
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_treeview()
        self._load_emprestimos()

    # ------------------------------------------------------------------
    # Cabeçalho com título e botão
    # ------------------------------------------------------------------
    def _create_header(self):
        header = tk.Frame(self, bg="#f8f9fa")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header, text="MEUS EMPRÉSTIMOS", font=("Arial", 16, "bold"),
            bg="#f8f9fa", fg="#2c3e50"
        ).grid(row=0, column=0, sticky="w")

        btn_frame = tk.Frame(header, bg="#f8f9fa")
        btn_frame.grid(row=0, column=1, sticky="e")

        tk.Button(
            btn_frame, text="Atualizar", command=self._load_emprestimos,
            bg="#007acc", fg="white", relief=tk.FLAT, padx=10
        ).pack()

    # ------------------------------------------------------------------
    # Treeview com colunas e cores
    # ------------------------------------------------------------------
    def _create_treeview(self):
        columns = ("ID", "Título do Livro", "Retirada", "Previsão", "Faltam", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        # Configuração das colunas
        col_widths = [60, 300, 100, 100, 90, 100]
        col_anchors = ["center", "w", "center", "center", "center", "center"]
        for col, width, anchor in zip(columns, col_widths, col_anchors):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 10))

        # Cores por status
        self.tree.tag_configure("atrasado", background="#ffebee", foreground="#c62828")
        self.tree.tag_configure("urgente", background="#fff3e0", foreground="#ef6c00")
        self.tree.tag_configure("em_dia", background="#e8f5e9", foreground="#2e7d32")

    # ------------------------------------------------------------------
    # Carregar e exibir dados
    # ------------------------------------------------------------------
    def _load_emprestimos(self):
        # Limpar
        for item in self.tree.get_children():
            self.tree.delete(item)

        emprestimos = processar_meus_emprestimos(self.user_data["Id_Usuario"]) or []

        if not emprestimos:
            messagebox.showinfo("Sem Empréstimos", "Você não tem empréstimos ativos no momento.")
            return

        hoje = date.today()

        for emp in emprestimos:
            try:
                # Campos flexíveis
                emp_id = emp.get("Id_Emprestimo") or emp.get("id_emprestimo")
                titulo = emp.get("Livro_Titulo") or emp.get("titulo", "Título não informado")
                retirada_str = emp["Data_Retirada"]
                previsao_str = emp["Data_Devolucao_Prev"]

                # Converter datas
                retirada = datetime.strptime(retirada_str, "%Y-%m-%d").date()
                previsao = datetime.strptime(previsao_str, "%Y-%m-%d").date()
                dias_faltam = (previsao - hoje).days

                # Status
                if dias_faltam < 0:
                    status = "Atrasado"
                    tag = "atrasado"
                elif dias_faltam <= 3:
                    status = f"{dias_faltam} dia(s)"
                    tag = "urgente"
                else:
                    status = f"{dias_faltam} dia(s)"
                    tag = "em_dia"

                # Inserir
                self.tree.insert("", "end", values=(
                    emp_id,
                    titulo,
                    retirada.strftime("%d/%m/%Y"),
                    previsao.strftime("%d/%m/%Y"),
                    f"{dias_faltam} dia(s)" if dias_faltam >= 0 else "Atrasado!",
                    status
                ), tags=(tag,))

            except Exception as e:
                print(f"[ERRO] Empréstimo inválido: {e}")
                continue