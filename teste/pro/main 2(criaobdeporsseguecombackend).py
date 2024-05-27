import sqlite3
import pandas as pd

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('biblioteca.db', check_same_thread=False)
    return conn

# Função para criar a tabela se ela não existir
def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero_livro TEXT UNIQUE,
                        nome TEXT,
                        editora TEXT,
                        autor TEXT,
                        sinopse TEXT,
                        disponibilidade TEXT CHECK(disponibilidade IN ('sim', 'não')),
                        detalhes_extras TEXT)''')
    conn.commit()

# Função para adicionar um novo livro
def adicionar_livro(conn, nome, numero_livro, editora, autor, sinopse, disponibilidade, detalhes_extras):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livros (nome, numero_livro, editora, autor, sinopse, disponibilidade, detalhes_extras) VALUES (?,?,?,?,?,?,?)",
                   (nome, numero_livro, editora, autor, sinopse, disponibilidade, detalhes_extras))
    conn.commit()

# Função para listar todos os livros
def listar_livros(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros ORDER BY id")
    livros = cursor.fetchall()
    return livros

# Função para modificar um livro existente
def modificar_livro(conn, id, nome=None, numero_livro=None, editora=None, autor=None, sinopse=None, disponibilidade=None, detalhes_extras=None):
    cursor = conn.cursor()
    params = {'nome': nome, 'numero_livro': numero_livro, 'editora': editora, 'autor': autor, 'sinopse': sinopse, 'disponibilidade': disponibilidade, 'detalhes_extras': detalhes_extras}
    if params:
        set_clause = ', '.join([f"{key} =?" for key in params])
        where_clause = f"id = {id}"
        cursor.execute(f"UPDATE livros SET {set_clause} WHERE {where_clause}", tuple(params.values()))
    conn.commit()

# Função para excluir um livro
def excluir_livro(conn, id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id =?", (id,))
    conn.commit()

# Função para listar livros por disponibilidade
def listar_por_disponibilidade(conn, disponibilidade):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE disponibilidade =?", (disponibilidade,))
    livros = cursor.fetchall()
    return livros

# Função para pesquisar um livro pelo número
def pesquisar_livro(conn, numero_livro):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE numero_livro =?", (numero_livro,))
    livro = cursor.fetchone()
    return livro

# Função para marcar a disponibilidade de um livro
def marcar_disponibilidade(conn, numero_livro, nova_disponibilidade):
    cursor = conn.cursor()
    cursor.execute("UPDATE livros SET disponibilidade =? WHERE numero_livro =?", (nova_disponibilidade, numero_livro))
    conn.commit()

# Função para exportar dados para Excel
def exportar_para_excel(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    dados = cursor.fetchall()
    df = pd.DataFrame(dados, columns=['ID', 'Número do Livro', 'Nome', 'Editora', 'Autor', 'Sinopse', 'Disponibilidade', 'Detalhes Extras'])
    df.to_excel('livros.xlsx', index=False)

# Função principal para executar as operações
def main():
    conn = conectar_banco()
    criar_tabela(conn)

    # Adicionando um livro de exemplo
    adicionar_livro(conn, "O Poder do Pensamento", "1234567890", "Editora X", "João Silva", "Uma história inspiradora", "sim", "Detalhes adicionais...")

    # Listando todos os livros
    print("Todos os livros:")
    print(listar_livros(conn))

    # Modificando um livro
    modificar_livro(conn, 1, nome="Novo Nome", disponibilidade="não")

    # Excluindo um livro
    excluir_livro(conn, 1)

    # Listando livros por disponibilidade
    print("\nLivros Disponíveis:")
    print(listar_por_disponibilidade(conn, "sim"))
    print("\n\nLivros Indisponíveis:")
    print(listar_por_disponibilidade(conn, "não"))

    # Pesquisando um livro
    print("\n\nPesquisando livro pelo número:")
    print(pesquisar_livro(conn, "1234567890"))

    # Marcando a disponibilidade de um livro
    marcar_disponibilidade(conn, "1234567890", "sim")

    # Exportando para Excel
    exportar_para_excel(conn)

    conn.close()

if __name__ == "__main__":
    main()
