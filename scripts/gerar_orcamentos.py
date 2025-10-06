#!/usr/bin/env python3
"""
Script para gerar 2-4 orçamentos fictícios para cada demanda existente no banco
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Conectar ao banco
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Buscar todas as demandas
cursor.execute("""
    SELECT id, id_casal, id_categoria, titulo, orcamento_min, orcamento_max, status
    FROM demanda
    ORDER BY id
""")
demandas = cursor.fetchall()

# Buscar fornecedores disponíveis
cursor.execute("SELECT id FROM usuario WHERE perfil = 'FORNECEDOR'")
fornecedores = [row[0] for row in cursor.fetchall()]

if not fornecedores:
    print("❌ Nenhum fornecedor encontrado no banco!")
    conn.close()
    exit(1)

print(f"📦 {len(demandas)} demandas encontradas")
print(f"👤 {len(fornecedores)} fornecedores disponíveis")

# Observações possíveis para orçamentos
observacoes_templates = [
    "Orçamento válido por 30 dias. Inclui todos os materiais necessários.",
    "Valores já incluem impostos. Forma de pagamento: 50% entrada e 50% na entrega.",
    "Desconto de 10% para pagamento à vista.",
    "Parcelamento em até 3x sem juros no cartão de crédito.",
    "Incluímos garantia de 90 dias para o serviço prestado.",
    "Valores sujeitos a reajuste após visita técnica.",
    "Orçamento detalhado. Entre em contato para esclarecimentos.",
    "Disponibilidade confirmada para a data solicitada.",
    "Pacote promocional com desconto especial para casamentos.",
    "Experiência de 10+ anos no mercado de eventos.",
    None,
    None,  # Algumas sem observações
]

orcamentos_criados = []
total_por_status = {"PENDENTE": 0, "ACEITO": 0, "REJEITADO": 0}

# Gerar orçamentos para cada demanda
for demanda_id, id_casal, id_categoria, titulo, orc_min, orc_max, status_demanda in demandas:

    # Definir quantos orçamentos criar (2 a 4)
    num_orcamentos = random.randint(2, 4)

    # Selecionar fornecedores aleatórios (sem repetição para esta demanda)
    fornecedores_selecionados = random.sample(fornecedores, min(num_orcamentos, len(fornecedores)))

    # Determinar status dos orçamentos baseado no status da demanda
    if status_demanda == "FINALIZADA":
        # 1 aceito, resto pendente ou rejeitado
        status_orcamentos = ["ACEITO"] + random.choices(["PENDENTE", "REJEITADO"], k=num_orcamentos-1)
    elif status_demanda == "CANCELADA":
        # Apenas pendentes ou rejeitados
        status_orcamentos = random.choices(["PENDENTE", "REJEITADO"], k=num_orcamentos)
    else:  # ATIVA
        # Maioria pendente, alguns rejeitados
        status_orcamentos = random.choices(
            ["PENDENTE", "PENDENTE", "PENDENTE", "REJEITADO"],
            k=num_orcamentos
        )

    # Embaralhar para não ser sempre na mesma ordem
    random.shuffle(status_orcamentos)

    # Data base para orçamentos (entre 1 e 30 dias atrás)
    dias_atras = random.randint(1, 30)
    data_base = datetime.now() - timedelta(days=dias_atras)

    for i, fornecedor_id in enumerate(fornecedores_selecionados):
        # Calcular valor do orçamento dentro da faixa
        # Adicionar variação para tornar mais realista
        faixa = orc_max - orc_min
        valor_base = orc_min + (faixa * random.random())

        # Adicionar pequena variação adicional
        variacao = random.uniform(0.95, 1.05)
        valor_total = round(valor_base * variacao, 2)

        # Data de cadastro (variar um pouco entre orçamentos)
        data_cadastro = data_base + timedelta(hours=random.randint(0, 72))

        # Data de validade (15 a 30 dias após cadastro)
        dias_validade = random.randint(15, 30)
        data_validade = data_cadastro + timedelta(days=dias_validade)

        # Status do orçamento
        status_orc = status_orcamentos[i] if i < len(status_orcamentos) else "PENDENTE"

        # Observações
        obs = random.choice(observacoes_templates)

        # Se for aceito, adicionar observação especial
        if status_orc == "ACEITO":
            obs = "✅ Orçamento aceito pelo casal. Aguardando confirmação de pagamento."
        elif status_orc == "REJEITADO":
            motivos = [
                "Valor acima do orçamento disponível.",
                "Casal optou por outro fornecedor.",
                "Prazo de entrega incompatível.",
                "Serviço não atendeu às expectativas.",
            ]
            obs = random.choice(motivos)

        orcamentos_criados.append((
            demanda_id,
            fornecedor_id,
            data_cadastro.strftime('%Y-%m-%d %H:%M:%S'),
            data_validade.strftime('%Y-%m-%d %H:%M:%S'),
            status_orc,
            obs,
            valor_total
        ))

        total_por_status[status_orc] += 1

# Inserir orçamentos no banco
print(f"\n💾 Inserindo {len(orcamentos_criados)} orçamentos no banco...")

cursor.executemany('''
    INSERT INTO orcamento (
        id_demanda, id_fornecedor_prestador, data_hora_cadastro,
        data_hora_validade, status, observacoes, valor_total
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
''', orcamentos_criados)

conn.commit()

# Verificar inserção
cursor.execute("SELECT COUNT(*) FROM orcamento")
total_orcamentos = cursor.fetchone()[0]

print(f"✅ {total_orcamentos} orçamentos criados com sucesso!")

# Estatísticas
print("\n📊 Distribuição por status:")
for status, count in total_por_status.items():
    percentual = (count / total_orcamentos * 100) if total_orcamentos > 0 else 0
    print(f"  {status}: {count} ({percentual:.1f}%)")

# Média de orçamentos por demanda
cursor.execute("""
    SELECT
        COUNT(*) as total_orcamentos,
        COUNT(DISTINCT id_demanda) as total_demandas,
        ROUND(CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT id_demanda), 2) as media
    FROM orcamento
""")
total_orc, total_dem, media = cursor.fetchone()
print(f"\n📈 Média de orçamentos por demanda: {media}")

# Top 5 demandas com mais orçamentos
cursor.execute("""
    SELECT d.id, d.titulo, COUNT(o.id) as total_orcamentos
    FROM demanda d
    LEFT JOIN orcamento o ON d.id = o.id_demanda
    GROUP BY d.id
    ORDER BY total_orcamentos DESC
    LIMIT 5
""")
print("\n🏆 Top 5 demandas com mais orçamentos:")
for dem_id, titulo, count in cursor.fetchall():
    print(f"  #{dem_id} - {titulo[:50]}... ({count} orçamentos)")

# Demandas sem orçamentos (não deveria haver)
cursor.execute("""
    SELECT COUNT(*)
    FROM demanda d
    LEFT JOIN orcamento o ON d.id = o.id_demanda
    WHERE o.id IS NULL
""")
sem_orcamento = cursor.fetchone()[0]
if sem_orcamento > 0:
    print(f"\n⚠️  {sem_orcamento} demandas ainda sem orçamentos")
else:
    print(f"\n✅ Todas as demandas possuem orçamentos!")

conn.close()
print("\n✅ Script concluído!")
