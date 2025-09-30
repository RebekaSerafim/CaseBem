from typing import Optional, List
from util.base_repo import BaseRepo
from util.exceptions import RecursoNaoEncontradoError
from util.database import obter_conexao
from util.logger import logger
from core.sql import fornecedor_sql
from core.models.fornecedor_model import Fornecedor
from core.models.usuario_model import TipoUsuario
from core.repositories import usuario_repo

class FornecedorRepo(BaseRepo):
    """Repositório para operações com fornecedores"""

    def __init__(self):
        super().__init__('fornecedor', Fornecedor, fornecedor_sql)

    def _linha_para_objeto(self, linha: dict) -> Fornecedor:
        """Converte linha do banco em objeto Fornecedor"""
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
            token_redefinicao=self._safe_get(linha, "token_redefinicao"),
            data_token=self._safe_get(linha, "data_token"),
            data_cadastro=self._safe_get(linha, "data_cadastro"),
            # Campos específicos de Fornecedor
            nome_empresa=linha["nome_empresa"],
            cnpj=linha["cnpj"],
            descricao=self._safe_get(linha, "descricao"),
            verificado=bool(linha["verificado"]),
            data_verificacao=self._safe_get(linha, "data_verificacao"),
            newsletter=bool(linha["newsletter"])
        )

    def _objeto_para_tupla_insert(self, fornecedor: Fornecedor) -> tuple:
        """Prepara dados do fornecedor para inserção (apenas dados da tabela fornecedor)"""
        return (
            fornecedor.id,  # ID vem do usuário já inserido
            fornecedor.nome_empresa,
            fornecedor.cnpj,
            fornecedor.descricao,
            fornecedor.verificado,
            fornecedor.data_verificacao,
            fornecedor.newsletter
        )

    def _objeto_para_tupla_update(self, fornecedor: Fornecedor) -> tuple:
        """Prepara dados do fornecedor para atualização"""
        return (
            fornecedor.nome_empresa,
            fornecedor.cnpj,
            fornecedor.descricao,
            fornecedor.verificado,
            fornecedor.data_verificacao,
            fornecedor.newsletter,
            fornecedor.id
        )

    def inserir(self, fornecedor: Fornecedor) -> Optional[int]:
        """
        Insere um novo fornecedor (override de BaseRepo).

        Lógica especial: insere primeiro em Usuario, depois em Fornecedor.
        """
        # Primeiro inserir na tabela usuario
        usuario_id = usuario_repo.usuario_repo.inserir(fornecedor)

        if usuario_id:
            # Atualizar ID do fornecedor com o ID do usuário
            fornecedor.id = usuario_id

            # Inserir na tabela fornecedor usando BaseRepo
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                valores = self._objeto_para_tupla_insert(fornecedor)
                cursor.execute(self.sql.INSERIR, valores)
                logger.info(f"Fornecedor inserido", fornecedor_id=usuario_id)
                return usuario_id
        return None

    def atualizar(self, fornecedor: Fornecedor) -> bool:
        """
        Atualiza dados do fornecedor (override de BaseRepo).

        Lógica especial: atualiza Usuario E Fornecedor.
        """
        # Atualizar dados de usuario
        usuario_repo.usuario_repo.atualizar(fornecedor)

        # Atualizar dados específicos de fornecedor
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_update(fornecedor)
            cursor.execute(self.sql.ATUALIZAR, valores)
            atualizado = cursor.rowcount > 0

            if atualizado:
                logger.info(f"Fornecedor atualizado", fornecedor_id=fornecedor.id)
            else:
                logger.warning(f"Nenhum fornecedor foi atualizado", fornecedor_id=fornecedor.id)

            return atualizado

    def excluir(self, id: int) -> bool:
        """
        Exclui um fornecedor (override de BaseRepo).

        Lógica especial: exclui de Fornecedor E Usuario.
        """
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            # Primeiro excluir da tabela fornecedor
            cursor.execute(self.sql.EXCLUIR, (id,))
            # Depois excluir da tabela usuario na mesma conexão
            cursor.execute(fornecedor_sql.EXCLUIR_USUARIO_FORNECEDOR, (id,))
            excluido = cursor.rowcount > 0

            if excluido:
                logger.info(f"Fornecedor excluído", fornecedor_id=id)
            else:
                logger.warning(f"Nenhum fornecedor foi excluído", fornecedor_id=id)

            return excluido

    def contar_nao_verificados(self) -> int:
        """Conta o total de fornecedores não verificados"""
        resultados = self.executar_query(fornecedor_sql.CONTAR_FORNECEDORES_NAO_VERIFICADOS)
        total = resultados[0]["total"] if resultados else 0
        logger.info(f"Contagem de fornecedores não verificados realizada", total=total)
        return total

    def rejeitar(self, id_fornecedor: int) -> bool:
        """Rejeita um fornecedor, removendo a verificação"""
        sucesso = self.executar_comando(fornecedor_sql.REJEITAR_FORNECEDOR, (id_fornecedor,))
        if sucesso:
            logger.info(f"Fornecedor rejeitado", fornecedor_id=id_fornecedor)
        else:
            logger.warning(f"Nenhum fornecedor foi rejeitado", fornecedor_id=id_fornecedor)
        return sucesso

# Instância singleton do repositório
fornecedor_repo = FornecedorRepo()