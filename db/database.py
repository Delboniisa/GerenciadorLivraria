import sqlite3
import pandas as pd
from datetime import datetime

def conectar(db_path):
    return sqlite3.connect(db_path)    
    
def tabelaLivros(db_path):
    
    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER,
            genero TEXT,
            preco REAL
        )
    ''')
    conn.commit()
    

def excluirTabela(db_path):
    
    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE livros 
    ''')
    conn.commit()
    
        
def adicionarLivro(db_path):
    
    titulo = input("Título do livro: ")
    autor = input("Autor do livro: ")
    genero = input("Insira o gênero: ")
    
    #Validação de ano
    while True:
        try:
            ano_publicacao = int(input("Ano de Publicação: "))
            if 1000 <= ano_publicacao <= datetime.now().year:
                break
            else:
                print(f"Por favor, insira um ano válido entre 1000 e {datetime.now().year}.")
        except ValueError:
            print("Ano de publicação deve ser um número inteiro.")

    #Validação do preço
    while True:
        try:
            preco = float(input("Preço do livro (R$): "))
            if preco >= 0:
                break
            else:
                print("O preço deve ser um valor positivo.")
        except ValueError:
            print("Por favor, insira um valor numérico válido para o preço.")

    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor, genero,  ano, preco) VALUES (?, ?, ?, ?, ?)", 
                   (titulo, autor, genero, ano_publicacao, preco))
    conn.commit()
    conn.close()
    print(f'Livro "{titulo}" adicionado com sucesso!')
    #adicionar função e fazer backup automático
    
    
def obter_dados(db_path):
    conn = conectar(db_path)
    cursor = conn.cursor()
    
    # Executar uma consulta SQL
    cursor.execute("SELECT id, titulo, autor, ano, genero, preco FROM livros")
    
    # Recuperar todos os resultados
    dados = cursor.fetchall()
    
    # Recuperar os nomes das colunas
    colunas = [desc[0] for desc in cursor.description]
    
    conn.close()
    
    # Retornar os dados e os nomes das colunas
    return dados, colunas

def obter_dados_livros(db_path):
    conn = conectar(db_path)
    df = pd.read_sql_query("SELECT * FROM livros", conn)
    conn.close()
    return df

    
def exibirLivros(db_path):
        
        conn = conectar(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()
        conn.close()
    
        if livros:
            print("\n=== Lista de Livros Cadastrados ===")
            for livro in livros:
                print(f'ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Gênero: {livro[4]}, Preço: R${livro[5]:.2f}')
        else:
            print("Nenhum livro cadastrado.")
                   
            
def atualizarPreco(db_path):
    
    livro_id = input("ID do livro a ser atualizado: ")
    
    #Validação do novo preço
    while True:
        try:
            novo_preco = float(input("Novo preço do livro (R$): "))
            if novo_preco >= 0:
                break
            else:
                print("O preço deve ser um valor positivo.")
        except ValueError:
            print("Por favor, insira um valor numérico válido.")
    
    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE livros SET preco = ? WHERE id = ?", (novo_preco, livro_id))
    conn.commit()
    conn.close()
    print(f'Preço do livro com ID {livro_id} atualizado para R${novo_preco:.2f}')
    #adicionar função e fazer backup automático

    
    
def removerLivro(db_path):
    
    livro_id = input("ID do livro a ser removido: ")
    
    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    conn.commit()
    conn.close()
    print(f'Livro com ID {livro_id} removido com sucesso!')
    #adicionar função e fazer backup automático


def buscarLivroPorAutor(db_path):
    
    autor = input("Digite o nome do autor: ").upper()
    
    conn = conectar(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE autor LIKE ?", (f'%{autor}%',))
    livros = cursor.fetchall()
    conn.close()

    if livros:
        print("\n=== Livros de {autor} ===")
        for livro in livros:
            print(f'ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Gênero: {livro[4]}, Preço: R${livro[5]:.2f}')
    else:
         print("Nenhum livro cadastrado.")

    
                   
        
