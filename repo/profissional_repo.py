from typing import Optional, List
from util.database import obter_conexao
from sql.profissional_sql import *
from model.profissional_model import Profissional
from model.usuario_model import TipoUsuario
from repo import usuario_repo

def criar_tabela_profissional() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_PROFISSIONAL)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela profissional: {e}")
        return False

def inserir_profissional(profissional: Profissional) -> Optional[int]:
    try:
        # Primeiro inserir na tabela usuario
        usuario_id = usuario_repo.inserir_usuario(profissional)

        if usuario_id:
            # Depois inserir na tabela profissional
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(INSERIR_PROFISSIONAL,
                    (usuario_id, profissional.nome_empresa, profissional.cnpj,
                     profissional.descricao, profissional.prestador,
                     profissional.fornecedor, profissional.locador))
                return usuario_id
    except Exception as e:
        print(f"Erro ao inserir profissional: {e}")
    return None

def atualizar_profissional(profissional: Profissional) -> bool:
    try:
        # Atualizar dados de usuario
        usuario_repo.atualizar_usuario(profissional)

        # Atualizar dados específicos de profissional
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_PROFISSIONAL,
                (profissional.nome_empresa, profissional.cnpj, profissional.descricao,
                 profissional.prestador, profissional.fornecedor, profissional.locador,
                 profissional.id))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar profissional: {e}")
        return False

def excluir_profissional(id: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            # Primeiro excluir da tabela profissional
            cursor.execute(EXCLUIR_PROFISSIONAL, (id,))
            # Depois excluir da tabela usuario na mesma conexão
            cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir profissional: {e}")
        return False

def obter_profissional_por_id(id: int) -> Optional[Profissional]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_PROFISSIONAL_POR_ID, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return Profissional(
                    # Campos de Usuario na ordem correta
                    id=resultado["id"],
                    nome=resultado["nome"],
                    cpf=resultado["cpf"],
                    data_nascimento=resultado["data_nascimento"],
                    email=resultado["email"],
                    telefone=resultado["telefone"],
                    senha=resultado["senha"],
                    perfil=TipoUsuario.PROFISSIONAL,
                    foto=resultado["foto"],
                    token_redefinicao=resultado["token_redefinicao"],
                    data_token=resultado["data_token"],
                    data_cadastro=resultado["data_cadastro"],
                    # Campos específicos de Profissional
                    nome_empresa=resultado["nome_empresa"],
                    cnpj=resultado["cnpj"],
                    descricao=resultado["descricao"],
                    prestador=bool(resultado["prestador"]),
                    fornecedor=bool(resultado["fornecedor"]),
                    locador=bool(resultado["locador"])
                )
    except Exception as e:
        print(f"Erro ao obter profissional por ID: {e}")
    return None

def obter_profissionais_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Profissional]:
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            cursor = conexao.cursor()
            cursor.execute(OBTER_PROFISSIONAIS_POR_PAGINA, (limite, offset))
            resultados = cursor.fetchall()

            return [Profissional(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.PROFISSIONAL,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Profissional
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                fornecedor=bool(resultado["fornecedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter profissionais por página: {e}")
    return []

def obter_prestadores() -> List[Profissional]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_PRESTADORES)
            resultados = cursor.fetchall()

            return [Profissional(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.PROFISSIONAL,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Profissional
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                fornecedor=bool(resultado["fornecedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter prestadores: {e}")
    return []

def obter_fornecedores() -> List[Profissional]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_FORNECEDORES)
            resultados = cursor.fetchall()

            return [Profissional(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.PROFISSIONAL,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Profissional
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                fornecedor=bool(resultado["fornecedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter fornecedores: {e}")
    return []

def obter_locadores() -> List[Profissional]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_LOCADORES)
            resultados = cursor.fetchall()

            return [Profissional(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.PROFISSIONAL,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Profissional
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                fornecedor=bool(resultado["fornecedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter locadores: {e}")
    return []