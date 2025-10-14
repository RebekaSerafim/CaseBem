#!/usr/bin/env python3
"""
Script para inserir demandas de teste no banco de dados.
Cria 3 demandas para cada casal, com pelo menos 7 itens cada.
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Conexão com o banco de dados
DB_PATH = '/Volumes/Externo/Ifes/CaseBem/dados.db'

# Templates de demandas (variadas e realistas)
TEMPLATES_DEMANDA = [
    {
        "descricao": "Pacote Completo para Casamento",
        "orcamento_range": (45000, 85000),
        "prazo_dias": 30,
        "observacoes": "Buscamos fornecedores para todos os serviços principais do casamento. Qualidade e pontualidade são essenciais.",
        "itens": [
            ("ESPAÇO", 18, "Espaço para cerimônia religiosa com capacidade para {} convidados", lambda: random.randint(80, 150), (3000, 8000), "Preferência por locais com boa iluminação natural"),
            ("ESPAÇO", 19, "Espaço para recepção com área coberta e ao ar livre", lambda: random.randint(100, 200), (8000, 18000), "Necessário estrutura para dança e buffet"),
            ("SERVIÇO", 1, "Fotografia profissional com álbum premium de {} páginas", lambda: random.randint(40, 80), (2500, 6000), "Preferência por fotógrafo com portfólio em casamentos ao ar livre"),
            ("SERVIÇO", 3, "Buffet completo (entrada, prato principal, sobremesa) para {} pessoas", lambda: random.randint(100, 200), (8000, 15000), "Cardápio variado com opções vegetarianas"),
            ("SERVIÇO", 8, "Decoração floral e ambientação completa", lambda: 1, (4000, 9000), "Cores predominantes: branco, verde e dourado"),
            ("PRODUTO", 14, "Bolo de casamento {} andares com decoração personalizada", lambda: random.randint(3, 5), (800, 2000), "Sabores: chocolate e frutas vermelhas"),
            ("PRODUTO", 13, "Convites personalizados para {} convidados", lambda: random.randint(150, 250), (600, 1500), "Design elegante com acabamento em relevo"),
            ("SERVIÇO", 2, "DJ profissional com equipamento de som e iluminação", lambda: 1, (1800, 4000), "Playlist variada incluindo músicas românticas e animadas"),
        ]
    },
    {
        "descricao": "Decoração e Ambientação Premium",
        "orcamento_range": (18000, 35000),
        "prazo_dias": 45,
        "observacoes": "Foco em criar um ambiente sofisticado e acolhedor. Buscamos fornecedores criativos e detalhistas.",
        "itens": [
            ("SERVIÇO", 8, "Projeto completo de decoração temática", lambda: 1, (5000, 12000), "Tema: jardim encantado com elementos rústicos"),
            ("PRODUTO", 15, "Arranjos florais variados: {} buquês e {} centros de mesa", lambda: random.randint(8, 15), (2500, 5500), "Flores: rosas, lírios e folhagens"),
            ("PRODUTO", 16, "Locação de mobiliário: {} cadeiras, {} mesas e lounge", lambda: random.randint(120, 180), (2000, 4500), "Estilo rústico-chique com madeira e tecidos claros"),
            ("SERVIÇO", 2, "Iluminação cênica e decorativa", lambda: 1, (1500, 3500), "Luzes de LED, velas e spots direcionados"),
            ("PRODUTO", 13, "Papelaria personalizada: {} placas, menus e tags", lambda: random.randint(30, 60), (400, 900), "Design coordenado com o tema da decoração"),
            ("SERVIÇO", 4, "Assessoria de cerimonial para coordenação do evento", lambda: 1, (2000, 4500), "Acompanhamento desde o ensaio até o final da festa"),
            ("PRODUTO", 17, "Bebidas premium: {} garrafas de vinho e espumante", lambda: random.randint(40, 80), (1200, 3000), "Vinhos nacionais e importados selecionados"),
            ("PRODUTO", 14, "Mesa de doces finos com {} tipos de docinhos (100 unidades cada)", lambda: random.randint(8, 12), (1000, 2500), "Variedade de sabores e decoração refinada"),
        ]
    },
    {
        "descricao": "Serviços Essenciais e Apoio",
        "orcamento_range": (22000, 42000),
        "prazo_dias": 60,
        "observacoes": "Buscamos profissionais experientes para garantir que tudo saia perfeito no grande dia.",
        "itens": [
            ("SERVIÇO", 5, "Celebrante para cerimônia personalizada", lambda: 1, (1200, 2800), "Cerimônia laica com textos personalizados"),
            ("SERVIÇO", 6, "Equipe de beleza: {} profissionais (maquiagem, penteado, manicure)", lambda: random.randint(4, 8), (1500, 3500), "Preparação da noiva, madrinhas e mães"),
            ("SERVIÇO", 7, "Transporte: {} veículos de luxo", lambda: random.randint(3, 6), (1800, 4000), "Para noivos, padrinhos e familiares"),
            ("SERVIÇO", 1, "Filmagem profissional com edição de vídeo", lambda: 1, (3500, 7500), "Entrega de vídeo editado e making of"),
            ("SERVIÇO", 9, "Equipe de segurança discreta para o evento", lambda: random.randint(4, 8), (1200, 2500), "Profissionais uniformizados e experientes"),
            ("PRODUTO", 11, "Vestido de noiva sob medida com ajustes", lambda: 1, (5000, 12000), "Tecido nobre com bordados e cauda média"),
            ("PRODUTO", 12, "Par de alianças em ouro {} com gravação personalizada", lambda: lambda: f"{random.choice(['18k', '24k'])}", (2500, 6000), "Design clássico com acabamento polido"),
            ("ESPAÇO", 20, "Hospedagem para {} convidados em hotel próximo", lambda: random.randint(20, 40), (3000, 8000), "Acomodação para convidados de fora da cidade"),
        ]
    }
]

def get_casal_info(cursor, id_casal):
    """Busca informações do casal no banco de dados"""
    cursor.execute("""
        SELECT data_casamento, local_previsto
        FROM casal
        WHERE id = ?
    """, (id_casal,))
    return cursor.fetchone()

def calcular_prazo(data_casamento_str, dias_antes):
    """Calcula a data de prazo de entrega baseada na data do casamento"""
    if not data_casamento_str:
        return None
    try:
        data_casamento = datetime.strptime(data_casamento_str, '%Y-%m-%d')
        prazo = data_casamento - timedelta(days=dias_antes)
        return prazo.strftime('%Y-%m-%d')
    except:
        return None

def inserir_demanda(cursor, id_casal, template):
    """Insere uma demanda no banco de dados"""
    casal_info = get_casal_info(cursor, id_casal)
    if not casal_info:
        return None

    data_casamento, local_previsto = casal_info
    cidade_casamento = local_previsto.split(' - ')[-1] if local_previsto else "Não especificado"

    # Definir valores da demanda
    orcamento_total = random.uniform(*template["orcamento_range"])
    prazo_entrega = calcular_prazo(data_casamento, template["prazo_dias"])

    cursor.execute("""
        INSERT INTO demanda (
            id_casal, descricao, orcamento_total, data_casamento,
            cidade_casamento, prazo_entrega, status, data_criacao, observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_casal,
        template["descricao"],
        round(orcamento_total, 2),
        data_casamento,
        cidade_casamento,
        prazo_entrega,
        "ATIVA",
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        template["observacoes"]
    ))

    return cursor.lastrowid

