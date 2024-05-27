import sqlite3  # Importa o módulo sqlite3 para interação com o banco de dados SQLite
import tkinter as tk  # Importa o módulo tkinter para criação da GUI
from openpyxl import Workbook  # Importa o módulo openpyxl para manipulação de arquivos Excel

# Função para conectar ao banco de dados e garantir que a tabela seja criada
def conectar_banco():
    conn = sqlite3.connect('biblioteca.db')  # Conecta-se ao banco de dados 'biblioteca.db'
    criar_tabela(conn)  # Chama a função para criar a tabela, se ela ainda não existir
    return conn  # Retorna a conexão com o banco de dados

# Função para criar a tabela se não existir
def criar_tabela(conn):
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
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
    """)  # Comando SQL para criar a tabela 'livros', se ela ainda não existir
    conn.commit()  # Salva as alterações no banco de dados

# Função para adicionar um novo livro
def adicionar_livro():
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Solicita ao usuário informações sobre o livro a ser adicionado
    numero_livro = input("Digite o número do livro: ")
    nome = input("Digite o nome do livro: ")
    editora = input("Digite a editora: ")
    autor = input("Digite o autor: ")
    sinopse = input("Digite a sinopse: ")
    disponibilidade = input("O livro está disponível? (sim/não): ")
    detalhes_extras = input("Detalhes extras: ")
    # Insere as informações do livro no banco de dados
    cursor.execute("INSERT INTO livros (numero_livro, nome, editora, autor, sinopse, disponibilidade, detalhes_extras) VALUES (?,?,?,?,?,?,?)",
                   (numero_livro, nome, editora, autor, sinopse, disponibilidade, detalhes_extras))
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados
    print("Livro adicionado com sucesso.")

# Função para listar livros disponíveis
def listar_livros_disponiveis():
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Executa um comando SQL para selecionar todos os livros onde 'disponibilidade' é 'sim'
    cursor.execute("SELECT * FROM livros WHERE disponibilidade = 'sim'")
    livros = cursor.fetchall()  # Obtém todas as linhas retornadas pelo comando SQL
    for livro in livros:  # Imprime cada livro encontrado
        print(livro)
    conn.close()  # Fecha a conexão com o banco de dados

# Função para pesquisar livros
def pesquisar_livro():
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Solicita ao usuário o número do livro a ser pesquisado
    livro_pesquisa = input("Digite o número do livro para pesquisar: ")
    # Executa um comando SQL para selecionar o livro com o número especificado
    cursor.execute("SELECT * FROM livros WHERE numero_livro =?", (livro_pesquisa,))
    livro_encontrado = cursor.fetchone()  # Obtém a primeira linha retornada pelo comando SQL
    if livro_encontrado:  # Se o livro foi encontrado
        print("Livro encontrado:", livro_encontrado)
    else:  # Se o livro não foi encontrado
        print("Livro não encontrado.")
    conn.close()  # Fecha a conexão com o banco de dados

# Função para marcar a disponibilidade
def marcar_disponibilidade():
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Solicita ao usuário o número do livro e a nova disponibilidade
    numero_livro = input("Digite o número do livro para marcar a disponibilidade: ")
    nova_disponibilidade = input("Digite 'sim' para disponível ou 'não' para indisponível: ")
    # Atualiza a disponibilidade do livro no banco de dados
    cursor.execute("UPDATE livros SET disponibilidade =? WHERE numero_livro =?", (nova_disponibilidade, numero_livro))
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados
    print("Disponibilidade atualizada com sucesso.")

# Função para exportar dados para Excel
def exportar_para_excel():
    workbook = Workbook()  # Cria um novo arquivo Excel
    worksheet = workbook.active  # Seleciona a planilha ativa
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Executa um comando SQL para selecionar todos os livros
    cursor.execute("SELECT * FROM livros")
    dados = cursor.fetchall()  # Obtém todas as linhas retornadas pelo comando SQL
    conn.close()  # Fecha a conexão com o banco de dados
    
    if dados:  # Verifica se há dados para exportar
        for linha in dados:  # Adiciona cada linha de dados à planilha do Excel
            worksheet.append(linha)
    
    workbook.save("livros.xlsx")  # Salva o arquivo Excel
    print("Dados exportados para Excel com sucesso.")

# Função para deletar um livro
def deletar_livro():
    conn = conectar_banco()  # Conecta-se ao banco de dados
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL
    # Solicita ao usuário o número do livro a ser deletado
    numero_livro = input("Digite o número do livro para deletar: ")
    # Deleta o livro do banco de dados
    cursor.execute("DELETE FROM livros WHERE numero_livro =?", (numero_livro,))
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados
    print("Livro deletado com sucesso.")

# Função principal para iniciar o GUI
def main():
    root = tk.Tk()  # Cria a janela principal da aplicação
    root.title("Sistema de Cadastro de Livros")  # Define o título da janela

    # Funções de exemplo para os comandos dos botões
    def adicionar_livro_gui():
        adicionar_livro()

    def listar_livros_disponiveis_gui():
        listar_livros_disponiveis()

    def pesquisar_livro_gui():
        pesquisar_livro()

    def marcar_disponibilidade_gui():
        marcar_disponibilidade()

    def exportar_para_excel_gui():
        exportar_para_excel()

    def deletar_livro_gui():
        deletar_livro()

    # Botão para adicionar um livro
    btn_adicionar = tk.Button(root, text="Adicionar Livro", command=adicionar_livro_gui)
    btn_adicionar.pack(pady=10)  # Adiciona o botão na janela

    # Botão para listar livros disponíveis
    btn_listar = tk.Button(root, text="Listar Livros Disponíveis", command=listar_livros_disponiveis_gui)
    btn_listar.pack(pady=10)  # Adiciona o botão na janela

    # Botão para pesquisar um livro
    btn_pesquisar = tk.Button(root, text="Pesquisar Livro", command=pesquisar_livro_gui)
    btn_pesquisar.pack(pady=10)  # Adiciona o botão na janela

    # Botão para marcar a disponibilidade de um livro
    btn_marcar_disponibilidade = tk.Button(root, text="Marcar Disponibilidade", command=marcar_disponibilidade_gui)
    btn_marcar_disponibilidade.pack(pady=10)  # Adiciona o botão na janela

    # Botão para exportar dados para Excel
    btn_exportar = tk.Button(root, text="Exportar para Excel", command=exportar_para_excel_gui)
    btn_exportar.pack(pady=10)  # Adiciona o botão na janela

    # Botão para deletar um livro
    btn_deletar = tk.Button(root, text="Deletar Livro", command=deletar_livro_gui)
    btn_deletar.pack(pady=10)  # Adiciona o botão na janela

    root.mainloop()  # Inicia o loop principal da aplicação

if __name__ == "__main__":
    main()  # Executa a função principal se este script for executado diretamente
