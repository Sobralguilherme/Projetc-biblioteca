import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook

# Função para conectar ao banco de dados e garantir que a tabela seja criada
def conectar_banco():
    conn = sqlite3.connect('biblioteca.db')
    criar_tabela(conn)
    return conn

# Função para criar a tabela se não existir
def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_livro TEXT,
        nome TEXT,
        editora TEXT,
        autor TEXT,
        sinopse TEXT,
        disponibilidade TEXT,
        detalhes_extras TEXT
    );
    """)
    conn.commit()

# Função para adicionar um novo livro
def adicionar_livro_gui():
    conn = conectar_banco()
    cursor = conn.cursor()
    numero_livro = entry_numero_livro.get()
    nome = entry_nome.get()
    editora = entry_editora.get()
    autor = entry_autor.get()
    sinopse = entry_sinopse.get()
    disponibilidade = var_disponibilidade.get()
    detalhes_extras = entry_detalhes_extras.get("1.0", tk.END)
    cursor.execute("INSERT INTO livros (numero_livro, nome, editora, autor, sinopse, disponibilidade, detalhes_extras) VALUES (?,?,?,?,?,?,?)",
                   (numero_livro, nome, editora, autor, sinopse, disponibilidade, detalhes_extras))
    conn.commit()
    conn.close()
    listar_livros_treeview()
    messagebox.showinfo("Sucesso", "Livro adicionado com sucesso.")

# Função para listar livros disponíveis
def listar_livros_treeview():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE disponibilidade ='sim'")
    livros = cursor.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
    for livro in livros:
        tree.insert('', 'end', values=livro)

# Função para pesquisar livros
def pesquisar_livro_gui():
    conn = conectar_banco()
    cursor = conn.cursor()
    numero_livro = entry_numero_livro_pesquisa.get()
    cursor.execute("SELECT * FROM livros WHERE numero_livro=?", (numero_livro,))
    livro_encontrado = cursor.fetchone()
    conn.close()
    if livro_encontrado:
        messagebox.showinfo("Resultado da Pesquisa", str(livro_encontrado))
    else:
        messagebox.showinfo("Resultado da Pesquisa", "Livro não encontrado.")

# Função para marcar a disponibilidade
def marcar_disponibilidade_gui():
    conn = conectar_banco()
    cursor = conn.cursor()
    numero_livro = entry_numero_livro_disponibilidade.get()
    nova_disponibilidade = var_nova_disponibilidade.get()
    cursor.execute("UPDATE livros SET disponibilidade =? WHERE numero_livro =?", (nova_disponibilidade, numero_livro))
    conn.commit()
    conn.close()
    listar_livros_treeview()
    messagebox.showinfo("Sucesso", "Disponibilidade atualizada com sucesso.")

# Função para exportar dados para Excel
def exportar_para_excel_gui():
    workbook = Workbook()
    worksheet = workbook.active
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    dados = cursor.fetchall()
    conn.close()
    if dados:
        for linha in dados:
            worksheet.append(linha)
    workbook.save("livros.xlsx")
    messagebox.showinfo("Sucesso", "Dados exportados para Excel com sucesso.")

# Função para deletar um livro
def deletar_livro_gui():
    conn = conectar_banco()
    cursor = conn.cursor()
    numero_livro = entry_numero_livro_deletar.get()
    cursor.execute("DELETE FROM livros WHERE numero_livro=?", (numero_livro,))
    conn.commit()
    conn.close()
    listar_livros_treeview()
    messagebox.showinfo("Sucesso", "Livro deletado com sucesso.")

# Função principal para iniciar o GUI
def main():
    global tree, entry_numero_livro, entry_nome, entry_editora, entry_autor, entry_sinopse, var_disponibilidade, entry_detalhes_extras
    global entry_numero_livro_pesquisa, entry_numero_livro_disponibilidade, var_nova_disponibilidade, entry_numero_livro_deletar
    
    root = tk.Tk()
    root.title("Sistema de Cadastro de Livros")

    # Widgets de entrada
    tk.Label(root, text="Número do Livro").grid(row=0, column=0)
    entry_numero_livro = tk.Entry(root)
    entry_numero_livro.grid(row=0, column=1)
    tk.Label(root, text="Nome").grid(row=1, column=0)
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=1, column=1)
    tk.Label(root, text="Editora").grid(row=2, column=0)
    entry_editora = tk.Entry(root)
    entry_editora.grid(row=2, column=1)
    tk.Label(root, text="Autor").grid(row=3, column=0)
    entry_autor = tk.Entry(root)
    entry_autor.grid(row=3, column=1)
    tk.Label(root, text="Sinopse").grid(row=4, column=0)
    entry_sinopse = tk.Entry(root)
    entry_sinopse.grid(row=4, column=1)
    tk.Label(root, text="Disponibilidade").grid(row=5, column=0)
    var_disponibilidade = tk.StringVar()
    entry_disponibilidade = ttk.Combobox(root, textvariable=var_disponibilidade, values=["sim", "não"])
    entry_disponibilidade.grid(row=5, column=1)
    tk.Label(root, text="Detalhes Extras").grid(row=6, column=0)
    entry_detalhes_extras = tk.Text(root, height=5, width=30)
    entry_detalhes_extras.grid(row=6, column=1)

    # Árvore para listar livros
    tree = ttk.Treeview(root, columns=('ID', 'Numero do Livro', 'Nome', 'Editora', 'Autor', 'Sinopse', 'Disponibilidade', 'Detalhes Extras'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Numero do Livro', text='Número do Livro')
    tree.heading('Nome', text='Nome')
    tree.heading('Editora', text='Editora')
    tree.heading('Autor', text='Autor')
    tree.heading('Sinopse', text='Sinopse')
    tree.heading('Disponibilidade', text='Disponibilidade')
    tree.heading('Detalhes Extras', text='Detalhes Extras')
    tree.grid(row=7, column=0, columnspan=2)

    # Botões
    btn_adicionar = tk.Button(root, text="Adicionar Livro", command=adicionar_livro_gui)
    btn_adicionar.grid(row=8, column=0, pady=5)
    btn_listar = tk.Button(root, text="Listar Livros Disponíveis", command=listar_livros_treeview)
    btn_listar.grid(row=8, column=1, pady=5)
    tk.Label(root, text="Número do Livro para Pesquisar").grid(row=9, column=0)
    entry_numero_livro_pesquisa = tk.Entry(root)
    entry_numero_livro_pesquisa.grid(row=9, column=1)
    btn_pesquisar = tk.Button(root, text="Pesquisar Livro", command=pesquisar_livro_gui)
    btn_pesquisar.grid(row=10, column=0, pady=5)
    tk.Label(root, text="Número do Livro para Marcar Disponibilidade").grid(row=11, column=0)
    entry_numero_livro_disponibilidade = tk.Entry(root)
    entry_numero_livro_disponibilidade.grid(row=11, column=1)
    tk.Label(root, text="Nova Disponibilidade").grid(row=12, column=0)
    var_nova_disponibilidade = tk.StringVar()
    entry_nova_disponibilidade = ttk.Combobox(root, textvariable=var_nova_disponibilidade, values=["sim", "não"])
    entry_nova_disponibilidade.grid(row=12, column=1)
    btn_marcar_disponibilidade = tk.Button(root, text="Marcar Disponibilidade", command=marcar_disponibilidade_gui)
    btn_marcar_disponibilidade.grid(row=13, column=0, pady=5)
    btn_exportar = tk.Button(root, text="Exportar para Excel", command=exportar_para_excel_gui)
    btn_exportar.grid(row=13, column=1, pady=5)
    tk.Label(root, text="Número do Livro para Deletar").grid(row=14, column=0)
    entry_numero_livro_deletar = tk.Entry(root)
    entry_numero_livro_deletar.grid(row=14, column=1)
    btn_deletar = tk.Button(root, text="Deletar Livro", command=deletar_livro_gui)
    btn_deletar.grid(row=15, column=0, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
