# Arquivo: view/MainView.py (VERSÃO FINAL E ESTILIZADA)

import tkinter as tk
from tkinter import ttk
# Importações dos módulos (Certifique-se de que estes arquivos existem e estão atualizados)
from view.emprestimo_view import EmprestimoView
from view.usuario_view import UsuarioView
from view.acervo_view import AcervoView
from view.editora_view import EditoraView
from view.meus_emprestimos_view import MeusEmprestimosView 
from view.buscar_livros_view import BuscarLivrosView      

class MainView(tk.Toplevel):
    """
    Dashboard principal da aplicação com layout robusto (Grid e Pack) e tela inicial estilizada.
    """
    def __init__(self, master, app_controller, user_data):
        super().__init__(master)
        self.app_controller = app_controller
        self.user_data = user_data
        self.profile = user_data['Tipo']
        self.title(f"Sistema de Biblioteca - Dashboard: {self.profile}")
        self.geometry("1100x750") 
        
        self.grab_set() 
        self.protocol("WM_DELETE_WINDOW", self.app_controller.quit)
        
        # Configurar estilo TTK (para separador e tema base)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Configuração do Grid principal (Garante que tudo se expanda)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Menu lateral (fixo)
        self.grid_columnconfigure(1, weight=1) # Conteúdo principal (expansível)

        # 2. Frame de Navegação (Menu Lateral - tk.Frame básico para estabilidade)
        nav_frame = tk.Frame(self, width=220, bg='#f0f0f0', relief=tk.SUNKEN)
        nav_frame.grid(row=0, column=0, sticky='nswe', padx=0, pady=0)
        
        # 3. Frame de Conteúdo Principal
        self.content_frame = tk.Frame(self, bg='white', relief=tk.FLAT)
        self.content_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        # Saudação Simples e Estável
        tk.Label(nav_frame, text=f"Bem-vindo(a), {self.user_data['Nome'].split()[0]}!", 
                 font=("Arial", 11, "bold"), fg='#005a8d', bg='#f0f0f0').pack(pady=15, padx=10, fill=tk.X)
        
        # Separador visual
        ttk.Separator(nav_frame, orient='horizontal').pack(fill='x', pady=5, padx=10)
        
        self.create_nav_menu(nav_frame)
        
        # Botão de Logout (no fundo)
        tk.Button(nav_frame, text="LOGOUT 🚪", command=self.app_controller.logout, 
                  bg='red', fg='white', relief=tk.FLAT, font=("Arial", 10, "bold")).pack(side=tk.BOTTOM, pady=20, padx=15, fill=tk.X)
                  
        self.load_home()

    def create_nav_menu(self, nav_frame):
        # Menu Comum a todos
        self._add_nav_button(nav_frame, "🏠 Início (Dashboard)", self.load_home)
        
        # Separador
        ttk.Separator(nav_frame, orient='horizontal').pack(fill='x', pady=10, padx=10)

        # Menu Específico por Perfil
        if self.profile in ['Adm', 'Biblioteca']:
            self._add_nav_button(nav_frame, "🔄 Empréstimos/Devoluções", lambda: self.load_module(EmprestimoView))
            self._add_nav_button(nav_frame, "📚 Gerenciar Acervo (Livros)", lambda: self.load_module(AcervoView))
            self._add_nav_button(nav_frame, "🏢 Gerenciar Editoras (CRUD)", lambda: self.load_module(EditoraView))
            
        if self.profile == 'Adm':
            self._add_nav_button(nav_frame, "👥 Gerenciar Usuários (CRUD)", lambda: self.load_module(UsuarioView))
            
        if self.profile == 'Leitor':
            self._add_nav_button(nav_frame, "🔎 Buscar Livros", lambda: self.load_module(BuscarLivrosView))
            self._add_nav_button(nav_frame, "📥 Meus Empréstimos", lambda: self.load_module(MeusEmprestimosView))


    def _add_nav_button(self, parent, text, command):
        """Método auxiliar usando tk.Button básico para máxima compatibilidade e garantindo que apareçam."""
        tk.Button(parent, text=text, command=command, anchor="w", width=25, 
                   padx=10, pady=5, relief=tk.FLAT, bg='#e0e0e0', fg='#333').pack(pady=2, padx=10, fill=tk.X)

    def clear_content_frame(self):
        """Limpa o conteúdo do frame principal para carregar um novo módulo."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_home(self):
        """Carrega a tela inicial estilizada com informações do usuário."""
        self.clear_content_frame()
        
        home_container = tk.Frame(self.content_frame, bg='white')
        home_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        home_container.grid_rowconfigure(2, weight=1)
        home_container.grid_columnconfigure(0, weight=1)

        # 1. Título e Subtítulo
        tk.Label(home_container, text=f"📚 Bem-vindo(a) ao Sistema de Biblioteca", 
                 font=("Arial", 28, "bold"), fg='#005a8d', bg='white').grid(row=0, column=0, pady=(20, 5), sticky='w')
                 
        tk.Label(home_container, text=f"Seu ambiente de gestão e pesquisa do acervo.", 
                 font=("Arial", 14), fg='#666', bg='white').grid(row=1, column=0, pady=(0, 30), sticky='w')
        
        # 2. Informações do Perfil (Cartão de Destaque)
        info_frame = tk.Frame(home_container, bg='#f0f8ff', bd=1, relief=tk.SOLID)
        info_frame.grid(row=2, column=0, sticky='new', padx=10, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(info_frame, text=f"Sessão Ativa:", font=("Arial", 14, "bold"), fg='#005a8d', bg='#f0f8ff').grid(row=0, column=0, columnspan=2, sticky='w', padx=15, pady=(15, 5))
        
        # Detalhes
        tk.Label(info_frame, text="Nome:", font=("Arial", 11, "bold"), bg='#f0f8ff').grid(row=1, column=0, sticky='w', padx=15, pady=2)
        tk.Label(info_frame, text=self.user_data['Nome'], font=("Arial", 11), bg='#f0f8ff').grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(info_frame, text="Perfil:", font=("Arial", 11, "bold"), bg='#f0f8ff').grid(row=2, column=0, sticky='w', padx=15, pady=2)
        tk.Label(info_frame, text=self.user_data['Tipo'], font=("Arial", 11, "bold"), fg='darkgreen' if self.profile=='Adm' else 'blue', bg='#f0f8ff').grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(info_frame, text="ID:", font=("Arial", 11, "bold"), bg='#f0f8ff').grid(row=3, column=0, sticky='w', padx=15, pady=2)
        tk.Label(info_frame, text=self.user_data['Id_Usuario'], font=("Arial", 11), bg='#f0f8ff').grid(row=3, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(info_frame, text="📧 Email:", font=("Arial", 11, "bold"), bg='#f0f8ff').grid(row=4, column=0, sticky='w', padx=15, pady=2)
        tk.Label(info_frame, text=self.user_data['Email'], font=("Arial", 11), bg='#f0f8ff').grid(row=4, column=1, sticky='w', padx=5, pady=2)
        
        tk.Label(home_container, text="Use o menu lateral esquerdo para navegar e gerenciar os módulos de acordo com seu perfil.", 
                 font=("Arial", 12, "italic"), fg='#333', bg='white').grid(row=3, column=0, columnspan=2, pady=30)
        
    def load_module(self, module_class_or_name):
        self.clear_content_frame()
        
        if isinstance(module_class_or_name, type):
            # Passa o content_frame como master para que o módulo seja empacotado dentro dele
            # Usa o app_controller, não o self, como o segundo argumento para a View
            view_instance = module_class_or_name(self.content_frame, self.app_controller, self.user_data) 
            view_instance.pack(fill=tk.BOTH, expand=True)
        
        elif isinstance(module_class_or_name, str):
            tk.Label(self.content_frame, text=f"Módulo '{module_class_or_name}' ainda não implementado.", 
                     font=("Arial", 24, "bold"), fg='orange', bg='white').pack(pady=100)
            tk.Label(self.content_frame, text="Continue o desenvolvimento!", 
                     font=("Arial", 14), bg='white').pack(pady=20)