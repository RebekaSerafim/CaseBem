from typing import Optional, List
from util.database import obter_conexao
from sql.usuario_sql import *
from model.usuario_model import TipoUsuario, Usuario

def criar_tabela_usuarios() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_USUARIO)

            # Tenta adicionar a coluna 'ativo' se ainda não existir
            try:
                cursor.execute(ADICIONAR_COLUNA_ATIVO)
            except Exception:
                # Coluna já existe, ignorar erro
                pass

            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False
   

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir usuário com todos os campos
        cursor.execute(INSERIR_USUARIO,
            (usuario.nome, usuario.cpf, usuario.data_nascimento, usuario.email, usuario.telefone, usuario.senha, usuario.perfil.value))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_USUARIO,
            (usuario.nome, usuario.cpf, usuario.data_nascimento, usuario.telefone, usuario.email, usuario.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar senha do usuário
        cursor.execute(ATUALIZAR_SENHA_USUARIO, (senha_hash, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_USUARIO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_USUARIO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                ativo=bool(resultado["ativo"]))
    # Retorna None se não encontrou usuário
    return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo email
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                ativo=bool(resultado["ativo"]))
    # Retorna None se não encontrou usuário
    return None

def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_USUARIOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            cpf=resultado["cpf"],
            data_nascimento=resultado["data_nascimento"],
            email=resultado["email"],
            telefone=resultado["telefone"],
            senha=resultado["senha"],
            perfil=TipoUsuario(resultado["perfil"]),
            token_redefinicao=resultado["token_redefinicao"],
            data_token=resultado["data_token"],
            data_cadastro=resultado["data_cadastro"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []


def obter_usuarios_por_tipo_por_pagina(tipo: TipoUsuario, numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários por tipo com paginação
        cursor.execute(OBTER_USUARIOS_POR_TIPO_POR_PAGINA, (tipo.value, limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            cpf=resultado["cpf"],
            data_nascimento=resultado["data_nascimento"],
            email=resultado["email"],
            telefone=resultado["telefone"],
            senha=resultado["senha"],
            perfil=TipoUsuario(resultado["perfil"]),
            token_redefinicao=resultado["token_redefinicao"],
            data_token=resultado["data_token"],
            data_cadastro=resultado["data_cadastro"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []

def contar_usuarios() -> int:
    """Conta o total de usuários no sistema"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_USUARIOS)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar usuários: {e}")
        return 0

def contar_usuarios_por_tipo(tipo: TipoUsuario) -> int:
    """Conta o total de usuários de um tipo específico"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_USUARIOS_POR_TIPO, (tipo.value,))
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar usuários por tipo: {e}")
        return 0

def buscar_usuarios(busca: str = "", tipo_usuario: str = "", status: str = "", numero_pagina: int = 1, tamanho_pagina: int = 100) -> List[Usuario]:
    """Busca usuários com filtros de nome/email, tipo e status"""
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            cursor = conexao.cursor()
            cursor.execute(BUSCAR_USUARIOS, (busca, busca, busca, tipo_usuario, tipo_usuario, status, status, status, limite, offset))
            resultados = cursor.fetchall()
            return [Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                ativo=bool(resultado["ativo"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return []

def bloquear_usuario(id_usuario: int) -> bool:
    """Bloqueia (desativa) um usuário"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(BLOQUEAR_USUARIO, (id_usuario,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao bloquear usuário: {e}")
        return False

def ativar_usuario(id_usuario: int) -> bool:
    """Ativa um usuário"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATIVAR_USUARIO, (id_usuario,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao ativar usuário: {e}")
        return False

def obter_usuarios_paginado(pagina: int, tamanho_pagina: int) -> tuple[list[Usuario], int]:
    """Obtém usuários paginados e retorna lista de usuários e total"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Contar total de usuários
            cursor.execute("SELECT COUNT(*) as total FROM usuario")
            total = cursor.fetchone()["total"]

            # Buscar usuários da página
            offset = (pagina - 1) * tamanho_pagina
            cursor.execute(OBTER_USUARIOS_POR_PAGINA, (tamanho_pagina, offset))
            resultados = cursor.fetchall()

            usuarios = [Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                ativo=bool(resultado["ativo"])
            ) for resultado in resultados]

            return usuarios, total
    except Exception as e:
        print(f"Erro ao obter usuários paginados: {e}")
        return [], 0

def buscar_usuarios_paginado(busca: str = "", tipo_usuario: str = "", status: str = "", pagina: int = 1, tamanho_pagina: int = 10) -> tuple[list[Usuario], int]:
    """Busca usuários paginados com filtros e retorna lista de usuários e total"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()

            # Construir consulta baseada nos filtros
            condicoes = []
            parametros = []
            parametros_count = []

            if busca:
                condicoes.append("(nome LIKE ? OR email LIKE ?)")
                busca_param = f"%{busca}%"
                parametros.extend([busca_param, busca_param])
                parametros_count.extend([busca_param, busca_param])

            if tipo_usuario:
                condicoes.append("perfil = ?")
                parametros.append(tipo_usuario)
                parametros_count.append(tipo_usuario)

            if status == "ativo":
                condicoes.append("ativo = 1")
            elif status == "inativo":
                condicoes.append("ativo = 0")

            where_clause = ""
            if condicoes:
                where_clause = "WHERE " + " AND ".join(condicoes)

            # Contar total
            sql_count = f"SELECT COUNT(*) as total FROM usuario {where_clause}"
            cursor.execute(sql_count, parametros_count)
            total = cursor.fetchone()["total"]

            # Buscar usuários da página
            offset = (pagina - 1) * tamanho_pagina
            sql_select = f"SELECT * FROM usuario {where_clause} ORDER BY id DESC LIMIT ? OFFSET ?"
            parametros.extend([tamanho_pagina, offset])
            cursor.execute(sql_select, parametros)
            resultados = cursor.fetchall()

            usuarios = [Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                ativo=bool(resultado["ativo"])
            ) for resultado in resultados]

            return usuarios, total
    except Exception as e:
        print(f"Erro ao buscar usuários paginados: {e}")
        return [], 0
