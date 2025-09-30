from typing import Optional, List, Any, Dict
from util.database import obter_conexao
from util.error_handlers import tratar_erro_banco_dados, validar_parametros
from util.exceptions import RecursoNaoEncontradoError, BancoDadosError, ValidacaoError
from util.logger import logger

class BaseRepo:
    """
    Classe base para todos os repositórios.
    Fornece operações CRUD básicas que podem ser reutilizadas.
    """

    def __init__(self, nome_tabela: str, model_class: type, sql_module):
        """
        Inicializa o repositório base

        Args:
            nome_tabela: Nome da tabela no banco
            model_class: Classe do modelo (ex: Usuario, Categoria)
            sql_module: Módulo com as queries SQL
        """
        self.nome_tabela = nome_tabela
        self.model_class = model_class
        self.sql = sql_module

    @tratar_erro_banco_dados("criação de tabela")
    def criar_tabela(self) -> bool:
        """Cria a tabela se não existir"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.CRIAR_TABELA)
            logger.info(f"Tabela {self.nome_tabela} criada/verificada com sucesso")
            return True

    @tratar_erro_banco_dados("inserção de registro")
    def inserir(self, objeto: Any) -> int:
        """Insere um novo registro e retorna o ID"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_insert(objeto)
            cursor.execute(self.sql.INSERIR, valores)
            id_inserido = cursor.lastrowid

            if not id_inserido:
                raise BancoDadosError("Falha ao obter ID do registro inserido", "inserção")

            logger.info(f"Registro inserido em {self.nome_tabela}",
                       id_inserido=id_inserido)
            return id_inserido

    @tratar_erro_banco_dados("atualização de registro")
    def atualizar(self, objeto: Any) -> bool:
        """Atualiza um registro existente"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_update(objeto)
            cursor.execute(self.sql.ATUALIZAR, valores)
            atualizado = cursor.rowcount > 0

            if atualizado:
                logger.info(f"Registro atualizado em {self.nome_tabela}",
                           id_objeto=getattr(objeto, 'id', 'unknown'))
            else:
                logger.warning(f"Nenhum registro foi atualizado em {self.nome_tabela}",
                              id_objeto=getattr(objeto, 'id', 'unknown'))

            return atualizado

    @tratar_erro_banco_dados("exclusão de registro")
    @validar_parametros(int)
    def excluir(self, id: int) -> bool:
        """Exclui um registro pelo ID"""
        if id <= 0:
            raise ValidacaoError("ID deve ser um número positivo", "id", id)

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.EXCLUIR, (id,))
            excluido = cursor.rowcount > 0

            if excluido:
                logger.info(f"Registro excluído de {self.nome_tabela}", id_excluido=id)
            else:
                logger.warning(f"Nenhum registro foi excluído de {self.nome_tabela}", id=id)

            return excluido

    @tratar_erro_banco_dados("obtenção por ID")
    @validar_parametros(int)
    def obter_por_id(self, id: int) -> Any:
        """Obtém um registro pelo ID"""
        if id <= 0:
            raise ValidacaoError("ID deve ser um número positivo", "id", id)

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.OBTER_POR_ID, (id,))
            resultado = cursor.fetchone()

            if not resultado:
                raise RecursoNaoEncontradoError(
                    recurso=self.nome_tabela.title(),
                    identificador=id
                )

            return self._linha_para_objeto(resultado)

    @tratar_erro_banco_dados("listagem de registros")
    def listar_todos(self, ativo: Optional[bool] = None) -> List[Any]:
        """Lista todos os registros"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            if ativo is not None and hasattr(self.sql, 'LISTAR_ATIVOS'):
                cursor.execute(self.sql.LISTAR_ATIVOS if ativo else self.sql.LISTAR_INATIVOS)
            else:
                cursor.execute(self.sql.LISTAR_TODOS)

            resultados = cursor.fetchall()
            logger.info(f"Listagem realizada em {self.nome_tabela}",
                       total_registros=len(resultados), filtro_ativo=ativo)
            return [self._linha_para_objeto(row) for row in resultados]

    @tratar_erro_banco_dados("execução de query")
    def executar_query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Executa uma query customizada"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            resultados = cursor.fetchall()
            logger.info(f"Query executada em {self.nome_tabela}",
                       total_resultados=len(resultados))
            return resultados

    @tratar_erro_banco_dados("execução de comando")
    def executar_comando(self, sql: str, params: tuple = ()) -> bool:
        """Executa um comando SQL (UPDATE, DELETE) e retorna se afetou linhas"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            afetado = cursor.rowcount > 0
            logger.info(f"Comando executado em {self.nome_tabela}",
                       linhas_afetadas=cursor.rowcount)
            return afetado

    def _objeto_para_tupla_insert(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para INSERT - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_insert na classe filha")

    def _objeto_para_tupla_update(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para UPDATE - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_update na classe filha")

    def _linha_para_objeto(self, linha: Dict) -> Any:
        """Converte linha do BD em objeto - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _linha_para_objeto na classe filha")