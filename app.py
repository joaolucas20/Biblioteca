# Arquivo: app.py

from view.login_view import LoginView

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()