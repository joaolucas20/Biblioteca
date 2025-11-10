# Arquivo: app.py (Controlador Principal)

import tkinter as tk
from view.login_view import LoginView
from view.MainView import MainView 
from controller.biblioteca_controller import processar_login, processar_cadastro
from controller.biblioteca_controller import processar_check_admin_exists
from controller.biblioteca_controller import processar_check_admin_exists
class AppController(tk.Tk):
    """
    Controlador principal da aplicação. Gerencia o root do Tkinter, 
    o estado do usuário logado e a navegação entre as telas.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema da Biblioteca - MVC")
        self.withdraw() 
        self.geometry("800x600")
        
        self.current_user = None

        self.login_window = LoginView(self)
        
    def handle_login_success(self, user_data):
        """
        Chamado pelo LoginView após o sucesso. Abre o Dashboard.
        """
        self.current_user = user_data
        
        self.login_window.destroy()
        self.open_main_dashboard()

    def open_main_dashboard(self):
        """
        Instancia e exibe a MainView (Dashboard).
        """
        MainView(self, self, self.current_user)

    def logout(self):
        """
        Finaliza a sessão do usuário e retorna para a tela de login.
        """
        self.current_user = None
        
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        
        self.login_window = LoginView(self)
        
if __name__ == "__main__":
    from model.usuario_model import cadastrar_usuario
    
    # --- Configuração do Usuário Inicial (Para Teste) ---
    try:
        # 1. VERIFICA SE O ADMIN JÁ EXISTE ANTES DE CADASTRAR
        if not processar_check_admin_exists(): # Esta função verifica no BD
            # Tenta cadastrar um Admin (perfil 'Adm')
            cadastrar_usuario("Admin Geral", "Adm", "999999999", "admin@biblioteca.com", "senha123", "Sede Administrativa Principal")
            print("Usuário Admin 'admin@biblioteca.com' (senha123) cadastrado com sucesso.")
        else:
            print("Usuário Admin já existe. Criação automática ignorada.")

    except Exception as e:
        print(f"Erro ao tentar configurar o usuário Admin: {e}")
        
    app = AppController()
    app.mainloop()