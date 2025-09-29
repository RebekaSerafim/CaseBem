# 📚 FASE 1: Criar Classe Base para Repositórios

## 🎯 Objetivo Principal
Eliminar a duplicação de código nos repositórios criando uma classe base reutilizável que contenha toda a lógica CRUD comum.

## 🔍 Análise do Problema Atual

### Estatísticas de Duplicação:
- **12 repositórios** com código praticamente idêntico
- **129 ocorrências** de `with obter_conexao() as conexao:`
- **5 métodos repetidos** em cada repositório: criar_tabela, inserir, atualizar, excluir, obter_por_id
- **~60 linhas duplicadas** por repositório = **720 linhas totais** de código repetido

### Exemplo Atual (categoria_repo.py):
```python
def criar_tabela_categorias() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_CATEGORIA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categoria: {e}")
        return False

def inserir_categoria(categoria: Categoria) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_CATEGORIA,
            (categoria.nome, categoria.tipo_fornecimento.value, categoria.descricao, categoria.ativo))
        return cursor.lastrowid

def atualizar_categoria(categoria: Categoria) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_CATEGORIA,
            (categoria.nome, categoria.tipo_fornecimento.value, categoria.descricao, categoria.ativo, categoria.id))
        return (cursor.rowcount > 0)
```

## 💡 Solução Proposta

### 1. Criar `util/base_repo.py`:

```python
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
                # Converte objeto em tupla de valores
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

    # Métodos que devem ser sobrescritos nas classes filhas
    def _objeto_para_tupla_insert(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para INSERT - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_insert na classe filha")

    def _objeto_para_tupla_update(self, objeto: Any) -> tuple:
        """Converte objeto em tupla para UPDATE - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _objeto_para_tupla_update na classe filha")

    def _linha_para_objeto(self, linha: Dict) -> Any:
        """Converte linha do BD em objeto - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _linha_para_objeto na classe filha")
```

### 2. Refatorar `repo/categoria_repo.py` usando BaseRepo:

```python
from typing import Optional, List
from util.base_repo import BaseRepo
from sql import categoria_sql
from model.categoria_model import Categoria
from model.tipo_fornecimento_model import TipoFornecimento

class CategoriaRepo(BaseRepo):
    """Repositório para operações com categorias"""

    def __init__(self):
        super().__init__('categoria', Categoria, categoria_sql)

    def _objeto_para_tupla_insert(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para inserção"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo
        )

    def _objeto_para_tupla_update(self, categoria: Categoria) -> tuple:
        """Prepara dados da categoria para atualização"""
        return (
            categoria.nome,
            categoria.tipo_fornecimento.value,
            categoria.descricao,
            categoria.ativo,
            categoria.id
        )

    def _linha_para_objeto(self, linha: dict) -> Categoria:
        """Converte linha do banco em objeto Categoria"""
        return Categoria(
            id=linha["id"],
            nome=linha["nome"],
            tipo_fornecimento=TipoFornecimento(linha["tipo_fornecimento"]),
            descricao=linha["descricao"],
            ativo=bool(linha["ativo"])
        )

    def obter_por_tipo(self, tipo: TipoFornecimento) -> List[Categoria]:
        """Método específico: obter categorias por tipo"""
        resultados = self.executar_query(
            categoria_sql.OBTER_POR_TIPO,
            (tipo.value,)
        )
        return [self._linha_para_objeto(row) for row in resultados]

# Instância global do repositório
categoria_repo = CategoriaRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_categorias() -> bool:
    return categoria_repo.criar_tabela()

def inserir_categoria(categoria: Categoria) -> Optional[int]:
    return categoria_repo.inserir(categoria)

def atualizar_categoria(categoria: Categoria) -> bool:
    return categoria_repo.atualizar(categoria)

def excluir_categoria(id: int) -> bool:
    return categoria_repo.excluir(id)

def obter_categoria_por_id(id: int) -> Optional[Categoria]:
    return categoria_repo.obter_por_id(id)

def listar_categorias(ativo: Optional[bool] = None) -> List[Categoria]:
    return categoria_repo.listar_todos(ativo)

def obter_categorias_por_tipo(tipo: TipoFornecimento) -> List[Categoria]:
    return categoria_repo.obter_por_tipo(tipo)
```

## 📊 Análise de Impacto

### Antes:
- **12 arquivos** com ~80 linhas cada = **960 linhas totais**
- Código duplicado em cada repositório
- Mudanças precisam ser feitas em 12 lugares
- Alto risco de inconsistências

### Depois:
- **1 arquivo base** com 120 linhas
- **12 arquivos** com ~50 linhas cada = **600 linhas**
- **Total: 720 linhas** (redução de 25%)
- Mudanças centralizadas em um único lugar
- Consistência garantida

## 🎓 Conceitos Ensinados aos Alunos

1. **Herança de Classes**: Como reaproveitar código através de classes base
2. **Princípio DRY**: Don't Repeat Yourself - evitar duplicação
3. **Responsabilidade Única**: BaseRepo cuida apenas de operações CRUD
4. **Polimorfismo**: Métodos que podem ser sobrescritos quando necessário

## 📝 Passo a Passo da Implementação

### Passo 1: Criar a classe BaseRepo
1. Criar arquivo `util/base_repo.py`
2. Implementar métodos CRUD genéricos
3. Definir métodos abstratos para conversão de dados

### Passo 2: Refatorar um repositório piloto
1. Escolher `categoria_repo.py` como piloto
2. Criar classe `CategoriaRepo` herdando de `BaseRepo`
3. Implementar métodos de conversão específicos
4. Manter funções de compatibilidade

### Passo 3: Testar exaustivamente
1. Rodar todos os testes de categoria
2. Verificar se nada quebrou
3. Testar através da interface web

### Passo 4: Aplicar para outros repositórios
1. Refatorar `usuario_repo.py`
2. Refatorar `item_repo.py`
3. Continuar com os demais, um por vez

## ⚠️ Riscos e Mitigações

### Risco 1: Quebrar código existente
**Mitigação**: Manter funções de compatibilidade que chamam os novos métodos

### Risco 2: Complexidade para alunos
**Mitigação**: Documentar bem e fazer sessão explicativa sobre herança

### Risco 3: Casos especiais
**Mitigação**: Métodos específicos podem ser adicionados nas classes filhas

## ✅ Critérios de Sucesso

- [ ] BaseRepo criado e documentado
- [ ] Pelo menos 3 repositórios migrados
- [ ] Todos os testes passando
- [ ] Redução de pelo menos 200 linhas de código
- [ ] Alunos entendem o conceito de herança

## 🚀 Próximos Passos

Após completar a Fase 1, seguir para:
- **Fase 2**: Simplificar DTOs com classe base
- **Fase 3**: Centralizar tratamento de erros

## 💬 Exemplo de Explicação para Alunos

> "Imaginem que vocês têm 12 formulários diferentes, mas todos têm campos parecidos: nome, telefone, email. Em vez de escrever o código de validação 12 vezes, vocês criam um 'formulário base' com essas validações e os outros herdam dele. É exatamente isso que faremos com nossos repositórios!"