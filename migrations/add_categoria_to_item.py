import sqlite3
from util.database import obter_conexao

def add_categoria_to_item():
    """Adiciona o campo id_categoria à tabela item"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Verificar se a coluna já existe
            cursor.execute("PRAGMA table_info(item)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]

            if 'id_categoria' not in colunas:
                # Adicionar a coluna id_categoria
                cursor.execute("""
                    ALTER TABLE item
                    ADD COLUMN id_categoria INTEGER
                    REFERENCES categoria(id)
                """)
                print("Campo id_categoria adicionado à tabela item com sucesso")
            else:
                print("Campo id_categoria já existe na tabela item")

    except Exception as e:
        print(f"Erro ao adicionar campo id_categoria à tabela item: {e}")
        return False

    return True

if __name__ == "__main__":
    add_categoria_to_item()