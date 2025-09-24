from typing import Optional
from model.usuario_model import Usuario, TipoUsuario
from model.categoria_model import Categoria
from model.item_model import TipoItem, Item
from model.fornecedor_model import Fornecedor
from model.casal_model import Casal
from repo import usuario_repo, fornecedor_repo, casal_repo, item_repo, categoria_repo, fornecedor_item_repo, item_demanda_repo, item_orcamento_repo, demanda_repo, orcamento_repo, favorito_repo, chat_repo
from util.security import criar_hash_senha
from util.migracoes_avatar import migrar_sistema_avatar
import random

def criar_tabelas_banco():
    """
    Cria todas as tabelas necessárias no banco de dados.
    """
    usuario_repo.criar_tabela_usuarios()
    fornecedor_repo.criar_tabela_fornecedor()
    casal_repo.criar_tabela_casal()
    item_repo.criar_tabela_item()
    categoria_repo.criar_tabela_categorias()
    fornecedor_item_repo.criar_tabela_fornecedor_item()
    demanda_repo.criar_tabela_demandas()
    orcamento_repo.criar_tabela_orcamento()
    item_demanda_repo.criar_tabela_item_demanda()
    item_orcamento_repo.criar_tabela_item_orcamento()
    favorito_repo.criar_tabela_favoritos()
    chat_repo.criar_tabela_chat()

def criar_admin_padrao() -> Optional[int]:
    """
    Cria um administrador padrão se não existir nenhum admin no sistema.
    Retorna o ID do admin criado ou None se já existir um admin.
    """
    try:
        # Buscar por um admin existente (simplificado - seria melhor ter uma query específica)
        # Por ora, vamos verificar se existe um usuário com email admin específico
        admin_existente = usuario_repo.obter_usuario_por_email("admin@casebem.com")

        if admin_existente:
            print("✅ Administrador já existe no sistema")
            return admin_existente.id

        # Criar administrador padrão
        senha_hash = criar_hash_senha("1234aA@#")  # Senha padrão - deve ser alterada no primeiro login

        admin = Usuario(
            id=0,
            nome="Administrador Padrão",
            cpf=None,
            data_nascimento=None,
            email="admin@casebem.com",
            telefone="(28) 99999-0000",
            senha=senha_hash,
            perfil=TipoUsuario.ADMIN,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )

        admin_id = usuario_repo.inserir_usuario(admin)

        if admin_id:
            print(f"✅ Administrador padrão criado com sucesso! ID: {admin_id}")
            print("📧 Email: admin@casebem.com")
            print("🔑 Senha: 1234aA@#")
            print("⚠️ IMPORTANTE: Altere a senha no primeiro login!")
            return admin_id
        else:
            print("❌ Erro ao criar administrador padrão")
            return None

    except Exception as e:
        print(f"❌ Erro ao verificar/criar administrador: {e}")
        return None

def criar_categorias():
    """
    Cria categorias padrão para casamentos se não existirem no sistema.
    """
    try:
        # Verificar se já existem categorias
        categorias_existentes = categoria_repo.obter_categorias()
        if categorias_existentes:
            print("✅ Categorias já existem no sistema")
            return

        # Categorias do tipo SERVIÇO (10 categorias)
        categorias_servico = [
            Categoria(0, "Fotografia e Filmagem", TipoItem.SERVICO, "Serviços de registro fotográfico e audiovisual do casamento"),
            Categoria(0, "Música e Som", TipoItem.SERVICO, "DJ, banda, músicos e equipamentos de som"),
            Categoria(0, "Buffet e Catering", TipoItem.SERVICO, "Serviços de alimentação e bebidas"),
            Categoria(0, "Cerimonial e Assessoria", TipoItem.SERVICO, "Organização e coordenação do evento"),
            Categoria(0, "Celebrante", TipoItem.SERVICO, "Oficialização da cerimônia religiosa ou civil"),
            Categoria(0, "Beleza e Estética", TipoItem.SERVICO, "Maquiagem, cabelo, manicure e tratamentos"),
            Categoria(0, "Transporte", TipoItem.SERVICO, "Aluguel de carros, limusines e outros veículos"),
            Categoria(0, "Decoração e Ambientação", TipoItem.SERVICO, "Decoração floral e temática do evento"),
            Categoria(0, "Segurança", TipoItem.SERVICO, "Serviços de segurança para o evento"),
            Categoria(0, "Limpeza", TipoItem.SERVICO, "Limpeza pós-evento")
        ]

        # Categorias do tipo PRODUTO (7 categorias)
        categorias_produto = [
            Categoria(0, "Vestidos e Roupas", TipoItem.PRODUTO, "Vestidos de noiva, ternos e roupas para cerimônia"),
            Categoria(0, "Alianças e Joias", TipoItem.PRODUTO, "Alianças de casamento e joias"),
            Categoria(0, "Convites e Papelaria", TipoItem.PRODUTO, "Convites, lembrancinhas e papelaria personalizada"),
            Categoria(0, "Bolos e Doces", TipoItem.PRODUTO, "Bolos de casamento e doces finos"),
            Categoria(0, "Flores e Arranjos", TipoItem.PRODUTO, "Buquês, arranjos florais e plantas"),
            Categoria(0, "Móveis e Utensílios", TipoItem.PRODUTO, "Móveis, louças e utensílios para a festa"),
            Categoria(0, "Bebidas", TipoItem.PRODUTO, "Vinhos, champanhe e outras bebidas especiais")
        ]

        # Categorias do tipo ESPAÇO (3 categorias)
        categorias_espaco = [
            Categoria(0, "Espaços para Cerimônia", TipoItem.ESPACO, "Igrejas, jardins e locais para a cerimônia"),
            Categoria(0, "Espaços para Recepção", TipoItem.ESPACO, "Salões, sítios e locais para a festa"),
            Categoria(0, "Hospedagem", TipoItem.ESPACO, "Hotéis e pousadas para convidados")
        ]

        # Inserir todas as categorias
        todas_categorias = categorias_servico + categorias_produto + categorias_espaco

        for categoria in todas_categorias:
            categoria_id = categoria_repo.inserir_categoria(categoria)
            if categoria_id:
                print(f"✅ Categoria '{categoria.nome}' criada com sucesso")
            else:
                print(f"❌ Erro ao criar categoria '{categoria.nome}'")

        print(f"✅ {len(todas_categorias)} categorias padrão criadas com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar categorias padrão: {e}")

