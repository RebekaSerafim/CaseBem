from typing import Optional, List
from util.database import obter_conexao
from sql.item_demanda_servico_sql import *
from model.item_demanda_servico_model import ItemDemandaServico

def criar_tabela_item_demanda_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_DEMANDA_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemDemandaServico: {e}")
        return False

def inserir_item_demanda_servico(item: ItemDemandaServico) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_DEMANDA_SERVICO,
            (item.id_demanda, item.id_servico, item.quantidade, item.observacoes)
        )
        return cursor.rowcount > 0

def atualizar_item_demanda_servico(item: ItemDemandaServico) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_DEMANDA_SERVICO,
            (item.quantidade, item.observacoes, item.id_demanda, item.id_servico)
        )
        return cursor.rowcount > 0

def excluir_item_demanda_servico(id_demanda: int, id_servico: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_DEMANDA_SERVICO, (id_demanda, id_servico))
        return cursor.rowcount > 0

def obter_item_demanda_servico_por_id(id_demanda: int, id_servico: int) -> Optional[ItemDemandaServico]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_DEMANDA_SERVICO_POR_ID, (id_demanda, id_servico))
        resultado = cursor.fetchone()
        if resultado:
            return ItemDemandaServico(
                id_demanda=resultado["id_demanda"],
                id_servico=resultado["id_servico"],
                quantidade=resultado["quantidade"],
                observacoes=resultado["observacoes"]
            )
    return None

def obter_itens_por_demanda(id_demanda: int) -> List[ItemDemandaServico]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_POR_DEMANDA, (id_demanda,))
        resultados = cursor.fetchall()
        return [ItemDemandaServico(
            id_demanda=r["id_demanda"],
            id_servico=r["id_servico"],
            quantidade=r["quantidade"],
            observacoes=r["observacoes"]
        ) for r in resultados]

def obter_itens_demanda_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemDemandaServico]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_ITENS_DEMANDA_SERVICO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [ItemDemandaServico(
            id_demanda=r["id_demanda"],
            id_servico=r["id_servico"],
            quantidade=r["quantidade"],
            observacoes=r["observacoes"]
        ) for r in resultados]