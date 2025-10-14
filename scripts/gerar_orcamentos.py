#!/usr/bin/env python3
"""
Script para gerar orçamentos para todas as demandas existentes no banco de dados.
Para cada item_demanda, cria orçamentos com pelo menos 2 itens de orçamento compatíveis.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

# Caminhos
DB_PATH = Path(__file__).parent.parent / "dados.db"

# Status possíveis
STATUS_ORCAMENTO = ["PENDENTE", "APROVADO", "REJEITADO"]
STATUS_ITEM = ["PENDENTE", "APROVADO", "REJEITADO"]


def get_fornecedores(cursor):
    """Busca todos os fornecedores"""
    cursor.execute("SELECT id FROM usuario WHERE perfil = 'FORNECEDOR'")
    return [row[0] for row in cursor.fetchall()]


def get_demandas(cursor):
    """Busca todas as demandas"""
    cursor.execute("SELECT id FROM demanda")
    return [row[0] for row in cursor.fetchall()]


def get_itens_demanda_by_demanda(cursor, id_demanda):
    """Busca todos os itens de uma demanda"""
    cursor.execute("""
        SELECT id, id_categoria, quantidade, preco_maximo
        FROM item_demanda
        WHERE id_demanda = ?
    """, (id_demanda,))
    return cursor.fetchall()


def get_itens_by_categoria(cursor, id_categoria):
    """Busca itens do catálogo por categoria"""
    cursor.execute("""
        SELECT id, nome, preco
        FROM item
        WHERE id_categoria = ?
    """, (id_categoria,))
    return cursor.fetchall()


def criar_orcamento(cursor, id_demanda, id_fornecedor):
    """Cria um orçamento"""
    data_cadastro = datetime.now() - timedelta(days=random.randint(0, 30))
    data_validade = data_cadastro + timedelta(days=30)
    status = random.choice(["PENDENTE", "PENDENTE", "APROVADO", "REJEITADO"])  # Mais chances de ser PENDENTE

    observacoes = None
    if status == "APROVADO":
        observacoes = "Orçamento aprovado pelo casal"
    elif status == "REJEITADO":
        observacoes = random.choice([
            "Valores acima do esperado",
            "Fornecedor não disponível nas datas",
            "Optamos por outro fornecedor"
        ])

    cursor.execute("""
        INSERT INTO orcamento (
            id_demanda, id_fornecedor_prestador, data_hora_cadastro,
            data_hora_validade, status, observacoes, valor_total
        ) VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (id_demanda, id_fornecedor, data_cadastro, data_validade, status, observacoes))

    return cursor.lastrowid, status


def criar_item_orcamento(cursor, id_orcamento, id_item_demanda, id_item, quantidade, preco_unitario, status_orcamento):
    """Cria um item de orçamento"""
    # Se o orçamento foi rejeitado, alguns itens podem ter motivo
    motivo_rejeicao = None
    status_item = status_orcamento

    if status_orcamento == "REJEITADO" and random.random() < 0.3:
        motivo_rejeicao = random.choice([
            "Preço muito alto",
            "Item não disponível",
            "Qualidade não atende expectativa"
        ])

    # Desconto aleatório (0-20%)
    desconto = round(random.uniform(0, 20), 2) if random.random() < 0.3 else 0

    cursor.execute("""
        INSERT INTO item_orcamento (
            id_orcamento, id_item_demanda, id_item, quantidade,
            preco_unitario, desconto, status, motivo_rejeicao, observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
    """, (id_orcamento, id_item_demanda, id_item, quantidade, preco_unitario, desconto, status_item, motivo_rejeicao))

    return cursor.lastrowid


def calcular_valor_total_orcamento(cursor, id_orcamento):
    """Calcula e atualiza o valor total do orçamento"""
    cursor.execute("""
        SELECT SUM((preco_unitario * quantidade) * (1 - desconto/100))
        FROM item_orcamento
        WHERE id_orcamento = ?
    """, (id_orcamento,))

    valor_total = cursor.fetchone()[0] or 0

    cursor.execute("""
        UPDATE orcamento
        SET valor_total = ?
        WHERE id = ?
    """, (valor_total, id_orcamento))

    return valor_total


