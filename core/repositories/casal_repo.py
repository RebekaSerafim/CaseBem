from typing import Optional, List
from core.repositories.base_repo import BaseRepo
from core.repositories import usuario_repo
from util.exceptions import RecursoNaoEncontradoError
from core.sql import casal_sql
from core.models.casal_model import Casal


class CasalRepo(BaseRepo):
    """Repositório para operações com casais"""

    def __init__(self) -> None:
        super().__init__("casal", Casal, casal_sql)

    def _objeto_para_tupla_insert(self, casal: Casal) -> tuple:
        """Prepara dados do casal para inserção"""
        return (
            casal.id_noivo1,
            casal.id_noivo2,
            casal.data_casamento,
            casal.local_previsto,
            casal.orcamento_estimado,
            casal.numero_convidados,
        )

    def _objeto_para_tupla_update(self, casal: Casal) -> tuple:
        """Prepara dados do casal para atualização"""
        return (
            casal.data_casamento,
            casal.local_previsto,
            casal.orcamento_estimado,
            casal.numero_convidados,
            casal.id,
        )

    def _linha_para_objeto(self, linha: dict) -> Casal:
        """Converte linha do banco em objeto Casal"""
        return Casal(
            id=linha["id"],
            id_noivo1=linha["id_noivo1"],
            id_noivo2=linha["id_noivo2"],
            data_casamento=linha["data_casamento"],
            local_previsto=linha["local_previsto"],
            orcamento_estimado=linha["orcamento_estimado"],
            numero_convidados=linha["numero_convidados"],
            data_cadastro=linha["data_cadastro"],
        )

    def obter_por_id_completo(self, id: int) -> Casal:
        """Obtém casal por ID com dados dos noivos"""
        resultados = self.executar_consulta(casal_sql.OBTER_CASAL_POR_ID, (id,))
        if resultados:
            resultado = resultados[0]
            # Usa _linha_para_objeto para criar o objeto base
            casal = self._linha_para_objeto(resultado)
            # Adiciona os objetos Usuario dos noivos
            casal.noivo1 = usuario_repo.obter_por_id(  # type: ignore[attr-defined]
                resultado["id_noivo1"]
            )
            casal.noivo2 = usuario_repo.obter_por_id(  # type: ignore[attr-defined]
                resultado["id_noivo2"]
            )
            return casal
        raise RecursoNaoEncontradoError(recurso="Casal", identificador=id)

    def obter_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Casal]:
        """Obtém casais com paginação"""
        casais, _ = self.obter_paginado(numero_pagina, tamanho_pagina)
        return casais  # type: ignore[no-any-return]

    def obter_por_noivo(self, id_noivo: int) -> Optional[Casal]:
        """Obtém casal pelo ID de um dos noivos"""
        resultados = self.executar_consulta(
            casal_sql.OBTER_CASAL_POR_NOIVO, (id_noivo, id_noivo)
        )
        if resultados:
            return self._linha_para_objeto(resultados[0])
        return None


# Instância singleton do repositório
casal_repo = CasalRepo()
