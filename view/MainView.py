# Arquivo: view/MainView.py

import tkinter as tk
from tkinter import ttk

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
        
        # Configuração para que esta janela seja modal ou a única ativa
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
        
        tk.Label(nav_frame, text=f"Bem-vindo(a),\n{self.user_data['Nome']}!", 
                 font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=10, padx=5)
        tk.Label(nav_frame, text=f"Perfil: {self.profile}", 
                 font=("Arial", 10), bg='#f0f0f0').pack(pady=5, padx=5)

        # Botões de navegação
        self._add_nav_button(nav_frame, "Início", self.load_home)

        # Módulos Administrativos/Bibliotecário
        if self.profile in ['Adm', 'Biblioteca']:
            self._add_nav_button(nav_frame, "Gerenciar Livros (CRUD)", lambda: self.load_module("Livros"))
            self._add_nav_button(nav_frame, "Gerenciar Usuários (CRUD)", lambda: self.load_module("Usuários"))

        # Módulos Gerais
        self._add_nav_button(nav_frame, "Empréstimos/Devoluções", lambda: self.load_module("Empréstimos"))
        self._add_nav_button(nav_frame, "Minhas Reservas", lambda: self.load_module("Reservas"))

        # Módulos Admin (Alto Nível)
        if self.profile == 'Adm':
            self._add_nav_button(nav_frame, "Relatórios & Estatísticas", lambda: self.load_module("Relatórios"))

        # Botão de Logout
        tk.Button(nav_frame, text="Sair / Logout", command=self.handle_logout, 
                  bg='red', fg='white').pack(side=tk.BOTTOM, pady=20, padx=10, fill=tk.X)
                  
        self.load_home()

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
        
    def load_module(self, module_name):
        self.clear_content_frame()
        # Aqui, você chamará o controlador específico para o módulo
        tk.Label(self.content_frame, text=f"Carregando Módulo: {module_name}", 
                 font=("Arial", 24, "bold"), fg='blue').pack(pady=100)
        tk.Label(self.content_frame, text=f"Implementar {module_name}Controller.show_view() aqui.", 
                 font=("Arial", 12)).pack()
                 
    def handle_logout(self):
        self.destroy() # Fecha esta janela Toplevel
        self.app_controller.logout() # Chama o método de logout do AppController