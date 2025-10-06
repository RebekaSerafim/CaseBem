#!/usr/bin/env python3
"""
Script de migração para refatoração V2 do sistema de Demandas/Orçamentos.

MUDANÇAS:
- Tabela item_demanda: remover id_item, adicionar id, tipo, id_categoria, descricao
- Tabela demanda: remover id_categoria, titulo, orcamento_min/max, adicionar orcamento_total, data_casamento, cidade_casamento

IMPORTANTE: Execute um backup do banco antes de rodar este script!

Usage:
    python scripts/migrar_demanda_v2.py [--db-path PATH] [--dry-run]
"""

import sqlite3
import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

DEFAULT_DB_PATH = ROOT_DIR / "dados.db"
BACKUP_SUFFIX = f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def fazer_backup(db_path: Path) -> Path:
    """Cria backup do banco de dados"""
    backup_path = Path(str(db_path) + BACKUP_SUFFIX)
    print(f"📦 Criando backup: {backup_path}")

    import shutil
    shutil.copy2(db_path, backup_path)

    print(f"✅ Backup criado com sucesso!")
    return backup_path


def migrar_tabela_demanda(conn: sqlite3.Connection, dry_run: bool = False):
    """
    Migra tabela demanda para nova estrutura.

    Mudanças:
    - Remove: id_categoria, titulo, orcamento_min, orcamento_max
    - Adiciona: orcamento_total, data_casamento, cidade_casamento
    """
    print("\n🔄 Migrando tabela 'demanda'...")

    cursor = conn.cursor()

    # 1. Criar tabela temporária com nova estrutura
    print("  1️⃣ Criando tabela temporária...")
    cursor.execute("""
        CREATE TABLE demanda_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_casal INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            orcamento_total DECIMAL(10,2),
            data_casamento DATE,
            cidade_casamento VARCHAR(255),
            prazo_entrega VARCHAR(255),
            status VARCHAR(20) DEFAULT 'ATIVA',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observacoes TEXT,
            FOREIGN KEY (id_casal) REFERENCES casal(id)
        );
    """)

    # 2. Copiar dados da tabela antiga para nova
    print("  2️⃣ Copiando dados...")
    cursor.execute("""
        INSERT INTO demanda_new (
            id, id_casal, descricao, orcamento_total,
            data_casamento, cidade_casamento,
            prazo_entrega, status, data_criacao, observacoes
        )
        SELECT
            d.id,
            d.id_casal,
            COALESCE(d.descricao, d.titulo),  -- Usar descrição ou titulo como descrição
            CASE
                WHEN d.orcamento_min IS NOT NULL AND d.orcamento_max IS NOT NULL
                THEN (d.orcamento_min + d.orcamento_max) / 2.0
                WHEN d.orcamento_max IS NOT NULL THEN d.orcamento_max
                WHEN d.orcamento_min IS NOT NULL THEN d.orcamento_min
                ELSE NULL
            END as orcamento_total,
            c.data_casamento,
            c.local_previsto as cidade_casamento,
            d.prazo_entrega,
            d.status,
            d.data_criacao,
            d.observacoes
        FROM demanda d
        LEFT JOIN casal c ON d.id_casal = c.id;
    """)

    rows_migrated = cursor.rowcount
    print(f"  ✅ {rows_migrated} demandas migradas")

    if not dry_run:
        # 3. Dropar tabela antiga
        print("  3️⃣ Removendo tabela antiga...")
        cursor.execute("DROP TABLE demanda;")

        # 4. Renomear tabela nova
        print("  4️⃣ Renomeando tabela nova...")
        cursor.execute("ALTER TABLE demanda_new RENAME TO demanda;")

        conn.commit()
        print("  ✅ Migração de 'demanda' concluída!")
    else:
        print("  ⚠️ Dry-run: revertendo mudanças...")
        conn.rollback()


