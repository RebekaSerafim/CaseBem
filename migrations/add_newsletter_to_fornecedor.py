"""
Script para adicionar campo newsletter à tabela fornecedor
Execute este script uma vez para atualizar o banco de dados
"""
import sqlite3
import os

def adicionar_campo_newsletter():
    """Adiciona o campo newsletter à tabela fornecedor se não existir"""
    try:
        # Conectar ao banco de dados
        db_path = "dados.db"
        if not os.path.exists(db_path):
            print(f"❌ Banco de dados não encontrado: {db_path}")
            return

        with sqlite3.connect(db_path) as conexao:
            cursor = conexao.cursor()

            # Verificar se a coluna já existe
            cursor.execute("PRAGMA table_info(fornecedor)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]

            if 'newsletter' not in colunas:
                # Adicionar a coluna newsletter
                cursor.execute("ALTER TABLE fornecedor ADD COLUMN newsletter BOOLEAN DEFAULT 0")
                print("✅ Campo newsletter adicionado à tabela fornecedor")
            else:
                print("ℹ️  Campo newsletter já existe na tabela fornecedor")

    except Exception as e:
        print(f"❌ Erro ao adicionar campo newsletter: {e}")

if __name__ == "__main__":
    adicionar_campo_newsletter()