from typing import Optional, List
from util.database import obter_conexao
from sql.prestador_servico_sql import *
from model.prestador_servico_model import PrestadorServico

def criar_tabela_prestador_servico() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_PRESTADOR_SERVICO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela PrestadorServico: {e}")
        return False

def inserir_prestador_servico(servico: PrestadorServico) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_PRESTADOR_SERVICO,
            (servico.id_prestador, servico.descricao)
        )
        return cursor.lastrowid