def migrar_tabela_item_demanda(conn: sqlite3.Connection, dry_run: bool = False):
    """
    Migra tabela item_demanda para nova estrutura.

    Mudanças:
    - Remove: chave composta (id_demanda, id_item)
    - Adiciona: id (PK auto-increment), tipo, id_categoria, descricao
    - Mantém: quantidade, preco_maximo, observacoes
    """
    print("\n🔄 Migrando tabela 'item_demanda'...")

    cursor = conn.cursor()

    # 1. Criar tabela temporária com nova estrutura
    print("  1️⃣ Criando tabela temporária...")
    cursor.execute("""
        CREATE TABLE item_demanda_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_demanda INTEGER NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            id_categoria INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 1,
            preco_maximo REAL,
            observacoes TEXT,
            FOREIGN KEY (id_demanda) REFERENCES demanda(id) ON DELETE CASCADE,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id)
        );
    """)

    # 2. Copiar dados convertidos
    print("  2️⃣ Copiando e convertendo dados...")
    cursor.execute("""
        INSERT INTO item_demanda_new (
            id_demanda, tipo, id_categoria, descricao,
            quantidade, preco_maximo, observacoes
        )
        SELECT
            id.id_demanda,
            i.tipo as tipo,
            i.id_categoria,
            i.nome || CASE
                WHEN i.descricao IS NOT NULL AND i.descricao != ''
                THEN ': ' || i.descricao
                ELSE ''
            END as descricao,
            id.quantidade,
            id.preco_maximo,
            CASE
                WHEN id.observacoes IS NOT NULL AND id.observacoes != ''
                THEN id.observacoes
                WHEN i.observacoes IS NOT NULL AND i.observacoes != ''
                THEN 'Item original: ' || i.observacoes
                ELSE NULL
            END as observacoes
        FROM item_demanda id
        JOIN item i ON id.id_item = i.id;
    """)

    rows_migrated = cursor.rowcount
    print(f"  ✅ {rows_migrated} itens de demanda migrados")

    if not dry_run:
        # 3. Dropar tabela antiga
        print("  3️⃣ Removendo tabela antiga...")
        cursor.execute("DROP TABLE item_demanda;")

        # 4. Renomear tabela nova
        print("  4️⃣ Renomeando tabela nova...")
        cursor.execute("ALTER TABLE item_demanda_new RENAME TO item_demanda;")

        conn.commit()
        print("  ✅ Migração de 'item_demanda' concluída!")
    else:
        print("  ⚠️ Dry-run: revertendo mudanças...")
        conn.rollback()


def validar_migracao(conn: sqlite3.Connection):
    """Valida se a migração foi bem-sucedida"""
    print("\n🔍 Validando migração...")

    cursor = conn.cursor()

    # Verificar estrutura da tabela demanda
    cursor.execute("PRAGMA table_info(demanda);")
    colunas_demanda = {row[1] for row in cursor.fetchall()}
    colunas_esperadas_demanda = {
        "id", "id_casal", "descricao", "orcamento_total",
        "data_casamento", "cidade_casamento", "prazo_entrega",
        "status", "data_criacao", "observacoes"
    }

    if colunas_esperadas_demanda == colunas_demanda:
        print("  ✅ Estrutura da tabela 'demanda' está correta")
    else:
        print(f"  ❌ Estrutura da tabela 'demanda' incorreta!")
        print(f"     Esperado: {colunas_esperadas_demanda}")
        print(f"     Encontrado: {colunas_demanda}")
        return False

    # Verificar estrutura da tabela item_demanda
    cursor.execute("PRAGMA table_info(item_demanda);")
    colunas_item_demanda = {row[1] for row in cursor.fetchall()}
    colunas_esperadas_item_demanda = {
        "id", "id_demanda", "tipo", "id_categoria", "descricao",
        "quantidade", "preco_maximo", "observacoes"
    }

    if colunas_esperadas_item_demanda == colunas_item_demanda:
        print("  ✅ Estrutura da tabela 'item_demanda' está correta")
    else:
        print(f"  ❌ Estrutura da tabela 'item_demanda' incorreta!")
        print(f"     Esperado: {colunas_esperadas_item_demanda}")
        print(f"     Encontrado: {colunas_item_demanda}")
        return False

    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM demanda;")
    total_demandas = cursor.fetchone()[0]
    print(f"  📊 Total de demandas: {total_demandas}")

    cursor.execute("SELECT COUNT(*) FROM item_demanda;")
    total_itens = cursor.fetchone()[0]
    print(f"  📊 Total de itens de demanda: {total_itens}")

    print("\n✅ Validação concluída com sucesso!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Migração V2 do sistema de Demandas")
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH,
                        help="Caminho para o banco de dados SQLite")
    parser.add_argument("--dry-run", action="store_true",
                        help="Executa sem fazer mudanças permanentes")
    parser.add_argument("--skip-backup", action="store_true",
                        help="Pula criação de backup (NÃO RECOMENDADO)")

    args = parser.parse_args()

    print("=" * 70)
    print("🔧 MIGRAÇÃO V2: Sistema de Demandas/Orçamentos")
    print("=" * 70)

    if not args.db_path.exists():
        print(f"\n❌ Erro: Banco de dados não encontrado: {args.db_path}")
        sys.exit(1)

    # Criar backup
    if not args.skip_backup and not args.dry_run:
        fazer_backup(args.db_path)

    if args.dry_run:
        print("\n⚠️ MODO DRY-RUN: Nenhuma mudança permanente será feita\n")

    # Conectar ao banco
    conn = sqlite3.connect(args.db_path)
    conn.row_factory = sqlite3.Row

    try:
        # Executar migrações
        migrar_tabela_item_demanda(conn, dry_run=args.dry_run)
        migrar_tabela_demanda(conn, dry_run=args.dry_run)

        # Validar apenas se não for dry-run
        if not args.dry_run:
            if validar_migracao(conn):
                print("\n" + "=" * 70)
                print("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
                print("=" * 70)
            else:
                print("\n" + "=" * 70)
                print("❌ MIGRAÇÃO FALHOU NA VALIDAÇÃO!")
                print("=" * 70)
                sys.exit(1)
        else:
            print("\n" + "=" * 70)
            print("ℹ️ DRY-RUN CONCLUÍDO (nada foi alterado)")
            print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
