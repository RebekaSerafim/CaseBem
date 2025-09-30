from typing import Optional, List
from util.exceptions import RecursoNaoEncontradoError
from util.database import obter_conexao
from core.sql.fornecedor_sql import *
from core.models.fornecedor_model import Fornecedor
from core.models.usuario_model import TipoUsuario
from core.repositories import usuario_repo

class FornecedorRepo:
    """Repositório para operações com fornecedores"""

    def __init__(self):
        self.nome_tabela = 'fornecedor'

    def _linha_para_objeto(self, linha: dict) -> Fornecedor:
        """Converte linha do banco em objeto Fornecedor"""
        def safe_get(row, key, default=None):
            try:
                return row[key] if row[key] is not None else default
            except (KeyError, IndexError):
                return default

        return Fornecedor(
            # Campos de Usuario
            id=linha["id"],
            nome=linha["nome"],
            cpf=linha["cpf"],
            data_nascimento=linha["data_nascimento"],
            email=linha["email"],
            telefone=linha["telefone"],
            senha=linha["senha"],
            perfil=TipoUsuario.FORNECEDOR,
            token_redefinicao=safe_get(linha, "token_redefinicao"),
            data_token=safe_get(linha, "data_token"),
            data_cadastro=safe_get(linha, "data_cadastro"),
            # Campos específicos de Fornecedor
            nome_empresa=linha["nome_empresa"],
            cnpj=linha["cnpj"],
            descricao=safe_get(linha, "descricao"),
            verificado=bool(linha["verificado"]),
            data_verificacao=safe_get(linha, "data_verificacao"),
            newsletter=bool(linha["newsletter"])
        )

    def criar_tabela(self) -> bool:
        """Cria a tabela fornecedor"""
        try:
            with obter_conexao() as conexao:
                conexao.execute(CRIAR_TABELA_FORNECEDOR)
            return True
        except Exception as e:
            print(f"Erro ao criar tabela fornecedor: {e}")
            return False

    def inserir(self, fornecedor: Fornecedor) -> Optional[int]:
        """Insere um novo fornecedor"""
        try:
            # Primeiro inserir na tabela usuario
            usuario_id = usuario_repo.usuario_repo.inserir(fornecedor)

            if usuario_id:
                # Depois inserir na tabela fornecedor
                with obter_conexao() as conexao:
                    cursor = conexao.cursor()
                    cursor.execute(INSERIR_FORNECEDOR,
                        (usuario_id, fornecedor.nome_empresa, fornecedor.cnpj,
                         fornecedor.descricao,
                         fornecedor.verificado, fornecedor.data_verificacao,
                         fornecedor.newsletter))
                    return usuario_id
        except Exception as e:
            print(f"Erro ao inserir fornecedor: {e}")
        return None

    def atualizar(self, fornecedor: Fornecedor) -> bool:
        """Atualiza dados do fornecedor"""
        try:
            # Atualizar dados de usuario
            usuario_repo.usuario_repo.atualizar(fornecedor)

            # Atualizar dados específicos de fornecedor
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(ATUALIZAR_FORNECEDOR,
                    (fornecedor.nome_empresa, fornecedor.cnpj, fornecedor.descricao,
                     fornecedor.verificado, fornecedor.data_verificacao,
                     fornecedor.newsletter, fornecedor.id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar fornecedor: {e}")
            return False

    def excluir(self, id: int) -> bool:
        """Exclui um fornecedor"""
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

    def obter_por_id(self, id: int) -> Fornecedor:
        """Obtém fornecedor por ID"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(OBTER_FORNECEDOR_POR_ID, (id,))
                resultado = cursor.fetchone()
                if resultado:
                    return self._linha_para_objeto(resultado)
        except Exception as e:
            print(f"Erro ao obter fornecedor por ID: {e}")
            raise
        raise RecursoNaoEncontradoError(recurso="Fornecedor", identificador=id)

    def obter_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Fornecedor]:
        """Obtém fornecedores com paginação"""
        try:
            with obter_conexao() as conexao:
                limite = tamanho_pagina
                offset = (numero_pagina - 1) * tamanho_pagina
                cursor = conexao.cursor()
                cursor.execute(OBTER_FORNECEDORES_POR_PAGINA, (limite, offset))
                resultados = cursor.fetchall()
                return [self._linha_para_objeto(resultado) for resultado in resultados]
        except Exception as e:
            print(f"Erro ao obter fornecedores por página: {e}")
            return []

    def contar(self) -> int:
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

    def contar_nao_verificados(self) -> int:
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

    def rejeitar(self, id_fornecedor: int) -> bool:
        """Rejeita um fornecedor, removendo a verificação"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(REJEITAR_FORNECEDOR, (id_fornecedor,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao rejeitar fornecedor: {e}")
            return False

# Instância singleton do repositório
fornecedor_repo = FornecedorRepo()