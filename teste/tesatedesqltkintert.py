import sqlite3
import tkinter as tk
from tkinter import ttk

# Função para conectar ao banco de dados
def conectar_banco():
    db_path = 'database.db'
    return sqlite3.connect(db_path)

# Função para criar a tabela se ela não existir
def criar_tabela(conexao):
    cursor = conexao.cursor()
    query = '''CREATE TABLE IF NOT EXISTS SUPLEMENTO (LOTE INT, PRODUTO TEXT, FORNECEDOR TEXT)'''
    cursor.execute(query)
    conexao.commit()

# Função para preencher a tabela com os dados do banco de dados
def preencher_tabela(conexao, tree):
    cursor = conexao.cursor()
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='SUPLEMENTO';''')
    if cursor.fetchone() is None:
        criar_tabela(conexao)
    cursor.execute("SELECT * FROM SUPLEMENTO")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

# Inicialização da interface gráfica
root = tk.Tk()
root.title("Sistema de Gerenciamento de Suplementos Alimentares")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Criando widgets
entry_lote = ttk.Entry(frame)
entry_produto = ttk.Entry(frame)
combo_fornecedor = ttk.Combobox(frame, values=['Fornecedor 1', 'Fornecedor 2', 'Fornecedor 3'])
tree = ttk.Treeview(frame, columns=('Lote', 'Produto', 'Fornecedor'), show='headings')
tree.heading('Lote', text='Lote')
tree.heading('Produto', text='Produto')
tree.heading('Fornecedor', text='Fornecedor')

# Conectando widgets com funções
ttk.Button(frame, text="Preencher Tabela", command=lambda: preencher_tabela(conexao, tree)).grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

# Preenchendo a tabela inicialmente
conexao = conectar_banco()
preencher_tabela(conexao, tree)
conexao.close()

# Execução do loop principal
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
root.mainloop()
