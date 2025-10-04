#!/usr/bin/env python3
"""
Script para popular banco de dados com dados de seed para testes E2E

Este script adiciona:
- Demandas realísticas criadas por casais existentes
- Orçamentos propostos por fornecedores para essas demandas
- Itens do fornecedor teste E2E (id 999)
"""
import json
import sqlite3
from pathlib import Path
import sys

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

DB_PATH = ROOT_DIR / "dados.db"
SEEDS_DIR = ROOT_DIR / "data" / "seeds"

def carregar_json(filename):
    """Carrega arquivo JSON de seeds"""
    filepath = SEEDS_DIR / filename
    if not filepath.exists():
        print(f"⚠️  Arquivo {filename} não encontrado")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def criar_demandas_seed(conn):
    """Insere demandas de seed no banco"""
    print("\n📝 Carregando demandas...")

    demandas = carregar_json("demandas.json")
    if not demandas:
        return

    cursor = conn.cursor()

    # Verificar quantas demandas já existem
    cursor.execute("SELECT COUNT(*) FROM demanda")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"   ℹ️  Já existem {count} demandas no banco - pulando")
        return

    inseridas = 0
    for demanda in demandas:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO demanda (
                    id, id_casal, id_categoria, titulo, descricao,
                    orcamento_min, orcamento_max, prazo_entrega,
                    status, data_criacao, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                demanda['id'],
                demanda['id_casal'],
                demanda['id_categoria'],
                demanda['titulo'],
                demanda['descricao'],
                demanda['orcamento_min'],
                demanda['orcamento_max'],
                demanda['prazo_entrega'],
                demanda['status'],
                demanda['data_criacao'],
                demanda.get('observacoes')
            ))

            if cursor.rowcount > 0:
                inseridas += 1

        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Demanda ID {demanda['id']} já existe ou erro: {e}")

    conn.commit()
    print(f"   ✅ {inseridas} demandas inseridas com sucesso!")

def criar_orcamentos_seed(conn):
    """Insere orçamentos de seed no banco"""
    print("\n💰 Carregando orçamentos...")

    orcamentos = carregar_json("orcamentos.json")
    if not orcamentos:
        return

    cursor = conn.cursor()

    # Verificar quantos orçamentos já existem
    cursor.execute("SELECT COUNT(*) FROM orcamento")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"   ℹ️  Já existem {count} orçamentos no banco - pulando")
        return

    inseridos = 0
    for orc in orcamentos:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO orcamento (
                    id, id_demanda, id_fornecedor_prestador,
                    data_hora_cadastro, data_hora_validade,
                    status, observacoes, valor_total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                orc['id'],
                orc['id_demanda'],
                orc['id_fornecedor_prestador'],
                orc['data_hora_cadastro'],
                orc.get('data_hora_validade'),
                orc['status'],
                orc.get('observacoes'),
                orc['valor_total']
            ))

            if cursor.rowcount > 0:
                inseridos += 1

        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Orçamento ID {orc['id']} já existe ou erro: {e}")

    conn.commit()
    print(f"   ✅ {inseridos} orçamentos inseridos com sucesso!")

