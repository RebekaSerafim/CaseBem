from typing import Optional
from repo import usuario_repo
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

def inserir_casal(casal: Casal) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_CASAL, (casal.id_noivo1, casal.id_noivo2, casal.orcamento))
        return cursor.lastrowid

def atualizar_casal(casal: Casal) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_CASAL, (casal.orcamento, casal.id))
        return (cursor.rowcount > 0)

def excluir_casal(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_CASAL, (id,))
        return (cursor.rowcount > 0)

def obter_casal_por_id(id: int) -> Optional[Casal]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Casal(      
                id=resultado["id"],          
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                orcamento=resultado["orcamento"],
                noivo1=usuario_repo.obter_usuario_por_id(resultado["id_noivo1"]),
                noivo2=usuario_repo.obter_usuario_por_id(resultado["id_noivo2"])
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
            id=resultado["id"],
            id_noivo1=resultado["id_noivo1"],
            id_noivo2=resultado["id_noivo2"],
            orcamento=resultado["orcamento"]
        ) for resultado in resultados]

def obter_casal_por_noivo(id_noivo: int) -> Optional[Casal]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_CASAL_POR_NOIVO, (id_noivo, id_noivo))
        resultado = cursor.fetchone()
        if resultado:
            return Casal(
                id=resultado["id"],
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                orcamento=resultado["orcamento"]
            )
    return None
