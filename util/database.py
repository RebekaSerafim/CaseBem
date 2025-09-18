import sqlite3
import os
from util.sqlite_adapters import register_adapters

def obter_conexao():
    # Registra os adaptadores customizados para datetime
    register_adapters()
    # Obtém o caminho do banco de dados a partir da variável de ambiente de testes ou usa o padrão
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    # Conecta ao banco de dados SQLite
    conexao = sqlite3.connect(database_path)
    # Ativa as chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON")
    # Define a fábrica de linhas para retornar dicionários
    conexao.row_factory = sqlite3.Row
    # Retorna a conexão com o banco de dados
    return conexao