def criar_itens_fornecedor_teste(conn):
    """Insere itens do fornecedor teste E2E no banco"""
    print("\n🛍️  Carregando itens do fornecedor teste E2E...")

    data = carregar_json("itens_fornecedor_teste.json")
    if not data or 'itens' not in data:
        return

    cursor = conn.cursor()

    # Verificar se fornecedor teste existe
    cursor.execute("SELECT id FROM usuario WHERE id = 999 AND perfil = 'FORNECEDOR'")
    if not cursor.fetchone():
        print("   ⚠️  Fornecedor teste (id 999) não encontrado!")
        print("   Execute os testes E2E primeiro para criar o fornecedor teste")
        return

    inseridos = 0
    atualizados = 0

    for item in data['itens']:
        try:
            # Verificar se item já existe
            cursor.execute("SELECT id FROM item WHERE id = ?", (item['id'],))
            existe = cursor.fetchone()

            if existe:
                # Atualizar item existente
                cursor.execute("""
                    UPDATE item SET
                        id_fornecedor = ?,
                        id_categoria = ?,
                        nome = ?,
                        tipo = ?,
                        preco = ?,
                        descricao = ?,
                        ativo = ?
                    WHERE id = ?
                """, (
                    item['id_fornecedor'],
                    item['id_categoria'],
                    item['nome'],
                    item['tipo'],
                    item['preco'],
                    item['descricao'],
                    1 if item['ativo'] else 0,
                    item['id']
                ))
                atualizados += 1
            else:
                # Inserir novo item
                cursor.execute("""
                    INSERT INTO item (
                        id, id_fornecedor, id_categoria, nome, tipo,
                        preco, descricao, ativo, data_cadastro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item['id'],
                    item['id_fornecedor'],
                    item['id_categoria'],
                    item['nome'],
                    item['tipo'],
                    item['preco'],
                    item['descricao'],
                    1 if item['ativo'] else 0,
                    item['data_cadastro']
                ))
                inseridos += 1

        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Item ID {item['id']} erro: {e}")

    conn.commit()
    print(f"   ✅ {inseridos} itens inseridos, {atualizados} atualizados!")

def criar_itens_publicos(conn):
    """Insere itens públicos de diversos fornecedores no banco"""
    print("\n🛍️  Carregando itens públicos...")

    data = carregar_json("itens_publicos.json")
    if not data or 'itens' not in data:
        return

    cursor = conn.cursor()

    inseridos = 0
    atualizados = 0

    for item in data['itens']:
        try:
            # Verificar se item já existe
            cursor.execute("SELECT id FROM item WHERE id = ?", (item['id'],))
            existe = cursor.fetchone()

            if existe:
                # Atualizar item existente
                cursor.execute("""
                    UPDATE item SET
                        id_fornecedor = ?,
                        id_categoria = ?,
                        nome = ?,
                        tipo = ?,
                        preco = ?,
                        descricao = ?,
                        ativo = ?
                    WHERE id = ?
                """, (
                    item['id_fornecedor'],
                    item['id_categoria'],
                    item['nome'],
                    item['tipo'],
                    item['preco'],
                    item['descricao'],
                    1 if item['ativo'] else 0,
                    item['id']
                ))
                atualizados += 1
            else:
                # Inserir novo item
                cursor.execute("""
                    INSERT INTO item (
                        id, id_fornecedor, id_categoria, nome, tipo,
                        preco, descricao, ativo, data_cadastro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item['id'],
                    item['id_fornecedor'],
                    item['id_categoria'],
                    item['nome'],
                    item['tipo'],
                    item['preco'],
                    item['descricao'],
                    1 if item['ativo'] else 0,
                    item['data_cadastro']
                ))
                inseridos += 1

        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Item ID {item['id']} erro: {e}")

    conn.commit()
    print(f"   ✅ {inseridos} itens públicos inseridos, {atualizados} atualizados!")

def criar_orcamentos_noivo(conn):
    """Insere orçamentos para o casal teste (noivo) no banco"""
    print("\n💰 Carregando orçamentos do noivo...")

    orcamentos = carregar_json("orcamentos_noivo.json")
    if not orcamentos:
        return

    cursor = conn.cursor()

    # Verificar quantos orçamentos já existem para demandas do casal 1
    cursor.execute("""
        SELECT COUNT(*) FROM orcamento o
        JOIN demanda d ON o.id_demanda = d.id
        WHERE d.id_casal = 1
    """)
    count = cursor.fetchone()[0]

    inseridos = 0
    for orc in orcamentos:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO orcamento (
                    id, id_demanda, id_fornecedor_prestador,
                    data_hora_cadastro, data_hora_validade,
                    status, observacoes, valor_total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                orc['id'],
                orc['id_demanda'],
                orc['id_fornecedor_prestador'],
                orc['data_hora_cadastro'],
                orc.get('data_hora_validade'),
                orc['status'],
                orc.get('observacoes'),
                orc['valor_total']
            ))

            if cursor.rowcount > 0:
                inseridos += 1

        except sqlite3.IntegrityError as e:
            print(f"   ⚠️  Orçamento ID {orc['id']} já existe ou erro: {e}")

    conn.commit()
    print(f"   ✅ {inseridos} orçamentos do noivo inseridos! (Total: {count + inseridos})")

def main():
    """Função principal"""
    print("=" * 60)
    print("🌱 SEED DE DADOS PARA TESTES E2E")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"\n❌ Banco de dados não encontrado: {DB_PATH}")
        print("   Execute a aplicação primeiro para criar o banco.")
        return 1

    try:
        # Conectar ao banco
        conn = sqlite3.connect(DB_PATH)
        print(f"\n✅ Conectado ao banco: {DB_PATH}")

        # Carregar dados
        criar_demandas_seed(conn)
        criar_orcamentos_seed(conn)
        criar_orcamentos_noivo(conn)
        criar_itens_fornecedor_teste(conn)
        criar_itens_publicos(conn)

        conn.close()

        print("\n" + "=" * 60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Dados adicionados:")
        print("   • Demandas realísticas de casais")
        print("   • Orçamentos propostos por fornecedores")
        print("   • Orçamentos para o casal teste (noivo)")
        print("   • Itens do fornecedor teste E2E (id 999)")
        print("   • Itens públicos de diversos fornecedores (20 itens)")
        print("\n💡 Os testes E2E agora têm dados completos para executar!")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Erro ao executar seed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