def gerar_itens_por_categoria():
    """
    Gera um conjunto diversificado de itens garantindo 1-4 itens por categoria.
    """
    itens_templates = {
        # SERVIÇOS
        "Fotografia e Filmagem": [
            {"nome": "Ensaio Pré-Wedding", "preco": 850.0, "descricao": "Sessão fotográfica romântica antes do casamento"},
            {"nome": "Cobertura Completa do Casamento", "preco": 2500.0, "descricao": "Fotografia completa da cerimônia e recepção"},
            {"nome": "Filmagem Cerimônia", "preco": 1200.0, "descricao": "Filmagem profissional da cerimônia religiosa"},
            {"nome": "Vídeo Highlights", "preco": 800.0, "descricao": "Vídeo resumo dos melhores momentos"}
        ],
        "Música e Som": [
            {"nome": "DJ para Cerimônia", "preco": 650.0, "descricao": "DJ especializado em cerimônias religiosas"},
            {"nome": "DJ para Recepção 6h", "preco": 1200.0, "descricao": "DJ para festa com 6 horas de duração"},
            {"nome": "Iluminação LED Premium", "preco": 850.0, "descricao": "Sistema de iluminação completo"},
            {"nome": "Som para Cerimônia", "preco": 350.0, "descricao": "Sistema de som para cerimônia"}
        ],
        "Buffet e Catering": [
            {"nome": "Buffet Completo 100 pessoas", "preco": 4500.0, "descricao": "Buffet completo para 100 convidados"},
            {"nome": "Buffet Completo 150 pessoas", "preco": 6200.0, "descricao": "Buffet completo para 150 convidados"},
            {"nome": "Bar Premium", "preco": 1200.0, "descricao": "Serviço de bar com drinks premium"},
            {"nome": "Mesa de Doces Finos", "preco": 850.0, "descricao": "Mesa de doces gourmet"}
        ],
        "Beleza e Estética": [
            {"nome": "Maquiagem de Noiva", "preco": 280.0, "descricao": "Maquiagem profissional para noiva"},
            {"nome": "Penteado de Noiva", "preco": 220.0, "descricao": "Penteado elegante para noiva"},
            {"nome": "Teste de Maquiagem", "preco": 120.0, "descricao": "Teste antes do casamento"},
            {"nome": "Maquiagem Madrinhas", "preco": 80.0, "descricao": "Maquiagem para madrinhas"}
        ],
        "Transporte": [
            {"nome": "Limousine Branca", "preco": 850.0, "descricao": "Limousine para transporte dos noivos"},
            {"nome": "Carro Antigo Conversível", "preco": 650.0, "descricao": "Carro clássico para fotos"},
            {"nome": "Van para Convidados", "preco": 350.0, "descricao": "Transporte para convidados"}
        ],
        "Cerimonial e Assessoria": [
            {"nome": "Cerimonial Completo", "preco": 2500.0, "descricao": "Assessoria completa do casamento"},
            {"nome": "Cerimonial Cerimônia", "preco": 800.0, "descricao": "Coordenação apenas da cerimônia"}
        ],
        "Celebrante": [
            {"nome": "Celebrante Religioso", "preco": 500.0, "descricao": "Celebrante para cerimônia religiosa"},
            {"nome": "Celebrante Civil", "preco": 400.0, "descricao": "Celebrante para cerimônia civil"}
        ],
        "Decoração e Ambientação": [
            {"nome": "Decoração Completa", "preco": 3500.0, "descricao": "Decoração completa do evento"},
            {"nome": "Decoração do Altar", "preco": 650.0, "descricao": "Decoração específica do altar"},
            {"nome": "Arranjos Mesa", "preco": 85.0, "descricao": "Arranjos para mesas dos convidados"}
        ],
        "Segurança": [
            {"nome": "Segurança Particular", "preco": 400.0, "descricao": "Serviço de segurança para o evento"}
        ],
        "Limpeza": [
            {"nome": "Limpeza Pós-Evento", "preco": 300.0, "descricao": "Limpeza completa após o evento"}
        ],

        # PRODUTOS
        "Vestidos e Roupas": [
            {"nome": "Vestido de Noiva Princesa", "preco": 2800.0, "descricao": "Vestido estilo princesa com cauda"},
            {"nome": "Vestido de Noiva Sereia", "preco": 3200.0, "descricao": "Vestido estilo sereia moderno"},
            {"nome": "Véu de Noiva 3 metros", "preco": 280.0, "descricao": "Véu longo para cerimônia"},
            {"nome": "Sapato de Noiva Perolado", "preco": 320.0, "descricao": "Sapato elegante perolado"}
        ],
        "Alianças e Joias": [
            {"nome": "Aliança Ouro 18k Lisa", "preco": 580.0, "descricao": "Aliança clássica em ouro 18k"},
            {"nome": "Aliança com Diamante", "preco": 1200.0, "descricao": "Aliança com diamantes cravados"},
            {"nome": "Anel de Noivado Solitário", "preco": 2200.0, "descricao": "Anel solitário com diamante"},
            {"nome": "Brincos de Pérola", "preco": 320.0, "descricao": "Brincos elegantes de pérola"}
        ],
        "Convites e Papelaria": [
            {"nome": "Convite Clássico 100un", "preco": 350.0, "descricao": "Convites clássicos 100 unidades"},
            {"nome": "Save the Date 100un", "preco": 220.0, "descricao": "Save the Date 100 unidades"},
            {"nome": "Menu Personalizado 100un", "preco": 180.0, "descricao": "Menus personalizados"},
            {"nome": "Lembrancinha Sabonete 100un", "preco": 280.0, "descricao": "Lembrancinhas de sabonete"}
        ],
        "Bolos e Doces": [
            {"nome": "Bolo de Casamento 3 andares", "preco": 380.0, "descricao": "Bolo tradicional de 3 andares"},
            {"nome": "Bem-Casados 100un", "preco": 250.0, "descricao": "Bem-casados tradicionais"},
            {"nome": "Doces Finos 100un", "preco": 320.0, "descricao": "Seleção de doces finos"}
        ],
        "Flores e Arranjos": [
            {"nome": "Buquê de Noiva Rosas", "preco": 280.0, "descricao": "Buquê clássico com rosas brancas"},
            {"nome": "Buquê de Noiva Peônias", "preco": 350.0, "descricao": "Buquê sofisticado com peônias"},
            {"nome": "Corsage para Madrinhas", "preco": 25.0, "descricao": "Arranjo para pulso das madrinhas"},
            {"nome": "Boutonnière para Noivo", "preco": 35.0, "descricao": "Flor para lapela do noivo"}
        ],
        "Móveis e Utensílios": [
            {"nome": "Mesa Redonda 8 pessoas", "preco": 45.0, "descricao": "Mesa redonda para 8 convidados"},
            {"nome": "Cadeira Tiffany", "preco": 8.0, "descricao": "Cadeira elegante estilo Tiffany"},
            {"nome": "Toalha Mesa Rendada", "preco": 25.0, "descricao": "Toalha de mesa com renda"}
        ],
        "Bebidas": [
            {"nome": "Champagne Importado", "preco": 180.0, "descricao": "Champagne francês para brinde"},
            {"nome": "Vinho Tinto Seleção", "preco": 85.0, "descricao": "Vinho tinto nacional selecionado"},
            {"nome": "Caipirinha Bar", "preco": 12.0, "descricao": "Caipirinha preparada na hora"}
        ],

        # ESPAÇOS
        "Espaços para Cerimônia": [
            {"nome": "Capela Ecumênica", "preco": 600.0, "descricao": "Capela para cerimônias religiosas"},
            {"nome": "Jardim para Cerimônia", "preco": 800.0, "descricao": "Jardim paisagístico ao ar livre"},
            {"nome": "Gazebo para Cerimônia", "preco": 350.0, "descricao": "Gazebo romântico para altar"}
        ],
        "Espaços para Recepção": [
            {"nome": "Salão de Festas 100 pessoas", "preco": 1800.0, "descricao": "Salão climatizado para 100 convidados"},
            {"nome": "Salão de Festas 150 pessoas", "preco": 2400.0, "descricao": "Salão amplo para 150 convidados"},
            {"nome": "Espaço Gourmet", "preco": 450.0, "descricao": "Área para coquetel e confraternização"},
            {"nome": "Sala de Noiva", "preco": 200.0, "descricao": "Espaço exclusivo para preparação da noiva"}
        ],
        "Hospedagem": [
            {"nome": "Suíte Presidencial", "preco": 350.0, "descricao": "Suíte luxo para os noivos"},
            {"nome": "Quarto Standard", "preco": 120.0, "descricao": "Quarto confortável para convidados"},
            {"nome": "Pacote Weekend", "preco": 280.0, "descricao": "Pacote final de semana para família"}
        ]
    }

    return itens_templates

