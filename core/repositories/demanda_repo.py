from typing import Optional, List, Union
from datetime import datetime
from util.database import obter_conexao
from util.exceptions import RecursoNaoEncontradoError
from core.sql.demanda_sql import *
from core.models.demanda_model import Demanda, StatusDemanda

def criar_tabela_demandas() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_DEMANDA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de demandas: {e}")
        return False

def inserir_demanda(demanda: Demanda) -> Optional[int]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_DEMANDA, (
                demanda.id_casal,
                demanda.id_categoria,
                demanda.titulo,
                demanda.descricao,
                demanda.orcamento_min,
                demanda.orcamento_max,
                demanda.prazo_entrega,
                demanda.observacoes
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir demanda: {e}")
        return None

def atualizar_demanda(demanda: Demanda) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_DEMANDA, (
                demanda.titulo,
                demanda.descricao,
                demanda.orcamento_min,
                demanda.orcamento_max,
                demanda.prazo_entrega,
                demanda.observacoes,
                demanda.id
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar demanda: {e}")
        return False

def atualizar_status_demanda(id_demanda: int, status: StatusDemanda) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_STATUS_DEMANDA, (status.value, id_demanda))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status da demanda: {e}")
        return False

def excluir_demanda(id: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_DEMANDA, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir demanda: {e}")
        return False

def obter_demanda_por_id(id: int) -> Demanda:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_DEMANDA_POR_ID, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return _criar_demanda_de_resultado(resultado)
    except Exception as e:
        print(f"Erro ao obter demanda por ID: {e}")
        raise
    raise RecursoNaoEncontradoError(recurso="Demanda", identificador=id)

def obter_demandas_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
    try:
        with obter_conexao() as conexao:
            limite = tamanho_pagina
            offset = (numero_pagina - 1) * tamanho_pagina
            cursor = conexao.cursor()
            cursor.execute(OBTER_DEMANDAS_POR_PAGINA, (limite, offset))
            resultados = cursor.fetchall()
            return [_criar_demanda_de_resultado(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter demandas por página: {e}")
        return []

def obter_demandas_por_casal(id_casal: int) -> List[Demanda]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_DEMANDAS_POR_CASAL, (id_casal,))
            resultados = cursor.fetchall()
            return [_criar_demanda_de_resultado(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter demandas por casal: {e}")
        return []

def obter_demandas_ativas() -> List[Demanda]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_DEMANDAS_ATIVAS)
            resultados = cursor.fetchall()
            return [_criar_demanda_de_resultado(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter demandas ativas: {e}")
        return []

def buscar_demandas(termo: str) -> List[Demanda]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            termo_like = f"%{termo}%"
            cursor.execute(BUSCAR_DEMANDAS, (termo_like, termo_like))
            resultados = cursor.fetchall()
            return [_criar_demanda_de_resultado(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao buscar demandas: {e}")
        return []

def obter_demandas_por_status(status: Union[str, StatusDemanda]) -> List[Demanda]:
    """
    Obtém todas as demandas com um status específico

    Args:
        status (Union[str, StatusDemanda]): Status da demanda (ATIVA, FINALIZADA, CANCELADA)

    Returns:
        List[Demanda]: Lista de demandas com o status especificado
    """
    try:
        # Converter para string se for enum
        if isinstance(status, StatusDemanda):
            status_str = status.value
        else:
            status_str = status.upper()

        # Validar status usando o enum StatusDemanda
        valid_statuses = [s.value for s in StatusDemanda]

        if status_str not in valid_statuses:
            print(f"Status inválido: {status}. Status válidos: {valid_statuses}")
            return []

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_DEMANDAS_POR_STATUS, (status_str,))
            resultados = cursor.fetchall()
            return [_criar_demanda_de_resultado(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter demandas por status {status}: {e}")
        return []

def _criar_demanda_de_resultado(resultado) -> Demanda:
    return Demanda(
        id=resultado["id"],
        id_casal=resultado["id_casal"],
        id_categoria=resultado["id_categoria"],
        titulo=resultado["titulo"],
        descricao=resultado["descricao"],
        orcamento_min=resultado["orcamento_min"],
        orcamento_max=resultado["orcamento_max"],
        prazo_entrega=resultado["prazo_entrega"],
        status=resultado["status"],
        data_criacao=resultado["data_criacao"],
        observacoes=resultado["observacoes"]
    )

def contar_demandas() -> int:
    """Conta o total de demandas no sistema"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM demanda")
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar demandas: {e}")
        return 0