def inserir_item_demanda(cursor, id_demanda, tipo, id_categoria, descricao_template, quantidade_func, preco_range, observacoes):
    """Insere um item de demanda no banco de dados"""
    # Processar quantidade
    quantidade_valor = quantidade_func() if callable(quantidade_func) else quantidade_func

    # Contar número de placeholders na descrição
    num_placeholders = descricao_template.count('{}')

    # Processar descrição com formatação
    if callable(quantidade_valor):
        # Para casos especiais como "ouro 18k" (retorna string)
        valor_str = quantidade_valor()
        descricao = descricao_template.format(valor_str)
        quantidade_final = 1
    elif num_placeholders == 0:
        # Sem placeholders
        descricao = descricao_template
        quantidade_final = quantidade_valor
    elif num_placeholders == 1:
        # Um placeholder simples
        descricao = descricao_template.format(quantidade_valor)
        quantidade_final = quantidade_valor
    elif num_placeholders == 2:
        # Dois placeholders (ex: "X buquês e Y centros", "X cadeiras, Y mesas")
        val1 = quantidade_valor
        val2 = random.randint(20, 40)
        descricao = descricao_template.format(val1, val2)
        quantidade_final = val1
    else:
        # Fallback para casos não previstos
        descricao = descricao_template
        quantidade_final = quantidade_valor

    preco_maximo = random.uniform(*preco_range)

    cursor.execute("""
        INSERT INTO item_demanda (
            id_demanda, tipo, id_categoria, descricao,
            quantidade, preco_maximo, observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        id_demanda,
        tipo,
        id_categoria,
        descricao,
        quantidade_final,
        round(preco_maximo, 2),
        observacoes
    ))

    return cursor.lastrowid

def main():
    """Função principal"""
    print("=== Iniciando inserção de demandas ===\n")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Buscar todos os casais
        cursor.execute("SELECT id FROM casal ORDER BY id")
        casais = cursor.fetchall()

        total_demandas = 0
        total_itens = 0

        for (id_casal,) in casais:
            print(f"Processando Casal ID {id_casal}...")

            # Criar 3 demandas para cada casal
            for i, template in enumerate(TEMPLATES_DEMANDA, 1):
                # Inserir demanda
                id_demanda = inserir_demanda(cursor, id_casal, template)
                if not id_demanda:
                    print(f"  ⚠️  Erro ao criar demanda {i} para casal {id_casal}")
                    continue

                total_demandas += 1

                # Inserir itens da demanda
                itens_inseridos = 0
                for item in template["itens"]:
                    tipo, id_categoria, descricao, quantidade_func, preco_range, observacoes = item
                    inserir_item_demanda(
                        cursor, id_demanda, tipo, id_categoria,
                        descricao, quantidade_func, preco_range, observacoes
                    )
                    itens_inseridos += 1
                    total_itens += 1

                print(f"  ✓ Demanda {i} criada: {template['descricao']} ({itens_inseridos} itens)")

        # Commit das alterações
        conn.commit()

        print(f"\n=== Conclusão ===")
        print(f"✓ {len(casais)} casais processados")
        print(f"✓ {total_demandas} demandas criadas")
        print(f"✓ {total_itens} itens de demanda inseridos")
        print(f"✓ Média de {total_itens/total_demandas:.1f} itens por demanda")

    except Exception as e:
        conn.rollback()
        print(f"\n✗ Erro durante a execução: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
