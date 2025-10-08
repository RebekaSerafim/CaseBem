#!/usr/bin/env python3
"""
Script de migração: Adicionar status em item_orcamento

Este script adiciona o campo 'status' na tabela item_orcamento e migra
os dados existentes com base no status do orçamento pai.

Migração:
- Itens de orçamentos ACEITOS → status = ACEITO
- Itens de orçamentos REJEITADOS → status = REJEITADO
- Itens de orçamentos PENDENTES → status = PENDENTE

Autor: Sistema CaseBem
Data: 2025-10-08
"""

import sqlite3
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.logging import logger

DB_PATH = ROOT_DIR / "dados.db"


def executar_migracao():
    """Executa a migração do banco de dados"""

    logger.info("Iniciando migração: adicionar status em item_orcamento")

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 1. Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(item_orcamento)")
        colunas = [col[1] for col in cursor.fetchall()]

        if "status" in colunas:
            logger.warning("Coluna 'status' já existe em item_orcamento. Migração não necessária.")
            conn.close()
            return

        logger.info("Adicionando coluna 'status' em item_orcamento...")

        # 2. Adicionar coluna status
        cursor.execute("""
            ALTER TABLE item_orcamento
            ADD COLUMN status TEXT NOT NULL DEFAULT 'PENDENTE'
        """)

        logger.info("Coluna 'status' adicionada com sucesso")

        # 3. Migrar dados existentes
        logger.info("Migrando dados existentes...")

        cursor.execute("""
            UPDATE item_orcamento
            SET status = (
                SELECT o.status
                FROM orcamento o
                WHERE o.id = item_orcamento.id_orcamento
            )
        """)

        linhas_afetadas = cursor.rowcount
        logger.info(f"Dados migrados: {linhas_afetadas} itens atualizados")

        # 4. Criar índice para performance
        logger.info("Criando índice para coluna status...")

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_item_orcamento_status
            ON item_orcamento(status)
        """)

        logger.info("Índice criado com sucesso")

        # 5. Verificar migração
        cursor.execute("""
            SELECT status, COUNT(*) as total
            FROM item_orcamento
            GROUP BY status
        """)

        resultados = cursor.fetchall()
        logger.info("Verificação da migração:")
        for row in resultados:
            logger.info(f"  - Status {row['status']}: {row['total']} itens")

        # Commit das mudanças
        conn.commit()
        logger.info("✅ Migração concluída com sucesso!")

    except sqlite3.Error as e:
        logger.error(f"Erro na migração: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()


def reverter_migracao():
    """Reverte a migração (remove coluna status)"""

    logger.warning("⚠️  REVERTENDO migração: remover status de item_orcamento")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQLite não suporta DROP COLUMN diretamente
        # Precisamos recriar a tabela sem a coluna

        logger.info("Criando tabela temporária...")

        cursor.execute("""
            CREATE TABLE item_orcamento_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_orcamento INTEGER NOT NULL,
                id_item_demanda INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                preco_unitario REAL NOT NULL,
                observacoes TEXT,
                desconto REAL DEFAULT 0,
                FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
                FOREIGN KEY (id_item_demanda) REFERENCES item_demanda(id) ON DELETE CASCADE,
                FOREIGN KEY (id_item) REFERENCES item(id) ON DELETE CASCADE,
                UNIQUE(id_orcamento, id_item_demanda, id_item)
            )
        """)

        logger.info("Copiando dados...")

        cursor.execute("""
            INSERT INTO item_orcamento_temp
                (id, id_orcamento, id_item_demanda, id_item, quantidade,
                 preco_unitario, observacoes, desconto)
            SELECT id, id_orcamento, id_item_demanda, id_item, quantidade,
                   preco_unitario, observacoes, desconto
            FROM item_orcamento
        """)

        logger.info("Removendo tabela original...")
        cursor.execute("DROP TABLE item_orcamento")

        logger.info("Renomeando tabela temporária...")
        cursor.execute("ALTER TABLE item_orcamento_temp RENAME TO item_orcamento")

        logger.info("Recriando índices...")
        cursor.execute("""
            CREATE INDEX idx_item_orcamento_orcamento
            ON item_orcamento(id_orcamento)
        """)
        cursor.execute("""
            CREATE INDEX idx_item_orcamento_item_demanda
            ON item_orcamento(id_item_demanda)
        """)
        cursor.execute("""
            CREATE INDEX idx_item_orcamento_item
            ON item_orcamento(id_item)
        """)

        conn.commit()
        logger.info("✅ Reversão concluída com sucesso!")

    except sqlite3.Error as e:
        logger.error(f"Erro na reversão: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--revert":
        print("⚠️  ATENÇÃO: Você está prestes a REVERTER a migração!")
        print("Isso removerá o campo 'status' de item_orcamento.")
        resposta = input("Digite 'CONFIRMAR' para continuar: ")

        if resposta == "CONFIRMAR":
            reverter_migracao()
        else:
            print("Reversão cancelada.")
    else:
        executar_migracao()
