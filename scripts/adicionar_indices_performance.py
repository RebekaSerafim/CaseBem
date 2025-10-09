"""
Script de migração para adicionar índices de performance.

IMPORTANTE: Índices melhoram significativamente a performance de queries
frequentes, especialmente em tabelas que fazem JOINs e filtros.

Rodar: python scripts/adicionar_indices_performance.py
"""

import sqlite3
from infrastructure.database import obter_conexao
from infrastructure.logging import logger


def adicionar_indices():
    """Adiciona índices de performance ao banco de dados"""
    conn = obter_conexao()
    cursor = conn.cursor()

    indices = [
        # ÍNDICES EM DEMANDA
        ("idx_demanda_id_casal", "CREATE INDEX IF NOT EXISTS idx_demanda_id_casal ON demanda(id_casal)"),
        ("idx_demanda_status", "CREATE INDEX IF NOT EXISTS idx_demanda_status ON demanda(status)"),
        ("idx_demanda_cidade", "CREATE INDEX IF NOT EXISTS idx_demanda_cidade_casamento ON demanda(cidade_casamento)"),
        ("idx_demanda_data_criacao", "CREATE INDEX IF NOT EXISTS idx_demanda_data_criacao ON demanda(data_criacao DESC)"),

        # ÍNDICES EM ITEM_DEMANDA
        ("idx_item_demanda_id_demanda", "CREATE INDEX IF NOT EXISTS idx_item_demanda_id_demanda ON item_demanda(id_demanda)"),
        ("idx_item_demanda_tipo_categoria", "CREATE INDEX IF NOT EXISTS idx_item_demanda_tipo_categoria ON item_demanda(tipo, id_categoria)"),
        ("idx_item_demanda_id_categoria", "CREATE INDEX IF NOT EXISTS idx_item_demanda_id_categoria ON item_demanda(id_categoria)"),

        # ÍNDICES EM ORCAMENTO
        ("idx_orcamento_id_demanda", "CREATE INDEX IF NOT EXISTS idx_orcamento_id_demanda ON orcamento(id_demanda)"),
        ("idx_orcamento_id_fornecedor", "CREATE INDEX IF NOT EXISTS idx_orcamento_id_fornecedor ON orcamento(id_fornecedor_prestador)"),
        ("idx_orcamento_status", "CREATE INDEX IF NOT EXISTS idx_orcamento_status ON orcamento(status)"),
        ("idx_orcamento_data_cadastro", "CREATE INDEX IF NOT EXISTS idx_orcamento_data_cadastro ON orcamento(data_hora_cadastro DESC)"),

        # ÍNDICES EM ITEM_ORCAMENTO
        ("idx_item_orcamento_id_orcamento", "CREATE INDEX IF NOT EXISTS idx_item_orcamento_id_orcamento ON item_orcamento(id_orcamento)"),
        ("idx_item_orcamento_id_item_demanda", "CREATE INDEX IF NOT EXISTS idx_item_orcamento_id_item_demanda ON item_orcamento(id_item_demanda)"),
        ("idx_item_orcamento_id_item", "CREATE INDEX IF NOT EXISTS idx_item_orcamento_id_item ON item_orcamento(id_item)"),
        ("idx_item_orcamento_status", "CREATE INDEX IF NOT EXISTS idx_item_orcamento_status ON item_orcamento(status)"),
        # Índice composto para verificação de duplicatas
        ("idx_item_orc_dup", "CREATE INDEX IF NOT EXISTS idx_item_orc_duplicata ON item_orcamento(id_orcamento, id_item_demanda, id_item)"),
        # Índice composto para aceitação
        ("idx_item_orc_aceito", "CREATE INDEX IF NOT EXISTS idx_item_orc_item_demanda_status ON item_orcamento(id_item_demanda, status)"),

        # ÍNDICES EM ITEM (para JOINs frequentes)
        ("idx_item_id_fornecedor", "CREATE INDEX IF NOT EXISTS idx_item_id_fornecedor ON item(id_fornecedor)"),
        ("idx_item_id_categoria", "CREATE INDEX IF NOT EXISTS idx_item_id_categoria ON item(id_categoria)"),
        ("idx_item_tipo_categoria", "CREATE INDEX IF NOT EXISTS idx_item_tipo_categoria ON item(tipo, id_categoria)"),
        ("idx_item_ativo", "CREATE INDEX IF NOT EXISTS idx_item_ativo ON item(ativo)"),

        # ÍNDICES EM CASAL (para JOINs com demanda e orçamento)
        ("idx_casal_id_noivo1", "CREATE INDEX IF NOT EXISTS idx_casal_id_noivo1 ON casal(id_noivo1)"),
        ("idx_casal_id_noivo2", "CREATE INDEX IF NOT EXISTS idx_casal_id_noivo2 ON casal(id_noivo2)"),
    ]

    total_criados = 0
    for nome_indice, sql in indices:
        try:
            cursor.execute(sql)
            logger.info(f"Índice '{nome_indice}' criado/verificado com sucesso")
            total_criados += 1
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar índice '{nome_indice}': {e}")

    conn.commit()
    conn.close()

    logger.info(f"Total de {total_criados}/{len(indices)} índices criados/verificados")
    print(f"\n✅ {total_criados}/{len(indices)} índices de performance criados/verificados com sucesso!")

    return total_criados


if __name__ == "__main__":
    print("🔧 Adicionando índices de performance ao banco de dados...")
    print("=" * 70)
    adicionar_indices()
    print("=" * 70)
    print("✨ Migração concluída!\n")