def criar_fornecedores_inteligente():
    """
    Cria fornecedores de teste com distribuição inteligente de itens por categoria.
    Garante que cada categoria tenha entre 1-4 itens.
    """
    try:
        # Verificar se já existem fornecedores
        total_fornecedores = fornecedor_repo.contar_fornecedores()
        if total_fornecedores >= 5:
            print("✅ Fornecedores de teste já existem no sistema")
            return

        # Obter categorias para associar aos itens
        categorias = categoria_repo.obter_categorias()
        if not categorias:
            print("❌ Nenhuma categoria encontrada. Execute criar_categorias() primeiro.")
            return

        # Obter templates de itens
        itens_templates = gerar_itens_por_categoria()

        print("🏢 Criando fornecedores com distribuição inteligente de itens...")

        # Criar um mapeamento de categoria para seus itens
        categoria_para_itens = {}
        for categoria in categorias:
            if categoria.nome in itens_templates:
                categoria_para_itens[categoria.id] = itens_templates[categoria.nome]

        # Distribuir itens aleatoriamente garantindo 1-4 por categoria
        itens_por_categoria = {}
        for categoria_id, itens_disponiveis in categoria_para_itens.items():
            # Escolher entre 1-4 itens aleatoriamente para esta categoria
            quantidade = random.randint(1, min(4, len(itens_disponiveis)))
            itens_selecionados = random.sample(itens_disponiveis, quantidade)
            itens_por_categoria[categoria_id] = itens_selecionados

        # Criar fornecedores para distribuir os itens
        fornecedores_base = [
            {
                "nome": "Ana Costa",
                "email": "ana@casamentosperfeitos.com",
                "telefone": "(11) 98765-4321",
                "empresa": "Casamentos Perfeitos",
                "cnpj": "12.345.678/0001-90",
                "descricao": "Empresa especializada em produtos e serviços para casamentos"
            },
            {
                "nome": "Carlos Silva",
                "email": "carlos@eventosmagicos.com",
                "telefone": "(21) 99876-5432",
                "empresa": "Eventos Mágicos",
                "cnpj": "23.456.789/0001-01",
                "descricao": "Prestadora de serviços completos para eventos especiais"
            },
            {
                "nome": "Mariana Santos",
                "email": "mariana@belezaperfeita.com",
                "telefone": "(31) 98765-9876",
                "empresa": "Beleza & Estilo",
                "cnpj": "34.567.890/0001-12",
                "descricao": "Especializada em beleza e produtos para noivas"
            },
            {
                "nome": "Pedro Oliveira",
                "email": "pedro@espacoseletos.com",
                "telefone": "(41) 99654-3210",
                "empresa": "Espaços Seletos",
                "cnpj": "45.678.901/0001-23",
                "descricao": "Locação de espaços únicos para cerimônias e recepções"
            },
            {
                "nome": "Julia Ferreira",
                "email": "julia@fornecedorpremium.com",
                "telefone": "(51) 98888-7777",
                "empresa": "Premium Fornecedores",
                "cnpj": "56.789.012/0001-34",
                "descricao": "Fornecedora premium de produtos e serviços de luxo"
            }
        ]

        # Distribuir categorias entre fornecedores
        categorias_ids = list(itens_por_categoria.keys())
        random.shuffle(categorias_ids)

        categorias_por_fornecedor = []
        for i in range(len(fornecedores_base)):
            categorias_por_fornecedor.append([])

        # Distribuir categorias garantindo que cada fornecedor tenha pelo menos uma
        for i, categoria_id in enumerate(categorias_ids):
            fornecedor_idx = i % len(fornecedores_base)
            categorias_por_fornecedor[fornecedor_idx].append(categoria_id)

        # Criar fornecedores e seus itens
        for i, fornecedor_data in enumerate(fornecedores_base):
            # Criar fornecedor
            senha_hash = criar_hash_senha("1234aA@#")

            fornecedor = Fornecedor(
                id=0,
                nome=fornecedor_data["nome"],
                cpf=None,
                data_nascimento=None,
                email=fornecedor_data["email"],
                telefone=fornecedor_data["telefone"],
                senha=senha_hash,
                perfil=TipoUsuario.FORNECEDOR,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                ativo=True,
                nome_empresa=fornecedor_data["empresa"],
                cnpj=fornecedor_data["cnpj"],
                descricao=fornecedor_data["descricao"],
                prestador=True,
                vendedor=True,
                locador=True,
                verificado=True
            )

            fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)

            if fornecedor_id:
                print(f"✅ Fornecedor '{fornecedor.nome_empresa}' criado com sucesso! ID: {fornecedor_id}")

                # Criar itens para as categorias deste fornecedor
                total_itens = 0
                for categoria_id in categorias_por_fornecedor[i]:
                    categoria = next((c for c in categorias if c.id == categoria_id), None)
                    if categoria and categoria_id in itens_por_categoria:
                        for item_data in itens_por_categoria[categoria_id]:
                            item = Item(
                                id=0,
                                id_fornecedor=fornecedor_id,
                                tipo=categoria.tipo_fornecimento,
                                nome=item_data["nome"],
                                descricao=item_data["descricao"],
                                preco=item_data["preco"],
                                id_categoria=categoria_id,
                                observacoes=None,
                                ativo=True,
                                data_cadastro=None
                            )

                            item_id = item_repo.inserir_item(item)
                            if item_id:
                                print(f"  ✅ Item '{item.nome}' criado na categoria '{categoria.nome}' - R$ {item.preco:.2f}")
                                total_itens += 1
                            else:
                                print(f"  ❌ Erro ao criar item '{item.nome}'")

                print(f"  📦 Total de {total_itens} itens criados para {fornecedor.nome_empresa}")
            else:
                print(f"❌ Erro ao criar fornecedor '{fornecedor_data['empresa']}'")

        print("✅ Fornecedores e itens criados com distribuição inteligente!")

    except Exception as e:
        print(f"❌ Erro ao criar fornecedores: {e}")

