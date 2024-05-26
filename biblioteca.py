import csv
import sqlite3
import tkinter as tk
from openpyxl import Workbook

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('biblioteca.db')
    return conn

# Função para abrir o arquivo CSV
def abrir_arquivo():
    try:
        arquivo = open("livros.csv", "r")
        return csv.reader(arquivo)
    except FileNotFoundError:
        return None

# Função para salvar os dados no arquivo CSV
def salvar_dados(dados):
    with open("livros.csv", "w", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerows(dados)

# Função para adicionar um novo livro
def adicionar_livro():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    numero_livro = input("Digite o número do livro: ")
    nome = input("Digite o nome do livro: ")
    editora = input("Digite a editora: ")
    autor = input("Digite o autor: ")
    sinopse = input("Digite a sinopse: ")
    disponibilidade = input("O livro está disponível? (sim/não): ")
    detalhes_extras = input("Detalhes extras: ")
    cursor.execute("INSERT INTO livros VALUES (NULL,?,?,?,?,?,?,?)",
                    (numero_livro, nome, editora, autor, sinopse, disponibilidade, detalhes_extras))
    conn.commit()
    conn.close()
    print("Livro adicionado com sucesso.")
    
# Função para listar livros disponíveis
def listar_livros_disponiveis():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE disponibilidade = 'sim'")
    livros = cursor.fetchall()
    print(livros)
    conn.close()

# Função para pesquisar livros
def pesquisar_livro():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    livro_pesquisa = input("Digite o número do livro para pesquisar: ")
    cursor.execute("SELECT * FROM livros WHERE numero_livro =?", (livro_pesquisa,))
    livro_encontrado = cursor.fetchone()
    if livro_encontrado:
        print("Livro encontrado:", livro_encontrado)
    else:
        print("Livro não encontrado.")
    conn.close()

# Função para marcar a disponibilidade
def marcar_disponibilidade():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    numero_livro = input("Digite o número do livro para marcar a disponibilidade: ")
    nova_disponibilidade = input("Digite 'sim' para disponível ou 'não' para indisponível: ")
    cursor.execute("UPDATE livros SET disponibilidade =? WHERE numero_livro =?", (nova_disponibilidade, numero_livro))
    conn.commit()
    conn.close()
    print("Disponibilidade atualizada com sucesso.")

# Função para exportar dados para Excel
def exportar_para_excel():
    workbook = Workbook()
    worksheet = workbook.active
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    dados = cursor.fetchall()
    conn.close()
    
    if dados:
        for linha in dados:
            worksheet.append(linha)
    
    workbook.save("livros.xlsx")
    print("Dados exportados para Excel com sucesso.")

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

