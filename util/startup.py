from typing import Optional
import json
import os
from core.models.usuario_model import Usuario, TipoUsuario
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.models.fornecedor_model import Fornecedor
from core.models.casal_model import Casal
from core.repositories import usuario_repo, fornecedor_repo, casal_repo, item_repo, categoria_repo, fornecedor_item_repo, item_demanda_repo, item_orcamento_repo, demanda_repo, orcamento_repo, favorito_repo, chat_repo
from infrastructure.security import criar_hash_senha
from infrastructure.logging import logger

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
    Cria o administrador padrão se não existir.
    Esta função SEMPRE é executada na inicialização do sistema.
    Retorna o ID do admin criado ou existente.
    """
    try:
        # Verificar se já existe admin
        admin_existente = usuario_repo.obter_usuario_por_email("admin@casebem.com")
        if admin_existente:
            logger.info("Administrador já existe no sistema")
            return admin_existente.id

        # Criar administrador padrão
        logger.info("Criando administrador padrão...")

        from infrastructure.database import obter_conexao

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Inserir admin com ID fixo = 1
            cursor.execute(
                """INSERT INTO usuario (id, nome, cpf, data_nascimento, email, telefone, senha, perfil, ativo, token_redefinicao, data_token, data_cadastro)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
                (
                    1,  # ID fixo
                    "Administrador Padrão",
                    "000.000.000-00",
                    "1900-01-01",
                    "admin@casebem.com",
                    "(28) 99999-0000",
                    criar_hash_senha("1234aA@#"),
                    TipoUsuario.ADMIN.value,
                    1,  # ativo
                    None,  # token_redefinicao
                    None   # data_token
                )
            )

        logger.info("Administrador padrão criado com sucesso! ID: 1")
        logger.info("Email: admin@casebem.com | Senha: 1234aA@#")
        logger.warning("IMPORTANTE: Altere a senha no primeiro login!")
        return 1

    except Exception as e:
        logger.error(f"Erro ao verificar/criar administrador: {e}")
        return None

