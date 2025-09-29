from typing import Optional, List, Any, Dict
from util.database import obter_conexao

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

    def criar_tabela(self) -> bool:
        """Cria a tabela se não existir"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(self.sql.CRIAR_TABELA)
                return True
        except Exception as e:
            print(f"Erro ao criar tabela {self.nome_tabela}: {e}")
            return False

    def inserir(self, objeto: Any) -> Optional[int]:
        """Insere um novo registro e retorna o ID"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                valores = self._objeto_para_tupla_insert(objeto)
                cursor.execute(self.sql.INSERIR, valores)
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir em {self.nome_tabela}: {e}")
            return None

    def atualizar(self, objeto: Any) -> bool:
        """Atualiza um registro existente"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                valores = self._objeto_para_tupla_update(objeto)
                cursor.execute(self.sql.ATUALIZAR, valores)
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar em {self.nome_tabela}: {e}")
            return False

    def excluir(self, id: int) -> bool:
        """Exclui um registro pelo ID"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(self.sql.EXCLUIR, (id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir de {self.nome_tabela}: {e}")
            return False

    def obter_por_id(self, id: int) -> Optional[Any]:
        """Obtém um registro pelo ID"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(self.sql.OBTER_POR_ID, (id,))
                resultado = cursor.fetchone()
                if resultado:
                    return self._linha_para_objeto(resultado)
        except Exception as e:
            print(f"Erro ao obter de {self.nome_tabela}: {e}")
        return None

    def listar_todos(self, ativo: Optional[bool] = None) -> List[Any]:
        """Lista todos os registros"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                if ativo is not None and hasattr(self.sql, 'LISTAR_ATIVOS'):
                    cursor.execute(self.sql.LISTAR_ATIVOS if ativo else self.sql.LISTAR_INATIVOS)
                else:
                    cursor.execute(self.sql.LISTAR_TODOS)

                resultados = cursor.fetchall()
                return [self._linha_para_objeto(row) for row in resultados]
        except Exception as e:
            print(f"Erro ao listar de {self.nome_tabela}: {e}")
            return []

    def executar_query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Executa uma query customizada"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar query em {self.nome_tabela}: {e}")
            return []

    def executar_comando(self, sql: str, params: tuple = ()) -> bool:
        """Executa um comando SQL (UPDATE, DELETE) e retorna se afetou linhas"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao executar comando em {self.nome_tabela}: {e}")
            return False

    def _objeto_para_tupla_insert(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para INSERT - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_insert na classe filha")

    def _objeto_para_tupla_update(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para UPDATE - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_update na classe filha")

    def _linha_para_objeto(self, linha: Dict) -> Any:
        """Converte linha do BD em objeto - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _linha_para_objeto na classe filha")