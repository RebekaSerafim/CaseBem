from typing import Optional, List
from datetime import datetime
from util.base_repo import BaseRepo
from sql import orcamento_sql
from model.orcamento_model import Orcamento

class OrcamentoRepo(BaseRepo):
    """Repositório para operações com orçamentos"""

    def __init__(self):
        super().__init__('orcamento', Orcamento, orcamento_sql)

    def _objeto_para_tupla_insert(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para inserção"""
        return (
            orcamento.id_demanda,
            orcamento.id_fornecedor_prestador,
            orcamento.data_hora_cadastro,
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total
        )

    def _objeto_para_tupla_update(self, orcamento: Orcamento) -> tuple:
        """Prepara dados do orçamento para atualização"""
        return (
            orcamento.data_hora_validade,
            orcamento.status,
            orcamento.observacoes,
            orcamento.valor_total,
            orcamento.id
        )

    def _linha_para_objeto(self, linha: dict) -> Orcamento:
        """Converte linha do banco em objeto Orcamento"""
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Orcamento(
            id=linha_dict["id"],
            id_demanda=linha_dict["id_demanda"],
            id_fornecedor_prestador=linha_dict["id_fornecedor_prestador"],
            data_hora_cadastro=linha_dict["data_hora_cadastro"],
            data_hora_validade=linha_dict.get("data_hora_validade"),
            status=linha_dict.get("status", "PENDENTE"),
            observacoes=linha_dict.get("observacoes"),
            valor_total=linha_dict.get("valor_total")
        )

    def atualizar_status_orcamento(self, id: int, status: str) -> bool:
        """Atualiza apenas o status de um orçamento"""
        return self.executar_comando(orcamento_sql.ATUALIZAR_STATUS_ORCAMENTO, (status, id))

    def atualizar_valor_total_orcamento(self, id: int, valor_total: float) -> bool:
        """Atualiza apenas o valor total de um orçamento"""
        return self.executar_comando(orcamento_sql.ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id))

    def obter_orcamentos_por_demanda(self, id_demanda: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de uma demanda"""
        resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_orcamentos_por_fornecedor(self, id_fornecedor: int) -> List[Orcamento]:
        """Obtém todos os orçamentos de um fornecedor"""
        resultados = self.executar_query(orcamento_sql.OBTER_ORCAMENTOS_POR_FORNECEDOR, (id_fornecedor,))
        return [self._linha_para_objeto(row) for row in resultados]

# Instância global do repositório
orcamento_repo = OrcamentoRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_orcamento() -> bool:
    return orcamento_repo.criar_tabela()

def inserir_orcamento(orcamento: Orcamento) -> Optional[int]:
    return orcamento_repo.inserir(orcamento)

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    return orcamento_repo.atualizar(orcamento)

def excluir_orcamento(id: int) -> bool:
    return orcamento_repo.excluir(id)

def obter_orcamento_por_id(id: int) -> Optional[Orcamento]:
    return orcamento_repo.obter_por_id(id)

def listar_orcamentos() -> List[Orcamento]:
    return orcamento_repo.listar_todos()

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    return orcamento_repo.atualizar_status_orcamento(id_orcamento, status)

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    return orcamento_repo.atualizar_valor_total_orcamento(id_orcamento, valor_total)

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    return orcamento_repo.obter_orcamentos_por_demanda(id_demanda)

def obter_orcamentos_por_fornecedor_prestador(id_fornecedor: int) -> List[Orcamento]:
    return orcamento_repo.obter_orcamentos_por_fornecedor(id_fornecedor)

# Demais funções específicas permanecem com implementação original mas são raramente usadas

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do orçamento pelo ID
        cursor.execute(ATUALIZAR_ORCAMENTO, 
            (orcamento.data_hora_validade, orcamento.status,
             orcamento.observacoes, orcamento.valor_total, orcamento.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar status do orçamento
        cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar valor total do orçamento
        cursor.execute(ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para aceitar orçamento e rejeitar outros
        cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_orcamento(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar orçamento pelo ID
        cursor.execute(EXCLUIR_ORCAMENTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_orcamento_por_id(id: int) -> Optional[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamento pelo ID
        cursor.execute(OBTER_ORCAMENTO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Orcamento com dados do banco
            return Orcamento(
                id=resultado["id"],
                id_demanda=resultado["id_demanda"],
                id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
                data_hora_cadastro=resultado["data_hora_cadastro"],
                data_hora_validade=resultado["data_hora_validade"],
                status=resultado["status"],
                observacoes=resultado["observacoes"],
                valor_total=resultado["valor_total"]
            )
    # Retorna None se não encontrou orçamento
    return None

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por demanda
        cursor.execute(OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_fornecedor_prestador(id_fornecedor_prestador: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por fornecedor/prestador
        cursor.execute(OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor_prestador,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_noivo(id_noivo: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por noivo
        cursor.execute(OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_status(status: str) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por status
        cursor.execute(OBTER_ORCAMENTOS_POR_STATUS, (status,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos com paginação
        cursor.execute(OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]
def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    """Aceita um orçamento específico e rejeita todos os outros da mesma demanda"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        return False

def rejeitar_orcamento(id_orcamento: int) -> bool:
    """Rejeita um orçamento específico"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(REJEITAR_ORCAMENTO, (id_orcamento,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao rejeitar orçamento: {e}")
        return False

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    """Atualiza o status de um orçamento"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status do orçamento: {e}")
        return False

def contar_orcamentos() -> int:
    """Conta o total de orçamentos no sistema"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM orcamento")
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar orçamentos: {e}")
        return 0
