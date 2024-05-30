# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:58:29 2024

@author: Guilherme Sobral
"""

import tkinter as tk
import os
import sqlite3

diretorio_corrente = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(diretorio_corrente, 'database.db')

# Criando a tabela se ela não existir
conexao = sqlite3.connect(db_path)
query = ('''CREATE TABLE IF NOT EXISTS SUPLEMENTO (LOTE INT, PRODUTO TEXT, FORNECEDOR TEXT)''')
conexao.execute(query)
conexao.close()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.Titulos = ['Lote', 'Produto', 'Fornecedor']
        self.dados = []

        # Criação dos campos de entrada e botões
        for titulo in self.Titulos:
            self[titulo] = tk.Entry(self)
            self[titulo].pack(side="top")

        self.adicionar_button = tk.Button(self)
        self.adicionar_button["text"] = "Adicionar"
        self.adicionar_button["command"] = self.adicionar
        self.adicionar_button.pack(side="top")

        self.editar_button = tk.Button(self)
        self.editar_button["text"] = "Editar"
        self.editar_button["command"] = self.editar
        self.editar_button.pack(side="top")

        self.salvar_button = tk.Button(self)
        self.salvar_button["text"] = "Salvar"
        self.salvar_button["command"] = self.salvar
        self.salvar_button.pack(side="top")

        self.excluir_button = tk.Button(self)
        self.excluir_button["text"] = "Excluir"
        self.excluir_button["command"] = self.excluir
        self.excluir_button.pack(side="top")

        self.sair_button = tk.Button(self)
        self.sair_button["text"] = "Sair"
        self.sair_button["command"] = self.quit
        self.sair_button.pack(side="top")

    def adicionar(self):
        lote = self.Lote.get()
        produto = self.Produto.get()
        fornecedor = self.Fornecedor.get()
        self.dados.append((lote, produto, fornecedor))

        # Atualizar a tabela (neste exemplo, apenas adicionamos uma linha fictícia)
        self.tree.insert('', 'end', text="", values=(lote, produto, fornecedor))

        # Limpar campos
        for widget in self.winfo_children():
            widget.destroy()

        # Conectar ao banco de dados para inserir os dados
        conexao = sqlite3.connect(db_path)
        conexao.execute("INSERT INTO SUPLEMENTO (LOTE, PRODUTO, FORNECEDOR) VALUES (?,?,?)", (lote, produto, fornecedor))
        conexao.commit()
        conexao.close()

    def editar(self):
        try:
            # Seleciona a linha atualmente selecionada na tabela
            selected_item = self.tree.selection()[0]
            # Pega os valores da linha selecionada
            lote, produto, fornecedor = self.tree.item(selected_item)['values']
            # Preenche os campos de entrada com os valores selecionados
            self.Lote.delete(0, tk.END)
            self.Lote.insert(0, lote)
            self.Produto.delete(0, tk.END)
            self.Produto.insert(0, produto)
            self.Fornecedor.delete(0, tk.END)
            self.Fornecedor.insert(0, fornecedor)
        except IndexError:
            tk.messagebox.showerror(title="Erro", message="Por favor, selecione uma linha para editar.")

    def salvar(self):
        try:
            # Obtém os novos valores dos campos de entrada
            lote = self.Lote.get()
            produto = self.Produto.get()
            fornecedor = self.Fornecedor.get()
            # Atualiza a linha selecionada na tabela
            selected_item = self.tree.selection()[0]
            self.tree.item(selected_item, values=(lote, produto, fornecedor))
            # Atualiza a linha selecionada no banco de dados
            conexao = sqlite3.connect(db_path)
            conexao.execute("UPDATE SUPLEMENTO SET PRODUTO =?, FORNECEDOR =? WHERE LOTE =?", (produto, fornecedor, lote))
            conexao.commit()
            conexao.close()
        except IndexError:
            tk.messagebox.showerror(title="Erro", message="Por favor, selecione uma linha para salvar.")

    def excluir(self):
        try:
            # Obtém a linha selecionada
            selected_item = self.tree.selection()[0]
            # Remove a linha da tabela
            self.tree.delete(selected_item)
            # Remove a linha do banco de dados
            conexao = sqlite3.connect(db_path)
            conexao.execute("DELETE FROM SUPLEMENTO WHERE LOTE =?", (self.Lote.get(),))
            conexao.commit()
            conexao.close()
        except IndexError:
            tk.messagebox.showerror(title="Erro", message="Por favor, selecione uma linha para excluir.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
