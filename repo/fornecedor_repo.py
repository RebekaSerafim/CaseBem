from typing import Optional, List
from util.base_repo import BaseRepo
from sql import fornecedor_sql
from model.fornecedor_model import Fornecedor
from model.usuario_model import TipoUsuario
from repo import usuario_repo

class FornecedorRepo(BaseRepo):
    """Repositório para operações com fornecedor (herda de usuario)"""

    def __init__(self):
        super().__init__('fornecedor', Fornecedor, fornecedor_sql)

    def _objeto_para_tupla_insert(self, fornecedor: Fornecedor) -> tuple:
        """Prepara dados do fornecedor para inserção na tabela fornecedor"""
        return (
            fornecedor.id,
            fornecedor.nome_empresa,
            fornecedor.cnpj,
            fornecedor.descricao,
            fornecedor.verificado,
            fornecedor.data_verificacao,
            fornecedor.newsletter
        )

    def _objeto_para_tupla_update(self, fornecedor: Fornecedor) -> tuple:
        """Prepara dados do fornecedor para atualização"""
        return (
            fornecedor.nome_empresa,
            fornecedor.cnpj,
            fornecedor.descricao,
            fornecedor.verificado,
            fornecedor.data_verificacao,
            fornecedor.newsletter,
            fornecedor.id
        )

    def _linha_para_objeto(self, linha: dict) -> Fornecedor:
        """Converte linha do banco em objeto Fornecedor"""
        return Fornecedor(
            # Campos de Usuario
            id=linha["id"],
            nome=linha["nome"],
            cpf=linha["cpf"],
            data_nascimento=linha["data_nascimento"],
            email=linha["email"],
            telefone=linha["telefone"],
            senha=linha["senha"],
            perfil=TipoUsuario.FORNECEDOR,
            token_redefinicao=linha.get("token_redefinicao"),
            data_token=linha.get("data_token"),
            data_cadastro=linha.get("data_cadastro"),
            # Campos específicos de Fornecedor
            nome_empresa=linha.get("nome_empresa"),
            cnpj=linha.get("cnpj"),
            descricao=linha.get("descricao"),
            verificado=bool(linha.get("verificado", False)),
            data_verificacao=linha.get("data_verificacao"),
            newsletter=bool(linha.get("newsletter", False))
        )

    def inserir(self, fornecedor: Fornecedor) -> Optional[int]:
        """Insere fornecedor nas tabelas usuario e fornecedor"""
        try:
            # Primeiro inserir na tabela usuario
            usuario_id = usuario_repo.inserir_usuario(fornecedor)

            if usuario_id:
                # Depois inserir na tabela fornecedor
                fornecedor.id = usuario_id
                self.executar_comando(self.sql_module.INSERIR, self._objeto_para_tupla_insert(fornecedor))
                return usuario_id
        except Exception as e:
            self.logger.error(f"Erro ao inserir {self.nome_tabela}: {e}")
        return None

    def atualizar(self, fornecedor: Fornecedor) -> bool:
        """Atualiza fornecedor nas tabelas usuario e fornecedor"""
        try:
            # Atualizar dados de usuario
            usuario_repo.atualizar_usuario(fornecedor)

            # Atualizar dados específicos de fornecedor
            return self.executar_comando(self.sql_module.ATUALIZAR, self._objeto_para_tupla_update(fornecedor))
        except Exception as e:
            self.logger.error(f"Erro ao atualizar {self.nome_tabela}: {e}")
            return False

    def excluir(self, id: int) -> bool:
        """Exclui fornecedor das tabelas fornecedor e usuario"""
        try:
            with self.obter_conexao() as conexao:
                cursor = conexao.cursor()
                # Primeiro excluir da tabela fornecedor
                cursor.execute(self.sql_module.EXCLUIR, (id,))
                # Depois excluir da tabela usuario na mesma conexão
                cursor.execute("DELETE FROM Usuario WHERE id = ?", (id,))
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao excluir {self.nome_tabela}: {e}")
            return False

    def obter_fornecedores_por_pagina(self, numero_pagina: int, tamanho_pagina: int) -> List[Fornecedor]:
        """Obtém fornecedores por página"""
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_query(fornecedor_sql.OBTER_FORNECEDORES_POR_PAGINA, (limite, offset))
        return [self._linha_para_objeto(dict(resultado)) for resultado in resultados]

    def contar_fornecedores(self) -> int:
        """Conta o total de fornecedores no sistema"""
        resultados = self.executar_query(fornecedor_sql.CONTAR_FORNECEDORES)
        return resultados[0]["total"] if resultados else 0

    def contar_fornecedores_nao_verificados(self) -> int:
        """Conta o total de fornecedores não verificados"""
        resultados = self.executar_query(fornecedor_sql.CONTAR_FORNECEDORES_NAO_VERIFICADOS)
        return resultados[0]["total"] if resultados else 0

    def rejeitar_fornecedor(self, id_fornecedor: int) -> bool:
        """Rejeita um fornecedor, removendo a verificação"""
        return self.executar_comando(fornecedor_sql.REJEITAR_FORNECEDOR, (id_fornecedor,))

# Instância global do repositório
fornecedor_repo = FornecedorRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_fornecedor() -> bool:
    return fornecedor_repo.criar_tabela()

def inserir_fornecedor(fornecedor: Fornecedor) -> Optional[int]:
    return fornecedor_repo.inserir(fornecedor)

def atualizar_fornecedor(fornecedor: Fornecedor) -> bool:
    return fornecedor_repo.atualizar(fornecedor)

def excluir_fornecedor(id: int) -> bool:
    return fornecedor_repo.excluir(id)

def obter_fornecedor_por_id(id: int) -> Optional[Fornecedor]:
    return fornecedor_repo.obter_por_id(id)

def obter_fornecedores_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Fornecedor]:
    return fornecedor_repo.obter_fornecedores_por_pagina(numero_pagina, tamanho_pagina)

def contar_fornecedores() -> int:
    return fornecedor_repo.contar_fornecedores()

def contar_fornecedores_nao_verificados() -> int:
    return fornecedor_repo.contar_fornecedores_nao_verificados()

def rejeitar_fornecedor(id_fornecedor: int) -> bool:
    return fornecedor_repo.rejeitar_fornecedor(id_fornecedor)
