import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Scrollbar, RIGHT, Y, END
from controller import Controller
"""
A fazer
Criar conta
Fazer login

Pronto
Mostrar processos
Mostrar dados dos processos
Atualizar processos por RAM e por nome
Atualizar automaticamente
"""
class LoginScreen:
    def __init__(self, root):

        self.controller = Controller()
        self.root = root
        self.root.title("Tela de Login")
        self.root.geometry("300x200")

        self.label_username = tk.Label(root, text="Usuário:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(root, text="Senha:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)

        self.btn_login = tk.Button(root, text="Login", command=self.check_login)
        self.btn_login.pack(pady=10)
        self.btn_register = tk.Button(root, text="Criar conta", command=lambda: open_register(self.root))
        self.btn_register.pack(pady=10)
    def check_login(self):
        user = self.entry_username.get()
        password = self.entry_password.get()

        resultado = self.controller.auth(user, password)
        if resultado:
            messagebox.showinfo("Login bem-sucedido", "Bem-vindo ao Gerenciador de Tarefas!")
            self.root.destroy()
            open_task_manager()

        else:
            messagebox.showerror("Erro de login", "Usuário já existe.")
class RegisterScreen:
    def __init__(self, root):

        self.controller = Controller()
        self.root = root
        self.root.title("Tela de Registro")
        self.root.geometry("300x300")

        self.label_username = tk.Label(root, text="Usuário:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(root, text="Senha:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)
        self.label_password = tk.Label(root, text="Repita a senha:")
        self.label_password.pack(pady=5)
        self.entry_password2 = tk.Entry(root, show="*")
        self.entry_password2.pack(pady=5)
        self.btn_register = tk.Button(root, text="Register", command=self.check_register)
        self.btn_register.pack(pady=10)
        self.btn_login = tk.Button(root, text="Login", command=lambda: open_login(self.root))
        self.btn_login.pack(pady=10)
    def check_register(self):
        user = self.entry_username.get()
        password = self.entry_password.get()
        password2 = self.entry_password2.get()
        if password==password2:
            resultado = self.controller.setUser(user, password)
            if resultado:
                messagebox.showinfo("Login bem-sucedido", "Bem-vindo ao Gerenciador de Tarefas!")
                open_login(self.root)

            else:
                messagebox.showerror("Erro de Registro", "Usuário já existe.")
        else:
            messagebox.showerror("Erro de Registro", "Senhas diferentes")
            self.entry_password.delete(0, END)
            self.entry_password2.delete(0, END)

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("600x600")
        self.tipo = 0

        self.tree = ttk.Treeview(root, columns=("PID", "Nome", "Prioridade", "Uso CPU", "Estado", "Memória"), show="headings")
        scrollbar = Scrollbar(self.tree)
        scrollbar.pack( side = RIGHT, fill=Y )
        scrollbar.config( command = self.tree.yview )
        self.tree.heading("PID", text="PID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.heading("Uso CPU", text="Uso CPU (%)")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Memória", text="Memória (MB)")

        self.tree.column("PID", width=50)
        self.tree.column("Nome", width=50)
        self.tree.column("Prioridade", width=50)
        self.tree.column("Uso CPU", width=50)
        self.tree.column("Estado", width=50)
        self.tree.column("Memória", width=50)

        self.tree.pack(expand=True, fill='both')

        self.btn_refresh_name = tk.Button(root, text="Atualizar por nome", command=lambda: self.refresh_processes(0))
        self.btn_refresh_name.pack()
        self.btn_refresh_memo = tk.Button(root, text="Atualizar por memória", command=lambda: self.refresh_processes(1))
        self.btn_refresh_memo.pack()
        self.refresh_processes(0)
        self.btn_terminate = tk.Button(root, text="Finalizar Processo", command=self.terminate_process)
        self.btn_terminate.pack()
        self.auto_refresh()

    def auto_refresh(self):
        self.refresh_processes(self.tipo)
        self.root.after(2000, self.auto_refresh)

    def terminate_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um processo.")
            return
        
        pid = self.tree.item(selected_item)["values"][0]
        try:
            process = psutil.Process(pid)
            process.terminate()
            messagebox.showinfo("Sucesso", f"Processo {pid} finalizado.")
            self.refresh_processes(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            messagebox.showerror("Erro", f"Não foi possível finalizar o processo: {e}")

    def refresh_processes(self, tipo):

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'nice', 'cpu_percent', 'status', 'memory_info']):
            try:
                nice_value = proc.info['nice']

                if nice_value == 64:
                    nice_classification = "Alta"
                elif nice_value == 32:
                    nice_classification = "Média"
                else:
                    nice_classification = "Baixa"
                processes.append((
                    proc.info['pid'],
                    proc.info['name'],
                    nice_classification,
                    proc.info['cpu_percent'],
                    proc.info['status'],
                    round(proc.info['memory_info'].rss / (1024 * 1024), 1)
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if tipo == 0:
            self.tipo = 0
            processes.sort(key=lambda x: x[1].lower())
            print("Atualizou por nome")
        elif tipo == 1:
            self.tipo = 1
            processes.sort(key=lambda x: x[5], reverse=True)
            print("Atualizou por RAM")

        for process in processes:
            self.tree.insert("", "end", values=process)

def open_login(tela):
    tela.destroy()
    root = tk.Tk()
    loginS = LoginScreen(root)
    root.mainloop()

def open_task_manager():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
def open_register(tela):
    tela.destroy()
    root = tk.Tk()
    reg = RegisterScreen(root)
    root.mainloop

if __name__ == "__main__":
    root = tk.Tk()
    login = RegisterScreen(root)
    root.mainloop()
