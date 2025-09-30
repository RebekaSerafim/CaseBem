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

    @staticmethod
    def _safe_get(row: Dict[str, Any], key: str, default: Any = None) -> Any:
        """
        Obtém valor de uma linha do banco de forma segura.
        Funciona com sqlite3.Row e dict.

        Args:
            row: Linha retornada do banco (sqlite3.Row ou dict)
            key: Chave a buscar
            default: Valor padrão se chave não existir ou for None

        Returns:
            Valor da chave ou default
        """
        try:
            return row[key] if row[key] is not None else default
        except (KeyError, IndexError):
            return default

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
                raise BancoDadosError(
                    "Falha ao obter ID do registro inserido", "inserção"
                )

            logger.info(
                f"Registro inserido em {self.nome_tabela}", id_inserido=id_inserido
            )
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
                logger.info(
                    f"Registro atualizado em {self.nome_tabela}",
                    id_objeto=getattr(objeto, "id", "unknown"),
                )
            else:
                logger.warning(
                    f"Nenhum registro foi atualizado em {self.nome_tabela}",
                    id_objeto=getattr(objeto, "id", "unknown"),
                )

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
                logger.warning(
                    f"Nenhum registro foi excluído de {self.nome_tabela}", id=id
                )

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
                    recurso=self.nome_tabela.title(), identificador=id
                )

            return self._linha_para_objeto(resultado)

    @tratar_erro_banco_dados("listagem de registros")
    def listar_todos(self, ativo: Optional[bool] = None) -> List[Any]:
        """Lista todos os registros"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            if ativo is not None and hasattr(self.sql, "LISTAR_ATIVOS"):
                cursor.execute(
                    self.sql.LISTAR_ATIVOS if ativo else self.sql.LISTAR_INATIVOS
                )
            else:
                cursor.execute(self.sql.LISTAR_TODOS)

            resultados = cursor.fetchall()
            logger.info(
                f"Listagem realizada em {self.nome_tabela}",
                total_registros=len(resultados),
                filtro_ativo=ativo,
            )
            return [self._linha_para_objeto(row) for row in resultados]

    @tratar_erro_banco_dados("execução de query")
    def executar_query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Executa uma query customizada"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            resultados = cursor.fetchall()
            logger.info(
                f"Query executada em {self.nome_tabela}",
                total_resultados=len(resultados),
            )
            return resultados

    @tratar_erro_banco_dados("execução de comando")
    def executar_comando(self, sql: str, params: tuple = ()) -> bool:
        """Executa um comando SQL (UPDATE, DELETE) e retorna se afetou linhas"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            afetado = cursor.rowcount > 0
            logger.info(
                f"Comando executado em {self.nome_tabela}",
                linhas_afetadas=cursor.rowcount,
            )
            return afetado

    def _objeto_para_tupla_insert(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para INSERT - deve ser sobrescrito"""
        raise NotImplementedError(
            "Implemente _objeto_para_tupla_insert na classe filha"
        )

    def _objeto_para_tupla_update(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para UPDATE - deve ser sobrescrito"""
        raise NotImplementedError(
            "Implemente _objeto_para_tupla_update na classe filha"
        )

    def _linha_para_objeto(self, linha: Dict) -> Any:
        """Converte linha do BD em objeto - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _linha_para_objeto na classe filha")

    @tratar_erro_banco_dados("contagem de registros")
    def contar_registros(self, condicao: str = "", parametros: tuple = ()) -> int:
        """Conta o total de registros na tabela, opcionalmente com condição WHERE"""
        if condicao:
            sql = f"SELECT COUNT(*) as total FROM {self.nome_tabela} WHERE {condicao}"
        else:
            sql = f"SELECT COUNT(*) as total FROM {self.nome_tabela}"

        resultados = self.executar_query(sql, parametros)
        total = resultados[0]["total"] if resultados else 0
        logger.info(
            f"Contagem realizada em {self.nome_tabela}",
            total_registros=total,
            condicao=condicao or None,
        )
        return total

    @tratar_erro_banco_dados("paginação de registros")
    def obter_paginado(
        self, pagina: int, tamanho_pagina: int, ordenacao: str = "id DESC"
    ) -> tuple[List[Any], int]:
        """Obtém registros paginados e retorna lista de objetos e total de registros"""
        total = self.contar_registros()

        offset = (pagina - 1) * tamanho_pagina
        sql = f"SELECT * FROM {self.nome_tabela} ORDER BY {ordenacao} LIMIT ? OFFSET ?"
        resultados = self.executar_query(sql, (tamanho_pagina, offset))

        objetos = [self._linha_para_objeto(row) for row in resultados]
        logger.info(
            f"Paginação realizada em {self.nome_tabela}",
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            total_registros=total,
        )
        return objetos, total

    def contar(self) -> int:
        """
        Alias para contar_registros() - mantém compatibilidade com API existente

        Returns:
            int: Total de registros na tabela
        """
        return self.contar_registros()

    @tratar_erro_banco_dados("ativação de registro")
    def ativar(self, id: int, campo: str = "ativo") -> bool:
        """
        Ativa um registro (soft delete pattern)

        Args:
            id: ID do registro
            campo: Nome do campo booleano (padrão: 'ativo')

        Returns:
            bool: True se ativado com sucesso
        """
        sql = f"UPDATE {self.nome_tabela} SET {campo} = 1 WHERE id = ?"
        sucesso = self.executar_comando(sql, (id,))
        if sucesso:
            logger.info(f"Registro ativado em {self.nome_tabela}", id=id, campo=campo)
        return sucesso

    @tratar_erro_banco_dados("desativação de registro")
    def desativar(self, id: int, campo: str = "ativo") -> bool:
        """
        Desativa um registro (soft delete pattern)

        Args:
            id: ID do registro
            campo: Nome do campo booleano (padrão: 'ativo')

        Returns:
            bool: True se desativado com sucesso
        """
        sql = f"UPDATE {self.nome_tabela} SET {campo} = 0 WHERE id = ?"
        sucesso = self.executar_comando(sql, (id,))
        if sucesso:
            logger.info(
                f"Registro desativado em {self.nome_tabela}", id=id, campo=campo
            )
        return sucesso


class BaseRepoChaveComposta:
    """
    Classe base para repositórios com chave primária composta.
    Para tabelas que não têm um ID autoincrement único.
    """

    def __init__(
        self, nome_tabela: str, model_class: type, sql_module, campos_chave: List[str]
    ):
        """
        Inicializa o repositório base para chave composta

        Args:
            nome_tabela: Nome da tabela no banco
            model_class: Classe do modelo
            sql_module: Módulo com as queries SQL
            campos_chave: Lista dos campos que formam a chave primária
        """
        self.nome_tabela = nome_tabela
        self.model_class = model_class
        self.sql = sql_module
        self.campos_chave = campos_chave

    @staticmethod
    def _safe_get(row: Dict[str, Any], key: str, default: Any = None) -> Any:
        """
        Obtém valor de uma linha do banco de forma segura.
        Funciona com sqlite3.Row e dict.

        Args:
            row: Linha retornada do banco (sqlite3.Row ou dict)
            key: Chave a buscar
            default: Valor padrão se chave não existir ou for None

        Returns:
            Valor da chave ou default
        """
        try:
            return row[key] if row[key] is not None else default
        except (KeyError, IndexError):
            return default

    @tratar_erro_banco_dados("criação de tabela")
    def criar_tabela(self) -> bool:
        """Cria a tabela se não existir"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.CRIAR_TABELA)
            logger.info(f"Tabela {self.nome_tabela} criada/verificada com sucesso")
            return True

    @tratar_erro_banco_dados("inserção de registro")
    def inserir(self, objeto: Any) -> bool:
        """Insere um novo registro (chave composta não retorna ID)"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_insert(objeto)
            cursor.execute(self.sql.INSERIR, valores)
            sucesso = cursor.rowcount > 0

            if sucesso:
                logger.info(
                    f"Registro inserido em {self.nome_tabela}",
                    chave_valores=valores[: len(self.campos_chave)],
                )
            return sucesso

    @tratar_erro_banco_dados("atualização de registro")
    def atualizar(self, objeto: Any) -> bool:
        """Atualiza um registro existente pela chave composta"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            valores = self._objeto_para_tupla_update(objeto)
            cursor.execute(self.sql.ATUALIZAR, valores)
            atualizado = cursor.rowcount > 0

            if atualizado:
                logger.info(f"Registro atualizado em {self.nome_tabela}")
            else:
                logger.warning(f"Nenhum registro foi atualizado em {self.nome_tabela}")

            return atualizado

    @tratar_erro_banco_dados("exclusão de registro")
    def excluir(self, *chave_valores) -> bool:
        """Exclui um registro pela chave composta"""
        if len(chave_valores) != len(self.campos_chave):
            raise ValidacaoError(
                f"Esperado {len(self.campos_chave)} valores para chave composta, recebido {len(chave_valores)}"
            )

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.EXCLUIR, chave_valores)
            excluido = cursor.rowcount > 0

            if excluido:
                logger.info(
                    f"Registro excluído de {self.nome_tabela}",
                    chave_valores=chave_valores,
                )
            else:
                logger.warning(
                    f"Nenhum registro foi excluído de {self.nome_tabela}",
                    chave_valores=chave_valores,
                )

            return excluido

    @tratar_erro_banco_dados("obtenção por chave")
    def obter_por_chave(self, *chave_valores) -> Any:
        """Obtém um registro pela chave composta"""
        if len(chave_valores) != len(self.campos_chave):
            raise ValidacaoError(
                f"Esperado {len(self.campos_chave)} valores para chave composta, recebido {len(chave_valores)}"
            )

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.OBTER_POR_CHAVE, chave_valores)
            resultado = cursor.fetchone()

            if not resultado:
                raise RecursoNaoEncontradoError(
                    recurso=self.nome_tabela.title(), identificador=str(chave_valores)
                )

            return self._linha_para_objeto(resultado)

    @tratar_erro_banco_dados("listagem de registros")
    def listar_todos(self) -> List[Any]:
        """Lista todos os registros"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(self.sql.LISTAR_TODOS)
            resultados = cursor.fetchall()
            logger.info(
                f"Listagem realizada em {self.nome_tabela}",
                total_registros=len(resultados),
            )
            return [self._linha_para_objeto(row) for row in resultados]

    @tratar_erro_banco_dados("execução de query")
    def executar_consulta(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Executa uma query customizada"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            resultados = cursor.fetchall()
            logger.info(
                f"Query executada em {self.nome_tabela}",
                total_resultados=len(resultados),
            )
            return resultados

    @tratar_erro_banco_dados("execução de comando")
    def executar_comando(self, sql: str, params: tuple = ()) -> bool:
        """Executa um comando SQL (UPDATE, DELETE) e retorna se afetou linhas"""
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, params)
            afetado = cursor.rowcount > 0
            logger.info(
                f"Comando executado em {self.nome_tabela}",
                linhas_afetadas=cursor.rowcount,
            )
            return afetado

    def _objeto_para_tupla_insert(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para INSERT - deve ser sobrescrito"""
        raise NotImplementedError(
            "Implemente _objeto_para_tupla_insert na classe filha"
        )

    def _objeto_para_tupla_update(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para UPDATE - deve ser sobrescrito"""
        raise NotImplementedError(
            "Implemente _objeto_para_tupla_update na classe filha"
        )

    def _linha_para_objeto(self, linha: Dict) -> Any:
        """Converte linha do BD em objeto - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _linha_para_objeto na classe filha")