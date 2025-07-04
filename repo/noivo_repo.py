from typing import Optional
from util.database import obter_conexao
from sql.noivo_sql import *
from model.noivo_model import Noivo

def criar_tabela_noivos() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_NOIVO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de noivos: {e}")
        return False

def inserir_noivo(noivo: Noivo) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_NOIVO, (noivo.orcamento, noivo.id_noivo1, noivo.id_noivo2))
        return cursor.lastrowid

def atualizar_noivo(noivo: Noivo) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_NOIVO, (noivo.orcamento, noivo.id_noivo1, noivo.id_noivo2, noivo.id))
        return (cursor.rowcount > 0)

def excluir_noivo(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_NOIVO, (id,))
        return (cursor.rowcount > 0)

def obter_noivo_por_id(id: int) -> Optional[Noivo]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_NOIVO_POR_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Noivo(
                id=resultado["id"],
                orcamento=resultado["orcamento"],
                id_noivo1=resultado["id_noivo1"],
                id_noivo2=resultado["id_noivo2"],
                tipo=resultado["tipo"]
            )
    return None

def obter_noivos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Noivo]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(OBTER_NOIVO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Noivo(
            id=resultado["id"],
            orcamento=resultado["orcamento"],
            id_noivo1=resultado["id_noivo1"],
            id_noivo2=resultado["id_noivo2"]
        ) for resultado in resultados]
