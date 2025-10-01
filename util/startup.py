from typing import Optional
import json
import os
from core.models.usuario_model import Usuario, TipoUsuario
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.models.fornecedor_model import Fornecedor
from core.models.casal_model import Casal
from core.repositories import usuario_repo, fornecedor_repo, casal_repo, item_repo, categoria_repo, fornecedor_item_repo, item_demanda_repo, item_orcamento_repo, demanda_repo, orcamento_repo, favorito_repo, chat_repo
from infrastructure.security import criar_hash_senha
from util.migracoes_avatar import migrar_sistema_avatar

def criar_tabelas_banco():
    """
    Cria todas as tabelas necessárias no banco de dados.
    """
    usuario_repo.criar_tabela()
    fornecedor_repo.criar_tabela()
    casal_repo.criar_tabela()
    item_repo.criar_tabela()
    categoria_repo.criar_tabela()
    fornecedor_item_repo.criar_tabela()
    demanda_repo.criar_tabela()
    orcamento_repo.criar_tabela()
    item_demanda_repo.criar_tabela()
    item_orcamento_repo.criar_tabela()
    favorito_repo.criar_tabela()
    chat_repo.criar_tabela()

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
            cpf="000.000.000-00",
            data_nascimento="1990-01-01",
            email="admin@casebem.com",
            telefone="(28) 99999-0000",
            senha=senha_hash,
            perfil=TipoUsuario.ADMIN,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )

        admin_id = usuario_repo.inserir(admin)

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

def carregar_dados_json(nome_arquivo: str) -> dict:
    """
    Carrega dados de um arquivo JSON na pasta data/.
    """
    try:
        caminho_arquivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"❌ Arquivo {nome_arquivo} não encontrado na pasta data/")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar JSON do arquivo {nome_arquivo}")
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo {nome_arquivo}: {e}")
        return {}

def criar_categorias():
    """
    Cria categorias padrão para casamentos se não existirem no sistema.
    Utiliza dados do arquivo data/categorias.json com IDs explícitos.
    """
    try:
        # Verificar se já existem categorias
        categorias_existentes = categoria_repo.listar_todos()
        if categorias_existentes:
            print("✅ Categorias já existem no sistema")
            return

        # Carregar dados das categorias do arquivo JSON
        dados_categorias = carregar_dados_json('categorias.json')
        if not dados_categorias or 'categorias' not in dados_categorias:
            print("❌ Não foi possível carregar os dados das categorias")
            return

        lista_categorias = dados_categorias['categorias']

        # Inserir categorias com IDs explícitos
        from infrastructure.database import obter_conexao
        from core.sql import categoria_sql

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            for cat_data in lista_categorias:
                # Mapear string do tipo para enum
                tipo_item = getattr(TipoFornecimento, cat_data['tipo'])

                # Inserir com ID explícito
                cursor.execute(
                    categoria_sql.INSERIR_COM_ID,
                    (
                        cat_data['id'],
                        cat_data['nome'],
                        tipo_item.value,
                        cat_data['descricao'],
                        1  # ativo
                    )
                )
                print(f"✅ Categoria ID {cat_data['id']} '{cat_data['nome']}' criada com sucesso")

        print(f"✅ {len(lista_categorias)} categorias padrão criadas com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar categorias padrão: {e}")

