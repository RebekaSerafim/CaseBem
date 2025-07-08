from typing import Optional, List
from util.database import obter_conexao
from sql.item_contrato_servico_sql import *
from model.item_demanda_servico_model import ItemDemandaServico

def criar_tabela_item_contrato_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_CONTRATO_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemDemandaServico: {e}")
        return False

def inserir_item_contrato_servico(item: ItemDemandaServico) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_CONTRATO_SERVICO,
            (item.valor, item.quantidade, item.id_servico)
        )
        return cursor.lastrowid

def atualizar_item_contrato_servico(item: ItemDemandaServico) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_CONTRATO_SERVICO,
            (item.valor, item.quantidade, item.id_servico, item.id_item_contrato_servico)
        )
        return cursor.rowcount > 0

def excluir_item_contrato_servico(id_item: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_CONTRATO_SERVICO, (id_item,))
        return cursor.rowcount > 0

def obter_item_contrato_servico_por_id(id_item: int) -> Optional[ItemDemandaServico]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_CONTRATO_SERVICO_POR_ID, (id_item,))
        resultado = cursor.fetchone()
        if resultado:
            return ItemDemandaServico(
                id_item_contrato_servico=resultado["idItemDemandaServico"],
                valor=resultado["valor"],
                quantidade=resultado["quantidade"],
                id_servico=resultado["idServico"]
            )
    return None

def obter_itens_contrato_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemDemandaServico]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_ITENS_CONTRATO_SERVICO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [ItemDemandaServico(
            id_item_contrato_servico=r["idItemDemandaServico"],
            valor=r["valor"],
            quantidade=r["quantidade"],
            id_servico=r["idServico"]
        ) for r in resultados]
