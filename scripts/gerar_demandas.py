#!/usr/bin/env python3
"""
Script para gerar 60 demandas distintas no banco de dados
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Conectar ao banco
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Templates de demandas por categoria
demandas_templates = {
    1: [  # Fotografia e Filmagem
        ("Fotógrafo profissional para cerimônia", "Procuro fotógrafo experiente para cobrir cerimônia religiosa, making of e festa. Necessário portfolio."),
        ("Filmagem aérea com drone", "Buscamos profissional com drone para filmagem aérea do local e momentos especiais."),
        ("Ensaio pré-wedding", "Queremos ensaio fotográfico pré-casamento em local externo, preferencialmente praia ou campo."),
        ("Álbum de casamento premium", "Procuro serviço completo: fotos, edição e álbum premium com capa personalizada."),
        ("Book dos noivos", "Buscamos fotógrafo para fazer book dos noivos em estúdio e locação externa."),
        ("Fotografia making of", "Preciso de fotógrafo para registrar preparação dos noivos antes da cerimônia."),
    ],
    2: [  # Música e Som
        ("DJ para festa de casamento", "Procuro DJ experiente em festas de casamento, com equipamento próprio e repertório variado."),
        ("Banda ao vivo para recepção", "Buscamos banda com repertório MPB e samba para animar a festa."),
        ("Violinista para cerimônia", "Queremos violinista para tocar durante entrada da noiva e assinatura."),
        ("Coral para cerimônia religiosa", "Procuramos coral ou grupo vocal para cerimônia na igreja."),
        ("Saxofonista para coquetel", "Buscamos saxofonista para tocar durante coquetel de boas-vindas."),
    ],
    3: [  # Buffet e Catering
        ("Buffet completo para 150 pessoas", "Procuro buffet com opções variadas (carnes, massas, saladas) para 150 convidados."),
        ("Menu vegetariano e vegano", "Buscamos buffet que ofereça opções vegetarianas e veganas de qualidade."),
        ("Estação de drinks personalizados", "Queremos bar com drinks autorais e personalizados para o casamento."),
        ("Churrasco gourmet", "Procuramos serviço de churrasco gourmet com carnes nobres para recepção."),
        ("Jantar servido à francesa", "Buscamos buffet para jantar servido, estilo francês, menu degustação."),
    ],
    4: [  # Cerimonial e Assessoria
        ("Assessoria completa dia do casamento", "Preciso de cerimonialista experiente para coordenar todo o dia do evento."),
        ("Planejamento de casamento", "Buscamos wedding planner para ajudar no planejamento completo do casamento."),
        ("Organização de timeline", "Preciso de profissional para criar timeline detalhado e coordenar fornecedores."),
        ("Day coordinator", "Procuro coordenador apenas para o dia do casamento, supervisionar montagem e execução."),
    ],
    5: [  # Celebrante
        ("Celebrante para cerimônia ao ar livre", "Procuro celebrante para cerimônia simbólica ao ar livre, com roteiro personalizado."),
        ("Padre para casamento religioso", "Buscamos padre para cerimônia católica na igreja."),
        ("Pastor para cerimônia evangélica", "Precisamos de pastor para celebrar casamento evangélico."),
    ],
    6: [  # Beleza e Estética
        ("Maquiagem e penteado para noiva", "Procuro maquiador(a) e cabeleireiro(a) para dia do casamento, com teste prévio."),
        ("Spa day pré-casamento", "Queremos pacote spa para noivos e madrinhas no dia anterior ao casamento."),
        ("Manicure e pedicure", "Buscamos profissional para fazer unhas da noiva e madrinhas no dia."),
        ("Barbearia para noivo e padrinhos", "Procuro serviço de barbearia para noivo e padrinhos no dia do casamento."),
    ],
    7: [  # Transporte
        ("Carro clássico para noiva", "Procuro carro antigo/clássico para transporte da noiva até cerimônia."),
        ("Ônibus para convidados", "Buscamos ônibus para transportar convidados do hotel até local da festa."),
        ("Limusine para os noivos", "Queremos limusine para transporte dos noivos entre cerimônia e recepção."),
        ("Carros para padrinhos", "Precisamos de 3 carros executivos para transporte de padrinhos."),
    ],
    8: [  # Decoração e Ambientação
        ("Decoração rústica completa", "Procuro decoração estilo rústico-chique para cerimônia e recepção."),
        ("Arranjos de mesa", "Buscamos arranjos florais para 20 mesas da recepção."),
        ("Iluminação especial", "Queremos iluminação cênica para destacar mesa dos noivos e pista de dança."),
        ("Decoração clean e minimalista", "Procuramos decoração clean, minimalista, tons neutros."),
        ("Arco de flores para cerimônia", "Buscamos arco floral grande para altar da cerimônia."),
    ],
    9: [  # Segurança
        ("Segurança para evento", "Procuro equipe de segurança para controle de acesso e tranquilidade dos convidados."),
        ("Segurança particular VIP", "Buscamos seguranças discretos para familiares e convidados VIP."),
    ],
    10: [  # Limpeza
        ("Limpeza pós-evento", "Preciso de equipe de limpeza para após o término da festa."),
        ("Limpeza durante evento", "Buscamos equipe para manter banheiros e áreas comuns limpas durante festa."),
    ],
    11: [  # Vestidos e Roupas
        ("Vestido de noiva sob medida", "Procuro ateliê para confeccionar vestido de noiva personalizado."),
        ("Aluguel de smoking para noivo", "Buscamos loja para aluguel de smoking completo para o noivo."),
        ("Vestidos para madrinhas", "Precisamos de 6 vestidos iguais para madrinhas, tom lilás."),
        ("Terno sob medida", "Procuro alfaiate para fazer terno sob medida para o noivo."),
    ],
    12: [  # Alianças e Joias
        ("Alianças de ouro com diamantes", "Procuro joalheria para alianças personalizadas em ouro com incrustação de diamantes."),
        ("Semi-jóias para madrinhas", "Buscamos conjunto de brincos e colar para 6 madrinhas."),
        ("Aliança de namoro", "Queremos trocar alianças de namoro por aliança de noivado."),
    ],
    13: [  # Convites e Papelaria
        ("Convites impressos personalizados", "Procuro 150 convites impressos com design personalizado e acabamento especial."),
        ("Save the date digital", "Buscamos designer para criar save the date digital animado."),
        ("Papelaria completa", "Precisamos de convites, cardápios, tags, placas e sinalizações personalizadas."),
        ("Menu individual para mesas", "Queremos menus individuais impressos para cada lugar na mesa."),
    ],
    14: [  # Bolos e Doces
        ("Bolo de casamento 4 andares", "Procuro confeitaria para bolo de 4 andares, massa e recheio personalizados."),
        ("Mesa de doces finos", "Buscamos 500 doces finos variados para mesa de doces."),
        ("Cupcakes personalizados", "Queremos 100 cupcakes decorados no tema do casamento."),
        ("Bem casados para lembrancinha", "Precisamos de 150 bem casados embalados para dar de lembrança."),
    ],
    15: [  # Flores e Arranjos
        ("Buquê de noiva", "Procuro buquê de noiva com rosas brancas e folhagens."),
        ("Flores para igreja", "Buscamos decoração floral completa para igreja (altar, bancos, entrada)."),
        ("Arranjos de centro de mesa", "Precisamos de 20 arranjos baixos para centro de mesa da recepção."),
        ("Corsages para família", "Queremos corsages de lapela para pais e avós."),
    ],
    16: [  # Móveis e Utensílios
        ("Locação de mesas e cadeiras", "Preciso de 20 mesas redondas e 150 cadeiras para recepção."),
        ("Louças e talheres", "Buscamos locação de louças, talheres e taças para 150 pessoas."),
        ("Sofás para lounge", "Queremos criar área lounge com sofás e poltronas para convidados."),
    ],
    17: [  # Bebidas
        ("Bar de drinks aberto", "Procuro fornecedor de bebidas para bar aberto (destilados, vinhos, cervejas)."),
        ("Vinhos importados", "Buscamos seleção de vinhos importados para jantar."),
        ("Whisky premium para brinde", "Queremos whisky premium para brinde dos padrinhos."),
    ],
    18: [  # Espaços para Cerimônia
        ("Local para cerimônia ao ar livre", "Procuro espaço ao ar livre para cerimônia, capacidade 150 pessoas."),
        ("Capela para cerimônia", "Buscamos capela ou igreja para cerimônia religiosa, região sul."),
        ("Jardim para cerimônia", "Queremos jardim ou área externa para cerimônia intimista."),
    ],
    19: [  # Espaços para Recepção
        ("Salão para festa de casamento", "Procuro salão para recepção, capacidade 150-200 pessoas, com cozinha."),
        ("Espaço rústico para festa", "Buscamos local estilo fazenda/rústico para recepção."),
        ("Clube para casamento", "Queremos alugar clube ou espaço com piscina para festa."),
    ],
    20: [  # Hospedagem
        ("Hotel para lua de mel", "Procuro pacote de lua de mel 7 dias, destino praia."),
        ("Hospedagem para convidados", "Buscamos hotel para hospedar 20 convidados de fora da cidade."),
        ("Pousada para pré-casamento", "Queremos pousada para noivos e família ficarem no dia anterior."),
    ],
}

# Gerar variações de orçamento por categoria
orcamentos = {
    1: (2000, 8000),    # Fotografia
    2: (1500, 6000),    # Música
    3: (8000, 25000),   # Buffet
    4: (3000, 10000),   # Cerimonial
    5: (800, 3000),     # Celebrante
    6: (500, 3000),     # Beleza
    7: (1000, 5000),    # Transporte
    8: (5000, 20000),   # Decoração
    9: (800, 3000),     # Segurança
    10: (500, 2000),    # Limpeza
    11: (3000, 15000),  # Vestidos
    12: (2000, 10000),  # Alianças
    13: (800, 4000),    # Convites
    14: (1500, 6000),   # Bolos
    15: (1000, 5000),   # Flores
    16: (2000, 8000),   # Móveis
    17: (3000, 12000),  # Bebidas
    18: (2000, 10000),  # Espaço cerimônia
    19: (5000, 20000),  # Espaço recepção
    20: (8000, 30000),  # Hospedagem
}

# Prazos típicos (em dias a partir de hoje)
prazos_base = [30, 45, 60, 90, 120, 150, 180]

# Status possíveis
status_opcoes = ['ATIVA', 'ATIVA', 'ATIVA', 'ATIVA', 'FINALIZADA', 'CANCELADA']  # 4x mais ATIVAs

demandas_criadas = []

# Gerar 60 demandas
for i in range(60):
    # Selecionar casal aleatório
    id_casal = random.randint(1, 10)

    # Selecionar categoria aleatória
    id_categoria = random.randint(1, 20)

    # Pegar template aleatório da categoria
    templates_categoria = demandas_templates.get(id_categoria, [("Demanda genérica", "Descrição genérica")])
    titulo_base, descricao_base = random.choice(templates_categoria)

    # Personalizar título
    titulo = f"{titulo_base} - #{i+1}"

    # Adicionar detalhes à descrição
    detalhes_extras = [
        "Preferência por profissionais com experiência comprovada.",
        "Necessário apresentar portfolio de trabalhos anteriores.",
        "Flexibilidade de horário e disponibilidade no fim de semana.",
        "Orçamento inclui materiais e mão de obra.",
        "Pagamento pode ser parcelado.",
        "Prazo pode ser negociável.",
        "Procuramos qualidade e bom atendimento.",
        "Referências serão solicitadas.",
        "Necessário atender região metropolitana.",
        "Disponibilidade para reunião presencial.",
    ]
    descricao = f"{descricao_base} {random.choice(detalhes_extras)}"

    # Definir orçamento
    orc_min_base, orc_max_base = orcamentos.get(id_categoria, (1000, 5000))
    margem = random.uniform(0.8, 1.2)
    orcamento_min = round(orc_min_base * margem, 2)
    orcamento_max = round(orc_max_base * margem, 2)

    # Definir prazo
    dias_prazo = random.choice(prazos_base) + random.randint(-10, 10)
    prazo_entrega = (datetime.now() + timedelta(days=dias_prazo)).strftime('%Y-%m-%d')

    # Definir status (mais ATIVAs que outras)
    status = random.choice(status_opcoes)

    # Observações (algumas com, outras sem)
    observacoes_opcoes = [
        None,
        "Preferência por fornecedores da região",
        "Orçamento pode ser ajustado mediante negociação",
        "Urgente - prazo curto",
        "Flexível quanto ao prazo",
        "Já tenho algumas indicações, mas aceito outras propostas",
        "Preciso de pelo menos 3 orçamentos para comparar",
        "Qualidade é prioridade",
    ]
    observacoes = random.choice(observacoes_opcoes)

    demandas_criadas.append((
        id_casal,
        id_categoria,
        titulo,
        descricao,
        orcamento_min,
        orcamento_max,
        prazo_entrega,
        status,
        observacoes
    ))

# Inserir no banco
cursor.executemany('''
    INSERT INTO demanda (
        id_casal, id_categoria, titulo, descricao,
        orcamento_min, orcamento_max, prazo_entrega, status, observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', demandas_criadas)

conn.commit()

# Verificar inserção
cursor.execute("SELECT COUNT(*) FROM demanda")
total = cursor.fetchone()[0]

print(f"✅ {total} demandas criadas com sucesso!")

# Mostrar algumas estatísticas
cursor.execute("""
    SELECT status, COUNT(*) as total
    FROM demanda
    GROUP BY status
    ORDER BY total DESC
""")
print("\n📊 Distribuição por status:")
for status, count in cursor.fetchall():
    print(f"  {status}: {count}")

cursor.execute("""
    SELECT c.nome, COUNT(d.id) as total
    FROM categoria c
    LEFT JOIN demanda d ON c.id = d.id_categoria
    GROUP BY c.id, c.nome
    HAVING total > 0
    ORDER BY total DESC
    LIMIT 5
""")
print("\n📈 Top 5 categorias com mais demandas:")
for nome, count in cursor.fetchall():
    print(f"  {nome}: {count}")

conn.close()
print("\n✅ Script concluído!")
