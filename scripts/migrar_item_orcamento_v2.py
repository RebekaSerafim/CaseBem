#!/usr/bin/env python3
"""
Script de Migração: item_orcamento V2

Adiciona vínculo entre item_orcamento e item_demanda.

MUDANÇAS:
- Adiciona campo id_item_demanda em item_orcamento
- Muda chave primária de (id_orcamento, id_item) para id auto-increment
- Adiciona constraint único para (id_orcamento, id_item_demanda, id_item)

IMPORTANTE: Este script remove todos os dados existentes de item_orcamento
pois não há como inferir o id_item_demanda dos dados antigos.
"""

import sqlite3
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Caminho do banco de dados
DB_PATH = project_root / "dados.db"


def executar_migracao():
    """Executa a migração do banco de dados"""

    print("=" * 70)
    print("🔄 MIGRAÇÃO: item_orcamento V2 - Adicionar vínculo com item_demanda")
    print("=" * 70)
    print()

    if not DB_PATH.exists():
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return False

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # 1. Verificar se a migração já foi aplicada
        print("1️⃣ Verificando se migração já foi aplicada...")
        cursor.execute("PRAGMA table_info(item_orcamento)")
        colunas = {col[1] for col in cursor.fetchall()}

        if 'id_item_demanda' in colunas:
            print("   ✅ Migração já aplicada anteriormente!")
            print()
            return True

        # 2. Contar registros que serão perdidos
        print("2️⃣ Verificando dados existentes...")
        cursor.execute("SELECT COUNT(*) FROM item_orcamento")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"   ⚠️  ATENÇÃO: {count} registro(s) existente(s) será(ão) REMOVIDO(S)!")
            print("   (Não é possível migrar dados sem id_item_demanda)")
            resposta = input("   Continuar? (sim/não): ")
            if resposta.lower() not in ['sim', 's', 'yes', 'y']:
                print("   ❌ Migração cancelada pelo usuário")
                return False
        else:
            print("   ✅ Nenhum dado existente")

        print()

        # 3. Fazer backup da estrutura antiga
        print("3️⃣ Criando backup da tabela antiga...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_orcamento_backup_v1 AS
            SELECT * FROM item_orcamento
        """)
        print("   ✅ Backup criado: item_orcamento_backup_v1")
        print()

        # 4. Remover tabela antiga
        print("4️⃣ Removendo tabela antiga...")
        cursor.execute("DROP TABLE item_orcamento")
        print("   ✅ Tabela antiga removida")
        print()

        # 5. Criar nova estrutura
        print("5️⃣ Criando nova estrutura...")
        cursor.execute("""
            CREATE TABLE item_orcamento (
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
            );
        """)
        print("   ✅ Nova tabela criada com:")
        print("      - id (PK auto-increment)")
        print("      - id_item_demanda (NOVO campo)")
        print("      - Foreign keys para orcamento, item_demanda e item")
        print("      - Constraint UNIQUE (id_orcamento, id_item_demanda, id_item)")
        print()

        # 6. Criar índices para performance
        print("6️⃣ Criando índices...")
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
        print("   ✅ Índices criados")
        print()

        # 7. Commit das mudanças
        conn.commit()

        print("=" * 70)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print()
        print("Próximos passos:")
        print("1. Atualizar models e repositórios")
        print("2. Atualizar templates e rotas")
        print("3. Rodar testes")
        print()

        return True

    except Exception as e:
        conn.rollback()
        print()
        print("=" * 70)
        print("❌ ERRO NA MIGRAÇÃO!")
        print("=" * 70)
        print(f"Erro: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    sucesso = executar_migracao()
    sys.exit(0 if sucesso else 1)
