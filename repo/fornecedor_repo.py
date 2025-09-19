from typing import Optional, List
from util.database import obter_conexao
from sql.fornecedor_sql import *
from model.fornecedor_model import Fornecedor
from model.usuario_model import TipoUsuario
from repo import usuario_repo

def criar_tabela_fornecedor() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_FORNECEDOR)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela fornecedor: {e}")
        return False

def inserir_fornecedor(fornecedor: Fornecedor) -> Optional[int]:
    try:
        # Primeiro inserir na tabela usuario
        usuario_id = usuario_repo.inserir_usuario(fornecedor)

        if usuario_id:
            # Depois inserir na tabela fornecedor
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(INSERIR_FORNECEDOR,
                    (usuario_id, fornecedor.nome_empresa, fornecedor.cnpj,
                     fornecedor.descricao, fornecedor.prestador,
                     fornecedor.vendedor, fornecedor.locador,
                     fornecedor.verificado, fornecedor.data_verificacao))
                return usuario_id
    except Exception as e:
        print(f"Erro ao inserir fornecedor: {e}")
    return None

def atualizar_fornecedor(fornecedor: Fornecedor) -> bool:
    try:
        # Atualizar dados de usuario
        usuario_repo.atualizar_usuario(fornecedor)

        # Atualizar dados específicos de fornecedor
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_FORNECEDOR,
                (fornecedor.nome_empresa, fornecedor.cnpj, fornecedor.descricao,
                 fornecedor.prestador, fornecedor.vendedor, fornecedor.locador,
                 fornecedor.verificado, fornecedor.data_verificacao,
                 fornecedor.id))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar fornecedor: {e}")
        return False

def excluir_fornecedor(id: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            # Primeiro excluir da tabela fornecedor
            cursor.execute(EXCLUIR_FORNECEDOR, (id,))
            # Depois excluir da tabela usuario na mesma conexão
            cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir fornecedor: {e}")
        return False

def obter_fornecedor_por_id(id: int) -> Optional[Fornecedor]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_FORNECEDOR_POR_ID, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return Fornecedor(
                    # Campos de Usuario na ordem correta
                    id=resultado["id"],
                    nome=resultado["nome"],
                    cpf=resultado["cpf"],
                    data_nascimento=resultado["data_nascimento"],
                    email=resultado["email"],
                    telefone=resultado["telefone"],
                    senha=resultado["senha"],
                    perfil=TipoUsuario.FORNECEDOR,
                    foto=resultado["foto"],
                    token_redefinicao=resultado["token_redefinicao"],
                    data_token=resultado["data_token"],
                    data_cadastro=resultado["data_cadastro"],
                    # Campos específicos de Fornecedor
                    nome_empresa=resultado["nome_empresa"],
                    cnpj=resultado["cnpj"],
                    descricao=resultado["descricao"],
                    prestador=bool(resultado["prestador"]),
                    vendedor=bool(resultado["vendedor"]),
                    locador=bool(resultado["locador"]),
                    verificado=bool(resultado["verificado"]),
                    data_verificacao=resultado["data_verificacao"]
                )
    except Exception as e:
        print(f"Erro ao obter fornecedor por ID: {e}")
    return None

def obter_fornecedores_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Fornecedor]:
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            cursor = conexao.cursor()
            cursor.execute(OBTER_FORNECEDORES_POR_PAGINA, (limite, offset))
            resultados = cursor.fetchall()

            return [Fornecedor(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.FORNECEDOR,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Fornecedor
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                vendedor=bool(resultado["vendedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter fornecedores por página: {e}")
    return []

def obter_prestadores() -> List[Fornecedor]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_PRESTADORES)
            resultados = cursor.fetchall()

            return [Fornecedor(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.FORNECEDOR,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Fornecedor
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                vendedor=bool(resultado["vendedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter prestadores: {e}")
    return []

def obter_vendedores() -> List[Fornecedor]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_VENDEDORES)
            resultados = cursor.fetchall()

            return [Fornecedor(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.FORNECEDOR,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Fornecedor
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                vendedor=bool(resultado["vendedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter vendedores: {e}")
    return []

def obter_locadores() -> List[Fornecedor]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_LOCADORES)
            resultados = cursor.fetchall()

            return [Fornecedor(
                # Campos de Usuario na ordem correta
                id=resultado["id"],
                nome=resultado["nome"],
                cpf=resultado["cpf"],
                data_nascimento=resultado["data_nascimento"],
                email=resultado["email"],
                telefone=resultado["telefone"],
                senha=resultado["senha"],
                perfil=TipoUsuario.FORNECEDOR,
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"],
                # Campos específicos de Fornecedor
                nome_empresa=resultado["nome_empresa"],
                cnpj=resultado["cnpj"],
                descricao=resultado["descricao"],
                prestador=bool(resultado["prestador"]),
                vendedor=bool(resultado["vendedor"]),
                locador=bool(resultado["locador"])
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter locadores: {e}")
    return []
def contar_fornecedores() -> int:
    """Conta o total de fornecedores no sistema"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_FORNECEDORES)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar fornecedores: {e}")
        return 0

def contar_fornecedores_nao_verificados() -> int:
    """Conta o total de fornecedores não verificados"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_FORNECEDORES_NAO_VERIFICADOS)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar fornecedores não verificados: {e}")
        return 0

def rejeitar_fornecedor(id_fornecedor: int) -> bool:
    """Rejeita um fornecedor, removendo a verificação"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(REJEITAR_FORNECEDOR, (id_fornecedor,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao rejeitar fornecedor: {e}")
        return False
