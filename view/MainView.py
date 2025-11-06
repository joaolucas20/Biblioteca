# Arquivo: view/MainView.py (ATUALIZADO)

import tkinter as tk
from tkinter import ttk
from view.emprestimo_view import EmprestimoView
from view.usuario_view import UsuarioView
from view.acervo_view import AcervoView
# NOVO: Importa a nova View de Editora
from view.editora_view import EditoraView

class MainView(tk.Toplevel):
    """
    Dashboard principal da aplicação. 
    Seu conteúdo muda baseado no 'perfil_usuario' (Adm, Biblioteca, Leitor).
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
        nav_frame = tk.Frame(self, width=200, bg='#f0f0f0', relief=tk.SUNKEN)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Frame de Conteúdo Principal
        self.content_frame = tk.Frame(self, bg='white', relief=tk.FLAT)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(nav_frame, text=f"Bem-vindo, {self.user_data['Nome'].split()[0]}!", 
                 font=("Arial", 10, "bold"), fg='#333').pack(pady=10, padx=10, fill=tk.X)
        
        self.create_nav_menu(nav_frame)
        
        # Botão de Logout
        tk.Button(nav_frame, text="LOGOUT", command=self.app_controller.logout, 
                  bg='red', fg='white', relief=tk.FLAT).pack(side=tk.BOTTOM, pady=20, padx=10, fill=tk.X)
                  
        self.load_home()

    def create_nav_menu(self, nav_frame):
        # Menu Comum a todos
        self._add_nav_button(nav_frame, "Início (Dashboard)", self.load_home)

        # Menu Específico por Perfil
        if self.profile in ['Adm', 'Biblioteca']:
            self._add_nav_button(nav_frame, "Empréstimos/Devoluções", lambda: self.load_module(EmprestimoView))
            self._add_nav_button(nav_frame, "Gerenciar Acervo (Livros)", lambda: self.load_module(AcervoView))
            # NOVO: Adiciona a EditoraView
            self._add_nav_button(nav_frame, "Gerenciar Editoras (CRUD)", lambda: self.load_module(EditoraView))
            
        if self.profile == 'Adm':
            self._add_nav_button(nav_frame, "Gerenciar Usuários (CRUD)", lambda: self.load_module(UsuarioView))
            
        if self.profile == 'Leitor':
            self._add_nav_button(nav_frame, "Meus Empréstimos", lambda: self.load_module("Meus Empréstimos"))
            self._add_nav_button(nav_frame, "Buscar Livros", lambda: self.load_module("Buscar Livros"))


    def _add_nav_button(self, parent, text, command):
        """Método auxiliar para criar botões de menu."""
        tk.Button(parent, text=text, command=command, anchor="w", width=25, padx=10, pady=5).pack(pady=2, padx=10)

    def clear_content_frame(self):
        """Limpa o conteúdo do frame principal para carregar um novo módulo."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_home(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text=f"Dashboard Principal", 
                 font=("Arial", 24, "bold")).pack(pady=50)
        tk.Label(self.content_frame, text=f"Use o menu lateral para gerenciar os módulos da biblioteca.", 
                 font=("Arial", 14)).pack(pady=20)
        
    def load_module(self, module_class_or_name):
        self.clear_content_frame()
        
        if isinstance(module_class_or_name, type):
            view_instance = module_class_or_name(self.content_frame, self, self.user_data) 
            view_instance.pack(fill=tk.BOTH, expand=True)
        
        elif isinstance(module_class_or_name, str):
            tk.Label(self.content_frame, text=f"Módulo '{module_class_or_name}' ainda não implementado.", 
                     font=("Arial", 24, "bold"), fg='orange').pack(pady=100)
            tk.Label(self.content_frame, text="Continue o desenvolvimento!", 
                     font=("Arial", 14)).pack(pady=20)