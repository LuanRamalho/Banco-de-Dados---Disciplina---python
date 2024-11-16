import tkinter as tk
from tkinter import messagebox, ttk
import db

class SistemaNotas:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Notas")
        master.geometry("800x600")
        master.configure(bg="#f0f2f5")

        self.selected_item = None
        self.create_widgets()
        self.load_disciplinas()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="Cadastro de Disciplinas", font=("Segoe UI", 24), bg="#f0f2f5", fg="#007bff")
        title_label.pack(pady=20)

        self.search_entry = tk.Entry(self.master, width=30)
        self.search_entry.insert(0, "Buscar por disciplina")
        self.search_entry.pack(pady=5)

        search_button = tk.Button(self.master, text="Buscar", command=self.search_disciplina, bg="#007bff", fg="white")
        search_button.pack(pady=5)

        self.disciplina_entry = tk.Entry(self.master, width=30)
        self.disciplina_entry.insert(0, "Nome da Disciplina")
        self.disciplina_entry.pack(pady=5)

        self.av1_entry = tk.Entry(self.master, width=30)
        self.av1_entry.insert(0, "Nota AV1")
        self.av1_entry.pack(pady=5)

        self.av2_entry = tk.Entry(self.master, width=30)
        self.av2_entry.insert(0, "Nota AV2")
        self.av2_entry.pack(pady=5)

        self.av3_entry = tk.Entry(self.master, width=30)
        self.av3_entry.insert(0, "Nota AV3")
        self.av3_entry.pack(pady=5)

        self.av4_entry = tk.Entry(self.master, width=30)
        self.av4_entry.insert(0, "Nota AV4")
        self.av4_entry.pack(pady=5)

        submit_button = tk.Button(self.master, text="Cadastrar", command=self.cadastrar_disciplina, bg="#007bff", fg="white")
        submit_button.pack(pady=10)

        edit_button = tk.Button(self.master, text="Editar", command=self.prepare_edit, bg="#ffc107", fg="black")
        edit_button.pack(pady=10)

        delete_button = tk.Button(self.master, text="Excluir", command=self.delete_disciplina, bg="#dc3545", fg="white")
        delete_button.pack(pady=10)

        self.result_table = ttk.Treeview(self.master, columns=("Disciplina", "AV1", "AV2", "AV3", "AV4", "Média", "Situação"), show='headings')
        self.result_table.heading("Disciplina", text="Disciplina")
        self.result_table.heading("AV1", text="AV1")
        self.result_table.heading("AV2", text="AV2")
        self.result_table.heading("AV3", text="AV3")
        self.result_table.heading("AV4", text="AV4")
        self.result_table.heading("Média", text="Média")
        self.result_table.heading("Situação", text="Situação")
        self.result_table.pack(pady=10, fill=tk.BOTH, expand=True)

        self.result_table.bind("<Double-1>", self.select_disciplina)

    def load_disciplinas(self):
        for row in db.get_all_disciplinas():
            self.result_table.insert("", tk.END, values=row)

    def search_disciplina(self):
        search_term = self.search_entry.get()
        for row in self.result_table.get_children():
            self.result_table.delete(row)
        for row in db.search_disciplinas(search_term):
            self.result_table.insert("", tk.END, values=row)

    def cadastrar_disciplina(self):
        disciplina = self.disciplina_entry.get()
        av1 = float(self.av1_entry.get())
        av2 = float(self.av2_entry.get())
        av3 = float(self.av3_entry.get())
        av4 = float(self.av4_entry.get())
        media = (av1 + av2 + av3 + av4) / 4
        situacao = "APROVADO" if media >= 7 else "REPROVADO"

        db.insert_disciplina(disciplina, av1, av2, av3, av4, media, situacao)

        self.clear_entries()
        self.refresh_table()

        messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")

    def select_disciplina(self, event):
        selected_item = self.result_table.selection()[0]
        self.selected_item = selected_item
        item_values = self.result_table.item(selected_item, "values")
        
        self.disciplina_entry.delete(0, tk.END)
        self.disciplina_entry.insert(0, item_values[0])
        self.av1_entry.delete(0, tk.END)
        self.av1_entry.insert(0, item_values[1])
        self.av2_entry.delete(0, tk.END)
        self.av2_entry.insert(0, item_values[2])
        self.av3_entry.delete(0, tk.END)
        self.av3_entry.insert(0, item_values[3])
        self.av4_entry.delete(0, tk.END)
        self.av4_entry.insert(0, item_values[4])

    def prepare_edit(self):
        if self.selected_item:
            disciplina = self.disciplina_entry.get()
            av1 = float(self.av1_entry.get())
            av2 = float(self.av2_entry.get())
            av3 = float(self.av3_entry.get())
            av4 = float(self.av4_entry.get())
            media = (av1 + av2 + av3 + av4) / 4
            situacao = "APROVADO" if media >= 7 else "REPROVADO"

            db.update_disciplina(self.result_table.item(self.selected_item)["values"][0], disciplina, av1, av2, av3, av4, media, situacao)

            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            self.refresh_table()
            self.clear_entries()
            self.selected_item = None
        else:
            messagebox.showwarning("Seleção Inválida", "Selecione uma disciplina para editar.")

    def delete_disciplina(self):
        if self.selected_item:
            disciplina_nome = self.result_table.item(self.selected_item)["values"][0]
            if messagebox.askyesno("Confirmação", f"Deseja excluir a disciplina '{disciplina_nome}'?"):
                db.delete_disciplina(disciplina_nome)
                messagebox.showinfo("Sucesso", "Disciplina excluída com sucesso!")
                self.refresh_table()
                self.clear_entries()
                self.selected_item = None
        else:
            messagebox.showwarning("Seleção Inválida", "Selecione uma disciplina para excluir.")

    def refresh_table(self):
        self.result_table.delete(*self.result_table.get_children())
        self.load_disciplinas()

    def clear_entries(self):
        self.disciplina_entry.delete(0, tk.END)
        self.av1_entry.delete(0, tk.END)
        self.av2_entry.delete(0, tk.END)
        self.av3_entry.delete(0, tk.END)
        self.av4_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Buscar por disciplina")

if __name__ == "__main__":
    root = tk.Tk()
    sistema_notas = SistemaNotas(root)
    root.mainloop()
