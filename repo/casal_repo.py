from typing import Optional, List, Tuple
from util.database import obter_conexao
from sql.casal_sql import *
from model.casal_model import Casal

def criar_tabela_casal() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_CASAL)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de noivos: {e}")
        return False

def inserir_casal(casal: Casal) -> Optional[Tuple[int, int]]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_CASAL, (casal.id_noivo1, casal.id_noivo2, casal.orcamento))
        return (casal.id_noivo1, casal.id_noivo2) if cursor.rowcount > 0 else None

def atualizar_casal(casal: Casal) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_CASAL, (casal.orcamento, casal.id_noivo1, casal.id_noivo2))
        return (cursor.rowcount > 0)

def excluir_casal(casal: Casal) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_CASAL, (casal.id_noivo1, casal.id_noivo2))
        return (cursor.rowcount > 0)

def obter_casal_por_ids(id_noivo1: int, id_noivo2) -> Optional[Casal]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_IDS, (id_noivo1, id_noivo2))
        resultado = cursor.fetchone()
        if resultado:
            return Casal(                
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                orcamento=resultado["orcamento"]
            )
    return None

def obter_casais_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Casal]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Casal(
            id_noivo1=resultado["id_noivo1"],
            id_noivo2=resultado["id_noivo2"],
            orcamento=resultado["orcamento"]
        ) for resultado in resultados]
