"""
Serviço de casais - Lógica de negócio centralizada

Este serviço concentra todas as regras de negócio relacionadas aos casais,
incluindo criação, atualização e validações de relacionamento entre noivos.
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError, RecursoNaoEncontradoError
from core.models.casal_model import Casal
from core.models.usuario_model import TipoUsuario
from util.logger import logger


class CasalService:
    """
    Serviço para operações de negócio com casais

    Centraliza toda a lógica de negócio relacionada aos casais,
    aplicando validações, regras de domínio e orquestrando operações.
    """

    def __init__(self):
        from core.repositories import casal_repo, usuario_repo

        self.repo = casal_repo
        self.usuario_repo = usuario_repo

    def criar_casal(self, dados: dict) -> int:
        """
        Cria um novo casal aplicando regras de negócio

        Args:
            dados: Dados validados do casal

        Returns:
            ID do casal criado

        Raises:
            RegraDeNegocioError: Se regra de negócio for violada
        """
        id_noivo1 = dados['id_noivo1']
        id_noivo2 = dados.get('id_noivo2')

        # Validar que os noivos não são a mesma pessoa
        if id_noivo2 and id_noivo1 == id_noivo2:
            raise RegraDeNegocioError("Um casal não pode ser formado pela mesma pessoa")

        # Validar que ambos os usuários existem e são noivos
        try:
            noivo1 = self.usuario_repo.obter_usuario_por_id(id_noivo1)
            if noivo1.perfil != TipoUsuario.NOIVO:
                raise RegraDeNegocioError(f"Usuário {id_noivo1} não é um noivo")
        except RecursoNaoEncontradoError:
            raise RegraDeNegocioError(f"Noivo {id_noivo1} não encontrado")

        if id_noivo2:
            try:
                noivo2 = self.usuario_repo.obter_usuario_por_id(id_noivo2)
                if noivo2.perfil != TipoUsuario.NOIVO:
                    raise RegraDeNegocioError(f"Usuário {id_noivo2} não é um noivo")
            except RecursoNaoEncontradoError:
                raise RegraDeNegocioError(f"Noivo {id_noivo2} não encontrado")

        # Validar que os noivos não estão em outro casal
        casal_existente = self.repo.obter_casal_por_noivo(id_noivo1)
        if casal_existente:
            raise RegraDeNegocioError(f"Noivo {id_noivo1} já está em um casal")

        if id_noivo2:
            casal_existente = self.repo.obter_casal_por_noivo(id_noivo2)
            if casal_existente:
                raise RegraDeNegocioError(f"Noivo {id_noivo2} já está em um casal")

        # Validar orçamento
        if dados.get('orcamento_estimado') and dados['orcamento_estimado'] < 0:
            raise RegraDeNegocioError("Orçamento não pode ser negativo")

        # Criar casal
        casal = Casal(**dados)
        id_casal = self.repo.inserir_casal(casal)

        logger.info(f"Casal criado: {id_casal}", extra={
            'id_noivo1': id_noivo1,
            'id_noivo2': id_noivo2
        })

        return id_casal

    def atualizar_casal(self, id_casal: int, dados: dict) -> bool:
        """
        Atualiza dados de um casal

        Args:
            id_casal: ID do casal
            dados: Dados a serem atualizados

        Returns:
            True se atualizado com sucesso
        """
        # Buscar casal existente
        casal = self.repo.obter_casal_por_id(id_casal)

        # Validar orçamento se fornecido
        if 'orcamento_estimado' in dados and dados['orcamento_estimado'] < 0:
            raise RegraDeNegocioError("Orçamento não pode ser negativo")

        # Validar número de convidados se fornecido
        if 'numero_convidados' in dados and dados['numero_convidados'] < 0:
            raise RegraDeNegocioError("Número de convidados não pode ser negativo")

        # Atualizar campos permitidos
        campos_atualizaveis = ['data_casamento', 'local_previsto', 'orcamento_estimado', 'numero_convidados']
        for campo in campos_atualizaveis:
            if campo in dados:
                setattr(casal, campo, dados[campo])

        # Salvar
        sucesso = self.repo.atualizar_casal(casal)

        if sucesso:
            logger.info(f"Casal atualizado: {id_casal}")

        return sucesso

    def obter_casal(self, id_casal: int) -> Casal:
        """
        Obtém um casal por ID

        Args:
            id_casal: ID do casal

        Returns:
            Casal encontrado
        """
        return self.repo.obter_casal_por_id(id_casal)

    def obter_casal_por_noivo(self, id_noivo: int) -> Optional[Casal]:
        """
        Obtém o casal de um noivo

        Args:
            id_noivo: ID do noivo

        Returns:
            Casal do noivo ou None
        """
        return self.repo.obter_casal_por_noivo(id_noivo)

    def listar_casais(self, pagina: int = 1, tamanho: int = 10) -> List[Casal]:
        """
        Lista casais com paginação

        Args:
            pagina: Número da página
            tamanho: Tamanho da página

        Returns:
            Lista de casais
        """
        return self.repo.obter_casais_por_pagina(pagina, tamanho)

    def excluir_casal(self, id_casal: int) -> bool:
        """
        Exclui um casal

        Args:
            id_casal: ID do casal

        Returns:
            True se excluído com sucesso
        """
        # Verificar se existe
        self.repo.obter_casal_por_id(id_casal)

        # Excluir
        sucesso = self.repo.excluir_casal(id_casal)

        if sucesso:
            logger.info(f"Casal excluído: {id_casal}")

        return sucesso


# Instância singleton do serviço
casal_service = CasalService()