def criar_fornecedores():
    """
    Cria fornecedores de teste com distribuição inteligente de itens por categoria.
    Utiliza IDs explícitos do JSON para preservar compatibilidade com fotos.
    """
    try:
        # Verificar se já existem fornecedores
        total_fornecedores = fornecedor_repo.contar()
        if total_fornecedores >= 10:
            print("✅ Fornecedores de teste já existem no sistema")
            return

        # Obter categorias
        categorias = categoria_repo.listar_todos()
        if not categorias:
            print("❌ Nenhuma categoria encontrada. Execute criar_categorias() primeiro.")
            return

        # Carregar itens do JSON com IDs explícitos
        dados_itens = carregar_dados_json('itens.json')
        if not dados_itens or 'itens' not in dados_itens:
            print("❌ Não foi possível carregar os dados dos itens")
            return

        lista_itens = dados_itens['itens']

        # Carregar fornecedores base do arquivo JSON
        fornecedores_base = carregar_dados_json('fornecedores.json')
        if not fornecedores_base:
            print("❌ Não foi possível carregar os dados dos fornecedores básicos")
            return

        print("🏢 Criando fornecedores com distribuição determinística de itens...")

        # Agrupar itens por categoria (mantendo ordem do JSON)
        itens_por_categoria = {}
        for item_data in lista_itens:
            cat_id = item_data['id_categoria']
            if cat_id not in itens_por_categoria:
                itens_por_categoria[cat_id] = []
            itens_por_categoria[cat_id].append(item_data)

        # Distribuir categorias entre fornecedores de forma determinística
        categorias_ids = sorted(itens_por_categoria.keys())  # Ordem determinística

        categorias_por_fornecedor = []
        for i in range(len(fornecedores_base)):
            categorias_por_fornecedor.append([])

        # Distribuir categorias garantindo que cada fornecedor tenha pelo menos uma
        for i, categoria_id in enumerate(categorias_ids):
            fornecedor_idx = i % len(fornecedores_base)
            categorias_por_fornecedor[fornecedor_idx].append(categoria_id)

        # Importar módulos necessários
        from infrastructure.database import obter_conexao
        from core.sql import item_sql

        # Criar fornecedores e seus itens
        for i, fornecedor_data in enumerate(fornecedores_base):
            # Criar fornecedor
            senha_hash = criar_hash_senha("1234aA@#")

            fornecedor = Fornecedor(
                id=0,
                nome=fornecedor_data["nome"],
                cpf=fornecedor_data.get("cpf"),
                data_nascimento=fornecedor_data.get("data_nascimento"),
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
                verificado=True
            )

            fornecedor_id = fornecedor_repo.inserir(fornecedor)

            if fornecedor_id:
                print(f"✅ Fornecedor '{fornecedor.nome_empresa}' criado com sucesso! ID: {fornecedor_id}")

                # Criar itens para as categorias deste fornecedor com IDs explícitos
                total_itens = 0
                with obter_conexao() as conexao:
                    cursor = conexao.cursor()

                    for categoria_id in categorias_por_fornecedor[i]:
                        categoria = next((c for c in categorias if c.id == categoria_id), None)
                        if categoria and categoria_id in itens_por_categoria:
                            for item_data in itens_por_categoria[categoria_id]:
                                # Inserir item com ID explícito
                                cursor.execute(
                                    item_sql.INSERIR_COM_ID,
                                    (
                                        item_data['id'],
                                        fornecedor_id,
                                        categoria.tipo_fornecimento.value,
                                        item_data['nome'],
                                        item_data['descricao'],
                                        item_data['preco'],
                                        item_data['id_categoria'],
                                        None,  # observacoes
                                        1  # ativo
                                    )
                                )
                                print(f"  ✅ Item ID {item_data['id']} '{item_data['nome']}' criado - R$ {item_data['preco']:.2f}")
                                total_itens += 1

                print(f"  📦 Total de {total_itens} itens criados para {fornecedor.nome_empresa}")
            else:
                print(f"❌ Erro ao criar fornecedor '{fornecedor_data['empresa']}'")

        print("✅ Fornecedores e itens criados com IDs fixos!")

    except Exception as e:
        print(f"❌ Erro ao criar fornecedores: {e}")

def criar_itens():
    """
    Carrega os templates de itens do arquivo JSON.
    """
    return carregar_dados_json('itens.json')

def criar_casais():
    """
    Cria 10 casais fictícios para teste com dados realistas.
    """
    try:
        # Verificar se já existem casais
        casais_existentes = casal_repo.obter_por_pagina(1, 20)
        if len(casais_existentes) >= 10:
            print("✅ Casais de teste já existem no sistema")
            return

        # Carregar dados dos casais do arquivo JSON
        casais_dados = carregar_dados_json('casais.json')
        if not casais_dados:
            print("❌ Não foi possível carregar os dados dos casais")
            return

        print("💑 Criando casais de teste...")

        for casal_data in casais_dados:
            # Criar usuário noivo1
            senha_hash = criar_hash_senha("1234aA@#")

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

            noivo1_id = usuario_repo.inserir(noivo1)

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

            noiva1_id = usuario_repo.inserir(noiva1)

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

            casal_id = casal_repo.inserir(casal)

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

    # Criar administrador padrão se necessário
    criar_admin_padrao()

    # Criar categorias padrão se necessário
    criar_categorias()

    # Criar fornecedores de exemplo se necessário
    criar_fornecedores()

    # Criar casais de teste se necessário
    criar_casais()

    print("✅ Sistema inicializado com sucesso!")