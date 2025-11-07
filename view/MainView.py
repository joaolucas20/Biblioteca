# Arquivo: view/MainView.py (ATUALIZADO – SEM LAMBDA)

import tkinter as tk
from tkinter import ttk
from view.emprestimo_view import EmprestimoView
from view.usuario_view import UsuarioView
from view.acervo_view import AcervoView
from view.editora_view import EditoraView
from view.meus_emprestimos_view import MeusEmprestimosView
from view.buscar_livros_view import BuscarLivrosView


class MainView(tk.Toplevel):
    """
    Dashboard principal da aplicação.
    Navegação via menu lateral SEM uso de lambda.
    """
    def __init__(self, master, app_controller, user_data):
        super().__init__(master)
        self.master = master
        self.app_controller = app_controller
        self.user_data = user_data
        self.profile = user_data['Tipo']

        self.title(f"Biblioteca - Dashboard: {self.profile}")
        self.geometry("1000x700")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.app_controller.quit)

        self.create_widgets()

    def create_widgets(self):
        # Frame de Navegação (Menu Lateral)
        nav_frame = tk.Frame(self, width=220, bg='#2c3e50', relief=tk.SUNKEN)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        nav_frame.pack_propagate(False)

        # Frame de Conteúdo Principal
        self.content_frame = tk.Frame(self, bg='white')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Título de boas-vindas
        tk.Label(
            nav_frame, text=f"Bem-vindo,\n{self.user_data['Nome'].split()[0]}!",
            font=("Arial", 11, "bold"), fg='white', bg='#2c3e50', anchor='w'
        ).pack(pady=20, padx=15, fill=tk.X)

        self.create_nav_menu(nav_frame)

        # Botão de Logout
        tk.Button(
            nav_frame, text="LOGOUT", command=self.app_controller.logout,
            bg='#e74c3c', fg='white', relief=tk.FLAT, font=("Arial", 10, "bold")
        ).pack(side=tk.BOTTOM, pady=20, padx=15, fill=tk.X)

        self.load_home()

    def create_nav_menu(self, nav_frame):
        """Cria botões de navegação SEM lambda."""
        # --- MÓDULOS COMUNS ---
        self._add_nav_button(nav_frame, "Dashboard", self.load_home)
        self._add_nav_button(nav_frame, "Gerenciar Acervo", self.load_acervo)
        self._add_nav_button(nav_frame, "Gerenciar Editoras", self.load_editoras)

        # --- PERFIL: Administrador ---
        if self.profile == 'Adm':
            self._add_nav_button(nav_frame, "Gerenciar Usuários", self.load_usuarios)
            self._add_nav_button(nav_frame, "Gerenciar Empréstimos", self.load_emprestimos)

        # --- PERFIL: Biblioteca ---
        elif self.profile == 'Biblioteca':
            self._add_nav_button(nav_frame, "Gerenciar Empréstimos", self.load_emprestimos)
            self._add_nav_button(nav_frame, "Gerenciar Acervo", self.load_acervo)

        # --- PERFIL: Leitor ---
        elif self.profile == 'Leitor':
            self._add_nav_button(nav_frame, "Meus Empréstimos", self.load_meus_emprestimos)
            self._add_nav_button(nav_frame, "Buscar Livros", self.load_buscar_livros)

    def _add_nav_button(self, parent, text, command):
        """Método auxiliar para criar botões com estilo uniforme."""
        btn = tk.Button(
            parent, text=text, command=command,
            anchor="w", justify="left", padx=15, pady=8,
            bg='#34495e', fg='white', relief=tk.FLAT,
            font=("Arial", 10), cursor="hand2"
        )
        btn.pack(fill=tk.X, padx=10, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg='#1abc9c'))
        btn.bind("<Leave>", lambda e: btn.config(bg='#34495e'))

    # ------------------------------------------------------------------
    # Métodos de carregamento de módulos (SEM lambda)
    # ------------------------------------------------------------------
    def load_home(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Dashboard Principal", font=("Arial", 28, "bold"), fg="#2c3e50").pack(pady=60)
        tk.Label(self.content_frame, text="Use o menu lateral para acessar os módulos.", font=("Arial", 14)).pack(pady=20)

    def load_acervo(self):
        self.clear_content_frame()
        AcervoView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    def load_editoras(self):
        self.clear_content_frame()
        EditoraView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    def load_usuarios(sself):
        self.clear_content_frame()
        UsuarioView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    def load_emprestimos(self):
        self.clear_content_frame()
        EmprestimoView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    def load_meus_emprestimos(self):
        self.clear_content_frame()
        MeusEmprestimosView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    def load_buscar_livros(self):
        self.clear_content_frame()
        BuscarLivrosView(self.content_frame, self, self.user_data).pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    def clear_content_frame(self):
        """Remove todos os widgets do frame principal."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()