def criar_fornecedores_exemplo():
    """
    Cria fornecedores com dados fictícios para teste, cada um com seus respectivos itens.
    """
    try:
        # Verificar se já existem fornecedores
        total_fornecedores = fornecedor_repo.contar_fornecedores()
        if total_fornecedores >= 10:
            print("✅ Fornecedores de teste já existem no sistema")
            return

        # Obter categorias para associar aos itens
        categorias = categoria_repo.obter_categorias()
        if not categorias:
            print("❌ Nenhuma categoria encontrada. Execute criar_categorias() primeiro.")
            return

        # Criar mapeamento de categorias por tipo
        categorias_por_tipo = {
            TipoItem.SERVICO: [c for c in categorias if c.tipo_fornecimento == TipoItem.SERVICO],
            TipoItem.PRODUTO: [c for c in categorias if c.tipo_fornecimento == TipoItem.PRODUTO],
            TipoItem.ESPACO: [c for c in categorias if c.tipo_fornecimento == TipoItem.ESPACO]
        }

        # Dados dos fornecedores com seus respectivos itens
        fornecedores_dados = [
            {
                "fornecedor": {
                    "nome": "João Silva",
                    "email": "joao@fotosmagicas.com",
                    "telefone": "(11) 98765-4321",
                    "nome_empresa": "Fotos Mágicas Studio",
                    "cnpj": "12.345.678/0001-90",
                    "descricao": "Especialistas em fotografia e filmagem de casamentos há mais de 10 anos",
                    "prestador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Ensaio Pré-Wedding", "tipo": TipoItem.SERVICO, "preco": 850.0, "descricao": "Sessão fotográfica romântica antes do casamento"},
                    {"nome": "Cobertura Completa do Casamento", "tipo": TipoItem.SERVICO, "preco": 2500.0, "descricao": "Fotografia completa da cerimônia e recepção"},
                    {"nome": "Filmagem Cerimônia", "tipo": TipoItem.SERVICO, "preco": 1200.0, "descricao": "Filmagem profissional da cerimônia religiosa"},
                    {"nome": "Vídeo Highlights", "tipo": TipoItem.SERVICO, "preco": 800.0, "descricao": "Vídeo resumo dos melhores momentos"},
                    {"nome": "Álbum Premium 30x30", "tipo": TipoItem.PRODUTO, "preco": 450.0, "descricao": "Álbum fotográfico luxo com 60 fotos"},
                    {"nome": "Pendrive Personalizado", "tipo": TipoItem.PRODUTO, "preco": 120.0, "descricao": "Pendrive com todas as fotos em alta resolução"},
                    {"nome": "Impressões 15x21", "tipo": TipoItem.PRODUTO, "preco": 3.5, "descricao": "Impressão fotográfica premium por unidade"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Maria Santos",
                    "email": "maria@floresdoamor.com",
                    "telefone": "(21) 99876-5432",
                    "nome_empresa": "Flores do Amor",
                    "cnpj": "23.456.789/0001-01",
                    "descricao": "Floricultura especializada em arranjos para casamentos e eventos especiais",
                    "vendedor": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Buquê de Noiva Rosas Brancas", "tipo": TipoItem.PRODUTO, "preco": 280.0, "descricao": "Buquê clássico com rosas brancas importadas"},
                    {"nome": "Buquê de Noiva Peônias", "tipo": TipoItem.PRODUTO, "preco": 350.0, "descricao": "Buquê sofisticado com peônias cor de rosa"},
                    {"nome": "Arranjo Central Mesa Redonda", "tipo": TipoItem.PRODUTO, "preco": 85.0, "descricao": "Arranjo floral para centro de mesa"},
                    {"nome": "Corsage para Madrinhas", "tipo": TipoItem.PRODUTO, "preco": 25.0, "descricao": "Pequeno arranjo para pulso das madrinhas"},
                    {"nome": "Decoração Floral do Altar", "tipo": TipoItem.SERVICO, "preco": 650.0, "descricao": "Decoração completa do altar da cerimônia"},
                    {"nome": "Pétala de Rosas para Cerimônia", "tipo": TipoItem.PRODUTO, "preco": 45.0, "descricao": "Pétalas naturais para jogada dos convidados"},
                    {"nome": "Boutonnière para Noivo", "tipo": TipoItem.PRODUTO, "preco": 35.0, "descricao": "Flor para lapela do noivo e padrinhos"},
                    {"nome": "Arranjo de Entrada", "tipo": TipoItem.PRODUTO, "preco": 120.0, "descricao": "Arranjo floral para entrada do local"},
                    {"nome": "Coroa de Flores para Daminha", "tipo": TipoItem.PRODUTO, "preco": 55.0, "descricao": "Delicada coroa de flores para daminha"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Carlos Oliveira",
                    "email": "carlos@saboresdacasa.com",
                    "telefone": "(31) 98765-1234",
                    "nome_empresa": "Sabores da Casa Buffet",
                    "cnpj": "34.567.890/0001-12",
                    "descricao": "Buffet completo para casamentos com 25 anos de experiência",
                    "prestador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Buffet Completo 100 pessoas", "tipo": TipoItem.SERVICO, "preco": 4500.0, "descricao": "Buffet completo para até 100 convidados"},
                    {"nome": "Buffet Completo 150 pessoas", "tipo": TipoItem.SERVICO, "preco": 6200.0, "descricao": "Buffet completo para até 150 convidados"},
                    {"nome": "Buffet Completo 200 pessoas", "tipo": TipoItem.SERVICO, "preco": 7800.0, "descricao": "Buffet completo para até 200 convidados"},
                    {"nome": "Bar Premium", "tipo": TipoItem.SERVICO, "preco": 1200.0, "descricao": "Serviço de bar com bebidas premium"},
                    {"nome": "Mesa de Doces Finos", "tipo": TipoItem.SERVICO, "preco": 850.0, "descricao": "Mesa especial com doces gourmet"},
                    {"nome": "Coquetel de Boas-Vindas", "tipo": TipoItem.SERVICO, "preco": 450.0, "descricao": "Recepção com drinks e canapés"},
                    {"nome": "Bolo de Casamento 3 andares", "tipo": TipoItem.PRODUTO, "preco": 380.0, "descricao": "Bolo decorado para 100 pessoas"},
                    {"nome": "Bem-Casados (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 250.0, "descricao": "Doces tradicionais embalados"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Ana Costa",
                    "email": "ana@vestirbem.com",
                    "telefone": "(41) 99123-4567",
                    "nome_empresa": "Vestir Bem Atelier",
                    "cnpj": "45.678.901/0001-23",
                    "descricao": "Atelier especializado em vestidos de noiva sob medida",
                    "vendedor": True,
                    "locador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Vestido de Noiva Princesa", "tipo": TipoItem.PRODUTO, "preco": 2800.0, "descricao": "Vestido estilo princesa com cauda longa"},
                    {"nome": "Vestido de Noiva Sereia", "tipo": TipoItem.PRODUTO, "preco": 3200.0, "descricao": "Vestido modelo sereia com renda francesa"},
                    {"nome": "Vestido de Noiva Minimalista", "tipo": TipoItem.PRODUTO, "preco": 2200.0, "descricao": "Vestido clean e elegante"},
                    {"nome": "Véu de Noiva 3 metros", "tipo": TipoItem.PRODUTO, "preco": 280.0, "descricao": "Véu longo com bordado delicado"},
                    {"nome": "Véu de Noiva 1,5 metros", "tipo": TipoItem.PRODUTO, "preco": 180.0, "descricao": "Véu médio simples"},
                    {"nome": "Sapato de Noiva Perolado", "tipo": TipoItem.PRODUTO, "preco": 320.0, "descricao": "Sapato confortável com pérolas"},
                    {"nome": "Tiara com Cristais", "tipo": TipoItem.PRODUTO, "preco": 150.0, "descricao": "Tiara delicada com cristais Swarovski"},
                    {"nome": "Luvas de Renda", "tipo": TipoItem.PRODUTO, "preco": 85.0, "descricao": "Luvas longas de renda francesa"},
                    {"nome": "Anágua para Vestido", "tipo": TipoItem.PRODUTO, "preco": 120.0, "descricao": "Anágua estruturada para dar volume"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Roberto Lima",
                    "email": "roberto@musicacerta.com",
                    "telefone": "(51) 98765-9876",
                    "nome_empresa": "Música Certa",
                    "cnpj": "56.789.012/0001-34",
                    "descricao": "DJ profissional e aluguel de equipamentos de som para eventos",
                    "prestador": True,
                    "locador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "DJ para Cerimônia", "tipo": TipoItem.SERVICO, "preco": 650.0, "descricao": "Sonorização profissional da cerimônia"},
                    {"nome": "DJ para Recepção 6h", "tipo": TipoItem.SERVICO, "preco": 1200.0, "descricao": "DJ para festa com 6 horas de duração"},
                    {"nome": "DJ para Recepção 8h", "tipo": TipoItem.SERVICO, "preco": 1500.0, "descricao": "DJ para festa com 8 horas de duração"},
                    {"nome": "Iluminação LED Básica", "tipo": TipoItem.SERVICO, "preco": 450.0, "descricao": "Iluminação colorida para pista de dança"},
                    {"nome": "Iluminação LED Premium", "tipo": TipoItem.SERVICO, "preco": 850.0, "descricao": "Iluminação completa com efeitos especiais"},
                    {"nome": "Som para Cerimônia", "tipo": TipoItem.SERVICO, "preco": 350.0, "descricao": "Sistema de som para cerimônia ao ar livre"},
                    {"nome": "Microfone sem Fio", "tipo": TipoItem.PRODUTO, "preco": 80.0, "descricao": "Microfone profissional sem fio"},
                    {"nome": "Caixa de Som Portátil", "tipo": TipoItem.PRODUTO, "preco": 120.0, "descricao": "Caixa de som para ambientes pequenos"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Patricia Ferreira",
                    "email": "patricia@belezaperfeita.com",
                    "telefone": "(61) 99234-5678",
                    "nome_empresa": "Beleza Perfeita Studio",
                    "cnpj": "67.890.123/0001-45",
                    "descricao": "Studio de beleza especializado em noivas",
                    "prestador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Maquiagem de Noiva", "tipo": TipoItem.SERVICO, "preco": 280.0, "descricao": "Maquiagem completa para o grande dia"},
                    {"nome": "Penteado de Noiva", "tipo": TipoItem.SERVICO, "preco": 220.0, "descricao": "Penteado elegante e duradouro"},
                    {"nome": "Teste de Maquiagem", "tipo": TipoItem.SERVICO, "preco": 120.0, "descricao": "Teste de maquiagem antes do casamento"},
                    {"nome": "Teste de Penteado", "tipo": TipoItem.SERVICO, "preco": 100.0, "descricao": "Teste de penteado para escolher o ideal"},
                    {"nome": "Maquiagem Madrinhas (cada)", "tipo": TipoItem.SERVICO, "preco": 80.0, "descricao": "Maquiagem para madrinhas"},
                    {"nome": "Manicure e Pedicure", "tipo": TipoItem.SERVICO, "preco": 65.0, "descricao": "Cuidado completo das unhas"},
                    {"nome": "Limpeza de Pele", "tipo": TipoItem.SERVICO, "preco": 85.0, "descricao": "Tratamento facial profissional"},
                    {"nome": "Alongamento de Cílios", "tipo": TipoItem.SERVICO, "preco": 150.0, "descricao": "Aplicação de cílios fio a fio"},
                    {"nome": "Design de Sobrancelhas", "tipo": TipoItem.SERVICO, "preco": 45.0, "descricao": "Modelagem perfeita das sobrancelhas"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Eduardo Martins",
                    "email": "eduardo@aliancastop.com",
                    "telefone": "(85) 98123-4567",
                    "nome_empresa": "Alianças Top",
                    "cnpj": "78.901.234/0001-56",
                    "descricao": "Joalheria especializada em alianças de casamento",
                    "vendedor": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Aliança Ouro 18k Lisa", "tipo": TipoItem.PRODUTO, "preco": 580.0, "descricao": "Par de alianças em ouro 18k modelo tradicional"},
                    {"nome": "Aliança Ouro 18k com Diamante", "tipo": TipoItem.PRODUTO, "preco": 1200.0, "descricao": "Par de alianças com diamantes cravados"},
                    {"nome": "Aliança Ouro Branco 18k", "tipo": TipoItem.PRODUTO, "preco": 650.0, "descricao": "Par de alianças em ouro branco polido"},
                    {"nome": "Aliança com Gravação", "tipo": TipoItem.SERVICO, "preco": 80.0, "descricao": "Gravação personalizada nas alianças"},
                    {"nome": "Anel de Noivado Solitário", "tipo": TipoItem.PRODUTO, "preco": 2200.0, "descricao": "Anel com diamante solitário 50 pontos"},
                    {"nome": "Brincos de Pérola", "tipo": TipoItem.PRODUTO, "preco": 320.0, "descricao": "Brincos clássicos com pérolas naturais"},
                    {"nome": "Colar de Pérolas", "tipo": TipoItem.PRODUTO, "preco": 480.0, "descricao": "Colar delicado com pérolas graduadas"},
                    {"nome": "Pulseira de Ouro", "tipo": TipoItem.PRODUTO, "preco": 380.0, "descricao": "Pulseira elegante em ouro 18k"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Fernanda Ribeiro",
                    "email": "fernanda@convitesunicos.com",
                    "telefone": "(71) 99345-6789",
                    "nome_empresa": "Convites Únicos",
                    "cnpj": "89.012.345/0001-67",
                    "descricao": "Papelaria personalizada para casamentos",
                    "vendedor": True,
                    "prestador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Convite Clássico (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 350.0, "descricao": "Convites elegantes impressos em papel especial"},
                    {"nome": "Convite Premium (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 580.0, "descricao": "Convites luxo com acabamento dourado"},
                    {"nome": "Save the Date (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 220.0, "descricao": "Cartões para reservar a data"},
                    {"nome": "Menu Personalizado (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 180.0, "descricao": "Cardápios personalizados para mesa"},
                    {"nome": "Lembrancinha Sabonete (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 280.0, "descricao": "Sabonetes artesanais embalados"},
                    {"nome": "Lembrancinha Vela (100 unidades)", "tipo": TipoItem.PRODUTO, "preco": 320.0, "descricao": "Velas aromáticas personalizadas"},
                    {"nome": "Placa de Boas-Vindas", "tipo": TipoItem.PRODUTO, "preco": 120.0, "descricao": "Placa decorativa para entrada"},
                    {"nome": "Livro de Mensagens", "tipo": TipoItem.PRODUTO, "preco": 85.0, "descricao": "Livro para assinaturas dos convidados"},
                    {"nome": "Tags para Bem-Casados", "tipo": TipoItem.PRODUTO, "preco": 45.0, "descricao": "Etiquetas personalizadas para doces"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Marcos Souza",
                    "email": "marcos@transportevip.com",
                    "telefone": "(47) 98456-7890",
                    "nome_empresa": "Transporte VIP",
                    "cnpj": "90.123.456/0001-78",
                    "descricao": "Aluguel de veículos especiais para casamentos",
                    "locador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Limousine Branca", "tipo": TipoItem.SERVICO, "preco": 850.0, "descricao": "Limousine luxuosa para 8 pessoas"},
                    {"nome": "Carro Antigo Conversível", "tipo": TipoItem.SERVICO, "preco": 650.0, "descricao": "Carro clássico dos anos 60 restaurado"},
                    {"nome": "Rolls Royce", "tipo": TipoItem.SERVICO, "preco": 1200.0, "descricao": "Carro de luxo para momentos especiais"},
                    {"nome": "Van para Convidados", "tipo": TipoItem.SERVICO, "preco": 350.0, "descricao": "Transporte para grupos de até 15 pessoas"},
                    {"nome": "Decoração Automotiva", "tipo": TipoItem.SERVICO, "preco": 120.0, "descricao": "Decoração floral para veículos"},
                    {"nome": "Motorista Particular", "tipo": TipoItem.SERVICO, "preco": 180.0, "descricao": "Motorista profissional uniformizado"}
                ]
            },
            {
                "fornecedor": {
                    "nome": "Luciana Alves",
                    "email": "luciana@espacosmagicos.com",
                    "telefone": "(62) 99567-8901",
                    "nome_empresa": "Espaços Mágicos",
                    "cnpj": "01.234.567/0001-89",
                    "descricao": "Locação de espaços para cerimônias e recepções",
                    "locador": True,
                    "verificado": True
                },
                "itens": [
                    {"nome": "Salão de Festas 100 pessoas", "tipo": TipoItem.ESPACO, "preco": 1800.0, "descricao": "Salão climatizado para até 100 convidados"},
                    {"nome": "Salão de Festas 150 pessoas", "tipo": TipoItem.ESPACO, "preco": 2400.0, "descricao": "Salão amplo para até 150 convidados"},
                    {"nome": "Jardim para Cerimônia", "tipo": TipoItem.ESPACO, "preco": 800.0, "descricao": "Jardim paisagístico para cerimônia ao ar livre"},
                    {"nome": "Capela Ecumênica", "tipo": TipoItem.ESPACO, "preco": 600.0, "descricao": "Capela para cerimônias religiosas"},
                    {"nome": "Espaço Gourmet", "tipo": TipoItem.ESPACO, "preco": 450.0, "descricao": "Área para coquetel e confraternização"},
                    {"nome": "Sala de Noiva", "tipo": TipoItem.ESPACO, "preco": 200.0, "descricao": "Espaço exclusivo para preparação da noiva"},
                    {"nome": "Estacionamento Coberto", "tipo": TipoItem.ESPACO, "preco": 150.0, "descricao": "Estacionamento para 50 veículos"},
                    {"nome": "Gazebo para Cerimônia", "tipo": TipoItem.ESPACO, "preco": 350.0, "descricao": "Gazebo romântico para altar"}
                ]
            }
        ]

        print("🏢 Criando fornecedores de teste...")

        for fornecedor_data in fornecedores_dados:
            # Criar fornecedor
            senha_hash = criar_hash_senha("1234aA@#")

            fornecedor = Fornecedor(
                id=0,
                nome=fornecedor_data["fornecedor"]["nome"],
                cpf=None,
                data_nascimento=None,
                email=fornecedor_data["fornecedor"]["email"],
                telefone=fornecedor_data["fornecedor"]["telefone"],
                senha=senha_hash,
                perfil=TipoUsuario.FORNECEDOR,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                nome_empresa=fornecedor_data["fornecedor"]["nome_empresa"],
                cnpj=fornecedor_data["fornecedor"]["cnpj"],
                descricao=fornecedor_data["fornecedor"]["descricao"],
                prestador=fornecedor_data["fornecedor"].get("prestador", False),
                vendedor=fornecedor_data["fornecedor"].get("vendedor", False),
                locador=fornecedor_data["fornecedor"].get("locador", False),
                verificado=fornecedor_data["fornecedor"]["verificado"],
                newsletter=False
            )

            fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)

            if fornecedor_id:
                # Atualizar o ID do fornecedor no objeto
                fornecedor.id = fornecedor_id
                print(f"✅ Fornecedor '{fornecedor.nome_empresa}' criado com sucesso! ID: {fornecedor_id}")

                # Criar itens para este fornecedor
                for item_data in fornecedor_data["itens"]:
                    # Encontrar categoria apropriada para o tipo do item
                    categorias_tipo = categorias_por_tipo.get(item_data["tipo"], [])
                    categoria_id = None

                    if categorias_tipo:
                        # Mapeamento específico por fornecedor
                        nome_fornecedor = fornecedor_data["fornecedor"]["nome"]
                        if "Fotos Mágicas" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Fotografia" in c.nome), categorias_tipo[0].id)
                        elif "Flores do Amor" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Flores" in c.nome), categorias_tipo[0].id)
                        elif "Sabores da Casa" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Buffet" in c.nome), categorias_tipo[0].id)
                        elif "Vestir Bem" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Vestidos" in c.nome), categorias_tipo[0].id)
                        elif "Música Certa" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Música" in c.nome), categorias_tipo[0].id)
                        elif "Beleza Perfeita" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Beleza" in c.nome), categorias_tipo[0].id)
                        elif "Alianças Top" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Alianças" in c.nome), categorias_tipo[0].id)
                        elif "Convites Únicos" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Convites" in c.nome), categorias_tipo[0].id)
                        elif "Transporte VIP" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Transporte" in c.nome), categorias_tipo[0].id)
                        elif "Espaços Mágicos" in nome_fornecedor:
                            categoria_id = next((c.id for c in categorias_tipo if "Espaços" in c.nome), categorias_tipo[0].id)
                        else:
                            # Escolher categoria mais apropriada baseada no nome do item
                            for cat in categorias_tipo:
                                if any(palavra in item_data["nome"].lower() for palavra in cat.nome.lower().split()):
                                    categoria_id = cat.id
                                    break

                            # Se não encontrou categoria específica, usa a primeira do tipo
                            if not categoria_id:
                                categoria_id = categorias_tipo[0].id

                    item = Item(
                        id=0,
                        id_fornecedor=fornecedor_id,
                        tipo=item_data["tipo"],
                        nome=item_data["nome"],
                        descricao=item_data["descricao"],
                        preco=item_data["preco"],
                        observacoes=None,
                        ativo=True,
                        data_cadastro=None,
                        id_categoria=categoria_id
                    )

                    item_id = item_repo.inserir_item(item)
                    if item_id:
                        print(f"  ✅ Item '{item.nome}' criado - R$ {item.preco:.2f}")
                    else:
                        print(f"  ❌ Erro ao criar item '{item.nome}'")
            else:
                print(f"❌ Erro ao criar fornecedor '{fornecedor.nome_empresa}'")

        print("✅ Fornecedores e itens de teste criados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar fornecedores de teste: {e}")

def criar_casais_exemplo():
    """
    Cria 10 casais fictícios para teste com dados realistas.
    """
    try:
        # Verificar se já existem casais
        casais_existentes = casal_repo.obter_casais_por_pagina(1, 20)
        if len(casais_existentes) >= 10:
            print("✅ Casais de teste já existem no sistema")
            return

        # Dados fictícios dos casais
        casais_dados = [
            {
                "noivo1": {"nome": "João Silva", "email": "joao.silva@email.com", "telefone": "(11) 99888-7766", "cpf": "123.456.789-01"},
                "noiva1": {"nome": "Maria Santos", "email": "maria.santos@email.com", "telefone": "(11) 99888-7767", "cpf": "987.654.321-01"},
                "data_casamento": "2024-12-15",
                "local_previsto": "Igreja São João Batista - Salão Jardim das Rosas",
                "orcamento_estimado": "R$ 35.000,00",
                "numero_convidados": 120
            },
            {
                "noivo1": {"nome": "Pedro Oliveira", "email": "pedro.oliveira@email.com", "telefone": "(21) 98777-6655", "cpf": "234.567.890-12"},
                "noiva1": {"nome": "Ana Costa", "email": "ana.costa@email.com", "telefone": "(21) 98777-6656", "cpf": "876.543.210-12"},
                "data_casamento": "2025-02-22",
                "local_previsto": "Praia de Copacabana - Hotel Copacabana Palace",
                "orcamento_estimado": "R$ 85.000,00",
                "numero_convidados": 200
            },
            {
                "noivo1": {"nome": "Carlos Mendes", "email": "carlos.mendes@email.com", "telefone": "(31) 97666-5544", "cpf": "345.678.901-23"},
                "noiva1": {"nome": "Julia Ferreira", "email": "julia.ferreira@email.com", "telefone": "(31) 97666-5545", "cpf": "765.432.109-23"},
                "data_casamento": "2024-11-30",
                "local_previsto": "Fazenda Vista Alegre - Tiradentes/MG",
                "orcamento_estimado": "R$ 45.000,00",
                "numero_convidados": 80
            },
            {
                "noivo1": {"nome": "Rafael Lima", "email": "rafael.lima@email.com", "telefone": "(41) 96555-4433", "cpf": "456.789.012-34"},
                "noiva1": {"nome": "Camila Rodrigues", "email": "camila.rodrigues@email.com", "telefone": "(41) 96555-4434", "cpf": "654.321.098-34"},
                "data_casamento": "2025-03-15",
                "local_previsto": "Jardim Botânico de Curitiba",
                "orcamento_estimado": "R$ 28.000,00",
                "numero_convidados": 95
            },
            {
                "noivo1": {"nome": "Gabriel Souza", "email": "gabriel.souza@email.com", "telefone": "(51) 95444-3322", "cpf": "567.890.123-45"},
                "noiva1": {"nome": "Isabela Martins", "email": "isabela.martins@email.com", "telefone": "(51) 95444-3323", "cpf": "543.210.987-45"},
                "data_casamento": "2025-01-18",
                "local_previsto": "Vinícola Casa Valduga - Bento Gonçalves/RS",
                "orcamento_estimado": "R$ 55.000,00",
                "numero_convidados": 140
            },
            {
                "noivo1": {"nome": "Thiago Alves", "email": "thiago.alves@email.com", "telefone": "(61) 94333-2211", "cpf": "678.901.234-56"},
                "noiva1": {"nome": "Fernanda Castro", "email": "fernanda.castro@email.com", "telefone": "(61) 94333-2212", "cpf": "432.109.876-56"},
                "data_casamento": "2024-10-25",
                "local_previsto": "Espaço Villa Regia - Brasília/DF",
                "orcamento_estimado": "R$ 40.000,00",
                "numero_convidados": 110
            },
            {
                "noivo1": {"nome": "Bruno Pereira", "email": "bruno.pereira@email.com", "telefone": "(85) 93222-1100", "cpf": "789.012.345-67"},
                "noiva1": {"nome": "Larissa Gomes", "email": "larissa.gomes@email.com", "telefone": "(85) 93222-1101", "cpf": "321.098.765-67"},
                "data_casamento": "2025-05-10",
                "local_previsto": "Beach Park Resort - Fortaleza/CE",
                "orcamento_estimado": "R$ 60.000,00",
                "numero_convidados": 160
            },
            {
                "noivo1": {"nome": "Diego Santos", "email": "diego.santos@email.com", "telefone": "(71) 92111-0099", "cpf": "890.123.456-78"},
                "noiva1": {"nome": "Natália Silva", "email": "natalia.silva@email.com", "telefone": "(71) 92111-0100", "cpf": "210.987.654-78"},
                "data_casamento": "2025-04-05",
                "local_previsto": "Pelourinho - Salvador/BA",
                "orcamento_estimado": "R$ 38.000,00",
                "numero_convidados": 85
            },
            {
                "noivo1": {"nome": "Rodrigo Costa", "email": "rodrigo.costa@email.com", "telefone": "(62) 91000-9988", "cpf": "901.234.567-89"},
                "noiva1": {"nome": "Beatriz Ribeiro", "email": "beatriz.ribeiro@email.com", "telefone": "(62) 91000-9989", "cpf": "109.876.543-89"},
                "data_casamento": "2024-12-28",
                "local_previsto": "Clube Jaó - Goiânia/GO",
                "orcamento_estimado": "R$ 32.000,00",
                "numero_convidados": 75
            },
            {
                "noivo1": {"nome": "Leonardo Barbosa", "email": "leonardo.barbosa@email.com", "telefone": "(47) 90999-8877", "cpf": "012.345.678-90"},
                "noiva1": {"nome": "Priscila Moreira", "email": "priscila.moreira@email.com", "telefone": "(47) 90999-8878", "cpf": "098.765.432-90"},
                "data_casamento": "2025-06-20",
                "local_previsto": "Vila Germânica - Blumenau/SC",
                "orcamento_estimado": "R$ 42.000,00",
                "numero_convidados": 130
            }
        ]

        print("💑 Criando casais de teste...")

        for casal_data in casais_dados:
            # Criar usuário noivo1
            senha_hash = criar_hash_senha("123456")

            noivo1 = Usuario(
                id=0,
                nome=casal_data["noivo1"]["nome"],
                cpf=casal_data["noivo1"]["cpf"],
                data_nascimento="1995-01-15",  # Data padrão
                email=casal_data["noivo1"]["email"],
                telefone=casal_data["noivo1"]["telefone"],
                senha=senha_hash,
                perfil=TipoUsuario.NOIVO,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            noivo1_id = usuario_repo.inserir_usuario(noivo1)

            if not noivo1_id:
                print(f"❌ Erro ao criar noivo {casal_data['noivo1']['nome']}")
                continue

            # Criar usuário noiva1 (noivo2)
            noiva1 = Usuario(
                id=0,
                nome=casal_data["noiva1"]["nome"],
                cpf=casal_data["noiva1"]["cpf"],
                data_nascimento="1996-05-20",  # Data padrão
                email=casal_data["noiva1"]["email"],
                telefone=casal_data["noiva1"]["telefone"],
                senha=senha_hash,
                perfil=TipoUsuario.NOIVO,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            noiva1_id = usuario_repo.inserir_usuario(noiva1)

            if not noiva1_id:
                print(f"❌ Erro ao criar noiva {casal_data['noiva1']['nome']}")
                continue

            # Criar casal
            casal = Casal(
                id=0,
                id_noivo1=noivo1_id,
                id_noivo2=noiva1_id,
                data_casamento=casal_data["data_casamento"],
                local_previsto=casal_data["local_previsto"],
                orcamento_estimado=casal_data["orcamento_estimado"],
                numero_convidados=casal_data["numero_convidados"],
                data_cadastro=None
            )

            casal_id = casal_repo.inserir_casal(casal)

            if casal_id:
                print(f"✅ Casal '{casal_data['noivo1']['nome']} & {casal_data['noiva1']['nome']}' criado com sucesso! ID: {casal_id}")
                print(f"   📅 Casamento: {casal_data['data_casamento']} | 👥 Convidados: {casal_data['numero_convidados']} | 💰 Orçamento: {casal_data['orcamento_estimado']}")
            else:
                print(f"❌ Erro ao criar casal {casal_data['noivo1']['nome']} & {casal_data['noiva1']['nome']}")

        print("✅ Casais de teste criados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar casais de teste: {e}")

def inicializar_sistema():
    """
    Inicializa o sistema executando todas as verificações e configurações necessárias.
    """
    print("🚀 Inicializando sistema CaseBem...")

    # Criar todas as tabelas necessárias
    criar_tabelas_banco()

    # Executar migração do sistema de avatar
    migrar_sistema_avatar()

    # Criar administrador padrão se necessário
    criar_admin_padrao()

    # Criar categorias padrão se necessário
    criar_categorias()

    # Criar fornecedores de exemplo se necessário
    criar_fornecedores_inteligente()

    # Criar casais de teste se necessário
    criar_casais_exemplo()

    print("✅ Sistema inicializado com sucesso!")