def criar_usuarios_seed():
    """
    Importa usuários (noivos) do arquivo seeds/usuarios.json se não existirem.
    Esta função é opcional e só executa se o arquivo JSON existir.
    """
    try:
        # Verificar se já existem usuários noivos (não conta admin)
        from infrastructure.database import obter_conexao

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE perfil = 'NOIVO'")
            total_noivos = cursor.fetchone()[0]

            if total_noivos > 0:
                logger.info("Usuários noivos já existem no sistema")
                return

        # Carregar dados dos usuários do arquivo JSON
        usuarios_dados = carregar_dados_json('usuarios.json')
        if not usuarios_dados:
            logger.info("Arquivo usuarios.json não encontrado - pulando seed de usuários")
            return

        logger.info("Importando usuários noivos do seed...")

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            for user_data in usuarios_dados:
                # Inserir usuário com ID explícito
                cursor.execute(
                    """INSERT INTO usuario (id, nome, cpf, data_nascimento, email, telefone, senha, perfil, ativo, token_redefinicao, data_token, data_cadastro)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        user_data['id'],
                        user_data['nome'],
                        user_data['cpf'],
                        user_data['data_nascimento'],
                        user_data['email'],
                        user_data['telefone'],
                        user_data['senha'],
                        user_data['perfil'],
                        1,  # ativo
                        user_data.get('token_redefinicao'),
                        user_data.get('data_token'),
                        user_data.get('data_cadastro')
                    )
                )
                logger.debug(f"Usuário ID {user_data['id']} '{user_data['nome']}' importado")

        logger.info(f"{len(usuarios_dados)} usuários noivos importados com sucesso!")
        logger.warning("IMPORTANTE: Altere as senhas padrão dos usuários de teste!")

    except Exception as e:
        logger.error(f"Erro ao importar usuários: {e}")

def carregar_dados_json(nome_arquivo: str) -> dict:
    """
    Carrega dados de um arquivo JSON na pasta data/seeds/.
    """
    try:
        caminho_arquivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'seeds', nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        logger.error(f"Arquivo {nome_arquivo} não encontrado na pasta data/seeds/")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Erro ao decodificar JSON do arquivo {nome_arquivo}")
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo {nome_arquivo}: {e}")
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
            logger.info("Categorias já existem no sistema")
            return

        # Carregar dados das categorias do arquivo JSON
        dados_categorias = carregar_dados_json('categorias.json')
        if not dados_categorias or 'categorias' not in dados_categorias:
            logger.error("Não foi possível carregar os dados das categorias")
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
                logger.info(f"Categoria ID {cat_data['id']} '{cat_data['nome']}' criada com sucesso")

        logger.info(f"{len(lista_categorias)} categorias padrão criadas com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao criar categorias padrão: {e}")

def criar_fornecedores_seed():
    """
    Importa fornecedores do arquivo seeds/fornecedores.json se não existirem.
    Os dados de usuário do fornecedor são inseridos na tabela usuario primeiro.
    """
    try:
        # Verificar se já existem fornecedores
        total_fornecedores = fornecedor_repo.contar()
        if total_fornecedores >= 10:
            logger.info("Fornecedores já existem no sistema")
            return

        # Carregar dados dos fornecedores do arquivo JSON
        fornecedores_dados = carregar_dados_json('fornecedores.json')
        if not fornecedores_dados:
            logger.error("Não foi possível carregar os dados dos fornecedores")
            return

        logger.info("Importando fornecedores do seed...")

        from infrastructure.database import obter_conexao

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            for forn_data in fornecedores_dados:
                # Primeiro, inserir ou atualizar na tabela usuario
                cursor.execute(
                    """INSERT OR REPLACE INTO usuario (id, nome, cpf, data_nascimento, email, telefone, senha, perfil, ativo, token_redefinicao, data_token, data_cadastro)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        forn_data['id'],
                        forn_data['nome'],
                        forn_data['cpf'],
                        forn_data['data_nascimento'],
                        forn_data['email'],
                        forn_data['telefone'],
                        forn_data['senha'],
                        forn_data['perfil'],
                        forn_data['ativo'],
                        None,  # token_redefinicao
                        None,  # data_token
                        forn_data.get('data_cadastro')
                    )
                )

                # Depois, inserir na tabela fornecedor
                cursor.execute(
                    """INSERT INTO fornecedor (id, nome_empresa, cnpj, descricao, verificado)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        forn_data['id'],
                        forn_data['nome_empresa'],
                        forn_data['cnpj'],
                        forn_data['descricao'],
                        forn_data['verificado']
                    )
                )
                logger.debug(f"Fornecedor ID {forn_data['id']} '{forn_data['nome_empresa']}' importado")

        logger.info(f"{len(fornecedores_dados)} fornecedores importados com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao importar fornecedores: {e}")

def criar_itens_seed():
    """
    Importa itens do arquivo seeds/itens.json se não existirem.
    Os itens são distribuídos entre fornecedores com base em suas categorias.
    """
    try:
        # Verificar se já existem itens ativos
        from infrastructure.database import obter_conexao
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM item WHERE ativo = 1")
            total_itens = cursor.fetchone()[0]

        if total_itens >= 80:
            logger.info(f"Itens já existem no sistema ({total_itens} ativos)")
            return

        # Carregar dados de itens e categorias
        itens_json = carregar_dados_json('itens.json')
        if not itens_json or 'itens' not in itens_json:
            logger.error("Não foi possível carregar os dados dos itens")
            return

        itens_dados = itens_json['itens']

        # Carregar categorias para obter o tipo (PRODUTO/SERVICO/ESPACO)
        categorias_json = carregar_dados_json('categorias.json')
        if not categorias_json or 'categorias' not in categorias_json:
            logger.error("Não foi possível carregar as categorias")
            return

        # Criar mapa id_categoria -> tipo (normalizando para o formato do banco)
        def normalizar_tipo(tipo: str) -> str:
            """Normaliza tipo para o formato esperado pelo banco (com acentos)"""
            tipo_map = {
                'SERVICO': 'SERVIÇO',
                'ESPACO': 'ESPAÇO',
                'PRODUTO': 'PRODUTO'
            }
            return tipo_map.get(tipo.upper(), tipo)

        categoria_tipo_map = {cat['id']: normalizar_tipo(cat['tipo']) for cat in categorias_json['categorias']}

        logger.info(f"Importando {len(itens_dados)} itens do seed...")

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            for item_data in itens_dados:
                # Obter tipo da categoria (já normalizado com acentos)
                tipo = categoria_tipo_map.get(item_data['id_categoria'], 'PRODUTO')

                # Inserir item com ID explícito (compatibilidade com fotos)
                cursor.execute(
                    """INSERT INTO item (id, id_fornecedor, tipo, nome, descricao, preco, id_categoria, observacoes, ativo)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        item_data['id'],
                        item_data['id_fornecedor'],
                        tipo,
                        item_data['nome'],
                        item_data['descricao'],
                        item_data['preco'],
                        item_data['id_categoria'],
                        None,  # observacoes
                        1      # ativo
                    )
                )
                logger.debug(f"Item ID {item_data['id']} '{item_data['nome']}' importado (Fornecedor {item_data['id_fornecedor']})")

        logger.info(f"{len(itens_dados)} itens importados com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao importar itens: {e}")

