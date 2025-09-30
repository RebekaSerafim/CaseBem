from typing import Optional, List
from util.database import obter_conexao
from core.sql.favorito_sql import *
from core.models.favorito_model import Favorito

def criar_tabela_favoritos() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_FAVORITO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de favoritos: {e}")
        return False

def adicionar_favorito(id_noivo: int, id_item: int) -> bool:
    """Adiciona um item aos favoritos do noivo"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_FAVORITO, (id_noivo, id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao adicionar favorito: {e}")
        return False

def remover_favorito(id_noivo: int, id_item: int) -> bool:
    """Remove um item dos favoritos do noivo"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_FAVORITO, (id_noivo, id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover favorito: {e}")
        return False

def obter_favoritos_por_noivo(id_noivo: int) -> List[dict]:
    """Obtém todos os favoritos de um noivo com dados dos itens"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_FAVORITOS_POR_NOIVO, (id_noivo,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter favoritos: {e}")
        return []

def verificar_favorito(id_noivo: int, id_item: int) -> bool:
    """Verifica se um item está nos favoritos do noivo"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(VERIFICAR_FAVORITO, (id_noivo, id_item))
            resultado = cursor.fetchone()
            return resultado["count"] > 0 if resultado else False
    except Exception as e:
        print(f"Erro ao verificar favorito: {e}")
        return False

def contar_favoritos_por_noivo(id_noivo: int) -> int:
    """Conta o total de favoritos de um noivo"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_FAVORITOS_POR_NOIVO, (id_noivo,))
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar favoritos: {e}")
        return 0