def gerar_orcamentos_para_demanda(cursor, id_demanda, fornecedores):
    """Gera orçamentos para uma demanda"""
    # Buscar itens da demanda
    itens_demanda = get_itens_demanda_by_demanda(cursor, id_demanda)

    if not itens_demanda:
        print(f"⚠️  Demanda {id_demanda} não tem itens, pulando...")
        return 0, 0

    # Criar 1-3 orçamentos de fornecedores diferentes
    num_orcamentos = random.randint(1, min(3, len(fornecedores)))
    fornecedores_selecionados = random.sample(fornecedores, num_orcamentos)

    total_orcamentos = 0
    total_itens = 0

    for id_fornecedor in fornecedores_selecionados:
        # Criar orçamento
        id_orcamento, status_orcamento = criar_orcamento(cursor, id_demanda, id_fornecedor)
        total_orcamentos += 1

        # Para cada item da demanda, adicionar pelo menos 2 itens de orçamento
        for id_item_demanda, id_categoria, quantidade_demanda, preco_maximo in itens_demanda:
            # Buscar itens do catálogo dessa categoria
            itens_catalogo = get_itens_by_categoria(cursor, id_categoria)

            if not itens_catalogo:
                print(f"⚠️  Categoria {id_categoria} não tem itens no catálogo")
                continue

            # Selecionar pelo menos 2 itens (ou todos se houver menos de 2)
            num_itens = random.randint(2, min(3, len(itens_catalogo)))
            itens_selecionados = random.sample(itens_catalogo, min(num_itens, len(itens_catalogo)))

            for id_item, nome_item, preco_base in itens_selecionados:
                # Ajustar quantidade (pode variar um pouco da demanda)
                quantidade = quantidade_demanda
                if random.random() < 0.3:
                    quantidade = max(1, quantidade_demanda + random.randint(-1, 2))

                # Calcular preço unitário baseado no preço máximo da demanda
                # Variar entre 70% e 95% do preço máximo dividido pela quantidade
                if preco_maximo and quantidade_demanda > 0:
                    preco_base_calculado = preco_maximo / quantidade_demanda
                    fator = random.uniform(0.70, 0.95)
                    preco_unitario = round(preco_base_calculado * fator, 2)
                else:
                    # Usar preço base do item com variação
                    preco_unitario = round(preco_base * random.uniform(0.9, 1.1), 2)

                # Criar item de orçamento
                criar_item_orcamento(
                    cursor, id_orcamento, id_item_demanda,
                    id_item, quantidade, preco_unitario, status_orcamento
                )
                total_itens += 1

        # Calcular valor total do orçamento
        valor_total = calcular_valor_total_orcamento(cursor, id_orcamento)

    return total_orcamentos, total_itens


def main():
    """Executa a geração de orçamentos"""
    print(f"📊 Gerando orçamentos em {DB_PATH}\n")

    # Verificar se o banco existe
    if not DB_PATH.exists():
        print(f"❌ Erro: Banco de dados não encontrado em {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Limpar orçamentos existentes
        cursor.execute("DELETE FROM item_orcamento")
        cursor.execute("DELETE FROM orcamento")
        print("🗑️  Orçamentos existentes removidos\n")

        # Buscar fornecedores
        fornecedores = get_fornecedores(cursor)
        print(f"👥 Encontrados {len(fornecedores)} fornecedores")

        # Buscar demandas
        demandas = get_demandas(cursor)
        print(f"📋 Encontradas {len(demandas)} demandas\n")

        total_orcamentos = 0
        total_itens = 0

        # Gerar orçamentos para cada demanda
        for i, id_demanda in enumerate(demandas, 1):
            print(f"[{i}/{len(demandas)}] Processando demanda {id_demanda}...", end=" ")
            num_orc, num_itens = gerar_orcamentos_para_demanda(cursor, id_demanda, fornecedores)
            total_orcamentos += num_orc
            total_itens += num_itens
            print(f"✅ {num_orc} orçamentos, {num_itens} itens")

        # Commit das alterações
        conn.commit()

        print(f"\n🎉 Geração concluída!")
        print(f"   - {total_orcamentos} orçamentos criados")
        print(f"   - {total_itens} itens de orçamento criados")

        # Estatísticas
        cursor.execute("""
            SELECT status, COUNT(*)
            FROM orcamento
            GROUP BY status
        """)
        print(f"\n📊 Distribuição de orçamentos por status:")
        for status, count in cursor.fetchall():
            print(f"   - {status}: {count}")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Erro: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