def criar_casais_seed():
    """
    Importa casais do arquivo seeds/casais.json se não existirem.
    """
    try:
        # Verificar se já existem casais
        casais_existentes = casal_repo.obter_por_pagina(1, 20)
        if len(casais_existentes) >= 10:
            logger.info("Casais já existem no sistema")
            return

        # Carregar dados dos casais do arquivo JSON
        casais_dados = carregar_dados_json('casais.json')
        if not casais_dados:
            logger.error("Não foi possível carregar os dados dos casais")
            return

        logger.info("Importando casais do seed...")

        from infrastructure.database import obter_conexao

        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            for casal_data in casais_dados:
                # Inserir casal com ID explícito
                cursor.execute(
                    """INSERT INTO casal (id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados, data_cadastro)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        casal_data['id'],
                        casal_data['id_noivo1'],
                        casal_data['id_noivo2'],
                        casal_data['data_casamento'],
                        casal_data['local_previsto'],
                        casal_data['orcamento_estimado'],
                        casal_data['numero_convidados'],
                        casal_data.get('data_cadastro')
                    )
                )
                logger.debug(f"Casal ID {casal_data['id']} importado - {casal_data['data_casamento']}")

        logger.info(f"{len(casais_dados)} casais importados com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao importar casais: {e}")

def inicializar_sistema():
    """
    Inicializa o sistema executando todas as verificações e configurações necessárias.

    Ordem de execução:
    1. Criar tabelas
    2. Criar admin padrão (SEMPRE executa)
    3. Criar categorias padrão
    4. Importar usuários de teste (OPCIONAL - seeds/usuarios.json)
    5. Importar fornecedores (OPCIONAL - seeds/fornecedores.json)
    6. Importar itens (OPCIONAL - seeds/itens.json)
    7. Importar casais (OPCIONAL - seeds/casais.json)
    """
    logger.info("Inicializando sistema CaseBem...")

    # Criar todas as tabelas necessárias
    criar_tabelas_banco()

    # Criar administrador padrão (SEMPRE executa, independente de seeds)
    criar_admin_padrao()

    # Criar categorias padrão se necessário
    criar_categorias()

    # Importar usuários noivos de teste (OPCIONAL)
    criar_usuarios_seed()

    # Importar fornecedores de exemplo (OPCIONAL)
    criar_fornecedores_seed()

    # Importar itens de exemplo (OPCIONAL - após fornecedores)
    criar_itens_seed()

    # Importar casais de teste (OPCIONAL)
    criar_casais_seed()

    logger.info("Sistema inicializado com sucesso!")