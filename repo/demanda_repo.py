from typing import Optional, List, Union
from datetime import datetime
from util.base_repo import BaseRepo
from sql import demanda_sql
from model.demanda_model import Demanda, StatusDemanda

class DemandaRepo(BaseRepo):
    """Repositório para operações com demandas"""

    def __init__(self):
        super().__init__('demanda', Demanda, demanda_sql)

    def _objeto_para_tupla_insert(self, demanda: Demanda) -> tuple:
        """Prepara dados da demanda para inserção"""
        return (
            demanda.id_casal,
            demanda.id_categoria,
            demanda.titulo,
            demanda.descricao,
            demanda.orcamento_min,
            demanda.orcamento_max,
            demanda.prazo_entrega,
            demanda.observacoes
        )

    def _objeto_para_tupla_update(self, demanda: Demanda) -> tuple:
        """Prepara dados da demanda para atualização"""
        return (
            demanda.titulo,
            demanda.descricao,
            demanda.orcamento_min,
            demanda.orcamento_max,
            demanda.prazo_entrega,
            demanda.observacoes,
            demanda.id
        )

    def _linha_para_objeto(self, linha: dict) -> Demanda:
        """Converte linha do banco em objeto Demanda"""
        # Converter Row para dict se necessário
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Demanda(
            id=linha_dict["id"],
            id_casal=linha_dict["id_casal"],
            id_categoria=linha_dict["id_categoria"],
            titulo=linha_dict["titulo"],
            descricao=linha_dict["descricao"],
            orcamento_min=linha_dict.get("orcamento_min"),
            orcamento_max=linha_dict.get("orcamento_max"),
            prazo_entrega=linha_dict.get("prazo_entrega"),
            status=StatusDemanda(linha_dict.get("status", "ATIVA")),
            data_criacao=linha_dict.get("data_criacao"),
            observacoes=linha_dict.get("observacoes")
        )

    def atualizar_status_demanda(self, id: int, status: StatusDemanda) -> bool:
        """Atualiza apenas o status de uma demanda"""
        return self.executar_comando(demanda_sql.ATUALIZAR_STATUS_DEMANDA, (status.value, id))

    def obter_demandas_por_casal(self, id_casal: int) -> List[Demanda]:
        """Obtém todas as demandas de um casal"""
        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_POR_CASAL, (id_casal,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_demandas_por_categoria(self, id_categoria: int) -> List[Demanda]:
        """Obtém todas as demandas de uma categoria"""
        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_POR_CATEGORIA, (id_categoria,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_demandas_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
        """Lista demandas com paginação"""
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_query(demanda_sql.OBTER_DEMANDAS_POR_PAGINA, (limite, offset))
        return [self._linha_para_objeto(row) for row in resultados]

# Instância global do repositório
demanda_repo = DemandaRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_demandas() -> bool:
    return demanda_repo.criar_tabela()

def inserir_demanda(demanda: Demanda) -> Optional[int]:
    return demanda_repo.inserir(demanda)

def atualizar_demanda(demanda: Demanda) -> bool:
    return demanda_repo.atualizar(demanda)

def atualizar_status_demanda(id_demanda: int, status: StatusDemanda) -> bool:
    return demanda_repo.atualizar_status_demanda(id_demanda, status)

def excluir_demanda(id: int) -> bool:
    return demanda_repo.excluir(id)

def obter_demanda_por_id(id: int) -> Optional[Demanda]:
    return demanda_repo.obter_por_id(id)

def obter_demandas_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
    return demanda_repo.obter_demandas_por_pagina(numero_pagina, tamanho_pagina)

def obter_demandas_por_casal(id_casal: int) -> List[Demanda]:
    return demanda_repo.obter_demandas_por_casal(id_casal)

def obter_demandas_ativas() -> List[Demanda]:
    resultados = demanda_repo.executar_query(demanda_sql.OBTER_DEMANDAS_ATIVAS)
    return [demanda_repo._linha_para_objeto(row) for row in resultados]

def buscar_demandas(termo: str) -> List[Demanda]:
    termo_like = f"%{termo}%"
    resultados = demanda_repo.executar_query(demanda_sql.BUSCAR_DEMANDAS, (termo_like, termo_like))
    return [demanda_repo._linha_para_objeto(row) for row in resultados]

def obter_demandas_por_status(status: Union[str, StatusDemanda]) -> List[Demanda]:
    """Obtém todas as demandas com um status específico"""
    # Converter para string se for enum
    if isinstance(status, StatusDemanda):
        status_str = status.value
    else:
        status_str = status.upper()

    # Validar status usando o enum StatusDemanda
    valid_statuses = [s.value for s in StatusDemanda]
    if status_str not in valid_statuses:
        from util.logger import logger
        logger.warning(f"Status inválido: {status}. Status válidos: {valid_statuses}")
        return []

    resultados = demanda_repo.executar_query(demanda_sql.OBTER_DEMANDAS_POR_STATUS, (status_str,))
    return [demanda_repo._linha_para_objeto(row) for row in resultados]

def obter_demandas_por_categoria(id_categoria: int) -> List[Demanda]:
    return demanda_repo.obter_demandas_por_categoria(id_categoria)

def contar_demandas() -> int:
    """Conta o total de demandas no sistema"""
    resultados = demanda_repo.executar_query("SELECT COUNT(*) as total FROM demanda")
    return resultados[0]["total"] if resultados else 0

def listar_demandas() -> List[Demanda]:
    return demanda_repo.listar_todos()