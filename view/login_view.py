# Arquivo: view/login_view.py

import tkinter as tk
from tkinter import messagebox
from controller.biblioteca_controller import processar_login, processar_cadastro

class LoginView(tk.Toplevel): 
    def __init__(self, master):
        super().__init__(master)
        self.master = master 
        self.title("Sistema da Biblioteca - Login")
        self.geometry("400x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.master.quit) 
        
        # --- FRAME PRINCIPAL ---
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # --- TÍTULO ---
        tk.Label(self.main_frame, text="Login de Acesso", font=("Arial", 16)).pack(pady=10)
        
        # --- CAMPOS DE ENTRADA ---
        tk.Label(self.main_frame, text="Email:").pack(anchor='w')
        self.email_entry = tk.Entry(self.main_frame, width=30)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Senha:").pack(anchor='w')
        self.senha_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.senha_entry.pack(pady=5)
        
        # --- BOTÕES ---
        tk.Button(self.main_frame, text="ENTRAR", command=self.handle_login, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Cadastre-se", command=self.open_cadastro, width=20).pack(pady=5)

    def handle_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        
        usuario = processar_login(email, senha)
        
        if usuario:
            messagebox.showinfo("Sucesso", f"Login de {usuario['Tipo']} bem-sucedido! Bem-vindo(a), {usuario['Nome']}.")
            self.master.handle_login_success(usuario) 
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")
            self.senha_entry.delete(0, tk.END) 

    def open_cadastro(self):
        CadastroView(self.master)
        
        
class CadastroView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master 
        self.title("Novo Cadastro")
        self.geometry("350x350")
        self.resizable(False, False)
        
        tk.Label(self, text="CADASTRO DE LEITOR", font=("Arial", 14)).pack(pady=10)
        
        self.nome_entry = self._create_field("Nome:")
        self.email_entry = self._create_field("Email:")
        self.tel_entry = self._create_field("Telefone:")
        self.senha_entry = self._create_field("Senha:", show="*")
        
        tk.Button(self, text="FINALIZAR CADASTRO", command=self.handle_cadastro, width=25).pack(pady=20)
        
    def _create_field(self, label_text, **kwargs):
        tk.Label(self, text=label_text).pack(anchor='w', padx=20)
        entry = tk.Entry(self, width=40, **kwargs)
        entry.pack(pady=2, padx=20)
        return entry

    def handle_cadastro(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        tel = self.tel_entry.get()
        senha = self.senha_entry.get()
        
        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        sucesso = processar_cadastro(nome, 'Leitor', tel, email, senha)
        
        if sucesso:
            messagebox.showinfo("Sucesso", "Cadastro realizado! Você já pode fazer login.")
            self.destroy() 
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar. Verifique se o e-mail já está em uso.")