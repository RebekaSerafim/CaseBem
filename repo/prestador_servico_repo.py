from typing import Optional, List
from util.database import obter_conexao
from sql.prestador_servico_sql import *
from model.prestador_servico_model import Prestador

def criar_tabela_prestador_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_PRESTADOR_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela PrestadorServico: {e}")
        return False

def inserir_prestador_servico(ps: Prestador) -> Optional[tuple]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_PRESTADOR_SERVICO,
            (ps.id_prestador, ps.id_servico, ps.observacoes, ps.preco)
        )
        return (ps.id_prestador, ps.id_servico)

def atualizar_prestador_servico(ps: Prestador) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_PRESTADOR_SERVICO,
            (ps.observacoes, ps.preco, ps.id_prestador, ps.id_servico)
        )
        return cursor.rowcount > 0

def excluir_prestador_servico(id_prestador: int, id_servico: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_PRESTADOR_SERVICO, (id_prestador, id_servico))
        return cursor.rowcount > 0

def obter_prestador_servico_por_id(id_prestador: int, id_servico: int) -> Optional[Prestador]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_PRESTADOR_SERVICO_POR_ID, (id_prestador, id_servico))
        resultado = cursor.fetchone()
        if resultado:
            return Prestador(
                id_prestador=resultado["id_prestador"],
                id_servico=resultado["id_servico"],
                observacoes=resultado["observacoes"],
                preco=resultado["preco"]
            )
    return None

def obter_prestadores_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Prestador]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_PRESTADORES_SERVICO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Prestador(
            id_prestador=r["id_prestador"],
            id_servico=r["id_servico"],
            observacoes=r["observacoes"],
            preco=r["preco"]
        ) for r in resultados]