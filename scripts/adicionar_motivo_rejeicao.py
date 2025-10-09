"""
Script de migração para adicionar campo motivo_rejeicao em item_orcamento.

IMPORTANTE: Este campo permite que o noivo forneça um motivo
ao rejeitar um item do orçamento, melhorando a comunicação
com os fornecedores.

Rodar: python scripts/adicionar_motivo_rejeicao.py
"""

import sqlite3
from infrastructure.database import obter_conexao
from infrastructure.logging import logger


def verificar_coluna_existe(cursor: sqlite3.Cursor, tabela: str, coluna: str) -> bool:
    """Verifica se uma coluna já existe em uma tabela"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [row[1] for row in cursor.fetchall()]
    return coluna in colunas


def adicionar_motivo_rejeicao():
    """Adiciona coluna motivo_rejeicao na tabela item_orcamento"""
    conn = obter_conexao()
    cursor = conn.cursor()

    try:
        # Verificar se coluna já existe
        if verificar_coluna_existe(cursor, "item_orcamento", "motivo_rejeicao"):
            logger.info("Coluna 'motivo_rejeicao' já existe na tabela item_orcamento")
            print("✅ Coluna 'motivo_rejeicao' já existe - migração não necessária")
            return True

        # Adicionar coluna
        sql = """
        ALTER TABLE item_orcamento
        ADD COLUMN motivo_rejeicao TEXT;
        """

        cursor.execute(sql)
        conn.commit()

        logger.info("Coluna 'motivo_rejeicao' adicionada com sucesso à tabela item_orcamento")
        print("✅ Coluna 'motivo_rejeicao' adicionada com sucesso!")

        # Verificar que foi adicionada
        if verificar_coluna_existe(cursor, "item_orcamento", "motivo_rejeicao"):
            print("✅ Verificação: Coluna existe no banco de dados")
            return True
        else:
            logger.error("Coluna não foi adicionada corretamente")
            print("❌ ERRO: Coluna não foi adicionada corretamente")
            return False

    except sqlite3.Error as e:
        logger.error(f"Erro ao adicionar coluna motivo_rejeicao: {e}")
        print(f"❌ ERRO: {e}")
        return False

    finally:
        conn.close()


def verificar_estrutura_tabela():
    """Exibe a estrutura atual da tabela item_orcamento"""
    conn = obter_conexao()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(item_orcamento)")
        colunas = cursor.fetchall()

        print("\n📋 Estrutura da tabela item_orcamento:")
        print("-" * 70)
        for col in colunas:
            col_id, nome, tipo, not_null, default, pk = col
            nullable = "NOT NULL" if not_null else "NULL"
            pk_str = " PRIMARY KEY" if pk else ""
            default_str = f" DEFAULT {default}" if default else ""
            print(f"  {nome:20} {tipo:10} {nullable:10}{default_str}{pk_str}")
        print("-" * 70)

    except sqlite3.Error as e:
        logger.error(f"Erro ao verificar estrutura da tabela: {e}")
        print(f"❌ ERRO: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    print("🔧 Adicionando campo motivo_rejeicao à tabela item_orcamento...")
    print("=" * 70)

    # Mostrar estrutura antes
    print("\n📊 ESTRUTURA ANTES DA MIGRAÇÃO:")
    verificar_estrutura_tabela()

    # Executar migração
    print("\n⚙️  EXECUTANDO MIGRAÇÃO:")
    sucesso = adicionar_motivo_rejeicao()

    # Mostrar estrutura depois
    if sucesso:
        print("\n📊 ESTRUTURA APÓS A MIGRAÇÃO:")
        verificar_estrutura_tabela()

    print("=" * 70)
    if sucesso:
        print("✨ Migração concluída com sucesso!\n")
    else:
        print("❌ Migração falhou. Verifique os logs.\n")
