# -*- coding: utf-8 -*-
"""
Created on Sun May 26 17:26:08 2024

@author: Guilherme Sobral
"""

import tkinter as tk

# Função principal para iniciar o GUI
def main():
    root = tk.Tk()
    root.title("Sistema de Cadastro de Livros")

    # Funções de exemplo para os comandos dos botões
    def adicionar_livro():
        print("Função para adicionar livro chamada.")

    def listar_livros_disponiveis():
        print("Função para listar livros disponíveis chamada.")

    def pesquisar_livro():
        print("Função para pesquisar livro chamada.")

    def marcar_disponibilidade():
        print("Função para marcar disponibilidade chamada.")

    def exportar_para_excel():
        print("Função para exportar para Excel chamada.")

    # Botão para adicionar um livro
    btn_adicionar = tk.Button(root, text="Adicionar Livro", command=adicionar_livro)
    btn_adicionar.pack(pady=10)

    # Botão para listar livros disponíveis
    btn_listar = tk.Button(root, text="Listar Livros Disponíveis", command=listar_livros_disponiveis)
    btn_listar.pack(pady=10)

    # Botão para pesquisar um livro
    btn_pesquisar = tk.Button(root, text="Pesquisar Livro", command=pesquisar_livro)
    btn_pesquisar.pack(pady=10)

    # Botão para marcar a disponibilidade de um livro
    btn_marcar_disponibilidade = tk.Button(root, text="Marcar Disponibilidade", command=marcar_disponibilidade)
    btn_marcar_disponibilidade.pack(pady=10)

    # Botão para exportar dados para Excel
    btn_exportar = tk.Button(root, text="Exportar para Excel", command=exportar_para_excel)
    btn_exportar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
