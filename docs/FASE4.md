# 🧪 FASE 4: Simplificar e Organizar Estrutura de Testes

## 🎯 Objetivo Principal
Simplificar drasticamente a estrutura de testes usando Factory Pattern e eliminando as 310 linhas de fixtures repetitivas em `conftest.py`.

## 🔍 Análise do Problema Atual

### Problemas Identificados:
- **conftest.py gigantesco**: 310 linhas com fixtures muito similares
- **Padrão repetitivo**: Cada entidade tem fixture individual + fixture de lista
- **Dados hardcoded**: Valores fixos que dificultam testes variados
- **Manutenção difícil**: Mudança em um modelo quebra múltiplas fixtures
- **Falta de flexibilidade**: Fixtures muito específicas, pouco reutilizáveis

### Exemplo Atual em `conftest.py`:
```python
@pytest.fixture
def usuario_exemplo():
    from model.usuario_model import Usuario, TipoUsuario
    usuario = Usuario(0, "Usuário Teste", "123.456.789-00", "1990-01-01",
                     "usuario@email.com", "(28) 99999-0000", "123456",
                     TipoUsuario.ADMIN, None, None, None, None)
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    from model.usuario_model import Usuario, TipoUsuario
    tipos = [TipoUsuario.ADMIN, TipoUsuario.NOIVO, TipoUsuario.FORNECEDOR]
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"123.456.78{i:01d}-00",
                         f"199{i:01d}-01-01", f"usuario{i:02d}@email.com",
                         f"(28) 99999-00{i:02d}", "123456", tipos[i % 3],
                         None, None, None, None)
        usuarios.append(usuario)
    return usuarios

# ... Mais 20+ fixtures similares para cada modelo
```

## 💡 Solução Proposta

### 1. Criar Sistema de Factories

#### `tests/factories.py`:
```python
"""
Factories para criar objetos de teste de forma flexível e reutilizável.
Baseado no padrão Factory para reduzir código duplicado.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, TypeVar, Generic
from faker import Faker
import random

# Imports dos modelos
from model.usuario_model import Usuario, TipoUsuario
from model.fornecedor_model import Fornecedor
from model.categoria_model import Categoria
from model.item_model import Item
from model.tipo_fornecimento_model import TipoFornecimento

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')
Faker.seed(42)  # Para testes determinísticos

T = TypeVar('T')

class BaseFactory(Generic[T]):
    """Factory base com funcionalidades comuns"""

    @classmethod
    def criar(cls, **kwargs) -> T:
        """Cria uma instância com dados padrão + sobrescritas"""
        dados_padrao = cls._dados_padrao()
        dados_padrao.update(kwargs)
        return cls._construir_objeto(dados_padrao)

    @classmethod
    def criar_lista(cls, quantidade: int = 5, **kwargs_base) -> List[T]:
        """Cria uma lista de instâncias variadas"""
        objetos = []
        for i in range(quantidade):
            kwargs_item = kwargs_base.copy()
            kwargs_item.update(cls._variar_dados(i))
            objetos.append(cls.criar(**kwargs_item))
        return objetos

    @classmethod
    def criar_batch(cls, especificacoes: List[Dict[str, Any]]) -> List[T]:
        """Cria lista com especificações diferentes para cada item"""
        return [cls.criar(**spec) for spec in especificacoes]

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        """Dados padrão para criação - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _dados_padrao na classe filha")

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        """Variações nos dados para criar lista diversificada"""
        return {}

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> T:
        """Constrói o objeto final - deve ser sobrescrito"""
        raise NotImplementedError("Implemente _construir_objeto na classe filha")


class UsuarioFactory(BaseFactory[Usuario]):
    """Factory para criar usuários de teste"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'nome': fake.name(),
            'cpf': fake.cpf().replace('.', '').replace('-', ''),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'email': fake.email(),
            'telefone': fake.phone_number().replace(' ', '').replace('-', ''),
            'senha': fake.password(length=8),
            'perfil': TipoUsuario.NOIVO,
            'token_redefinicao': None,
            'data_token': None,
            'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ativo': True
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        """Cria variações nos dados para listas"""
        tipos = [TipoUsuario.ADMIN, TipoUsuario.NOIVO, TipoUsuario.FORNECEDOR]
        return {
            'id': indice + 1,
            'nome': fake.name(),
            'email': fake.unique.email(),
            'perfil': tipos[indice % len(tipos)]
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Usuario:
        return Usuario(**dados)

    @classmethod
    def criar_admin(cls, **kwargs) -> Usuario:
        """Shortcut para criar administrador"""
        kwargs.setdefault('perfil', TipoUsuario.ADMIN)
        kwargs.setdefault('nome', 'Admin Teste')
        kwargs.setdefault('email', 'admin@casebem.com')
        return cls.criar(**kwargs)

    @classmethod
    def criar_noivo(cls, **kwargs) -> Usuario:
        """Shortcut para criar noivo"""
        kwargs.setdefault('perfil', TipoUsuario.NOIVO)
        return cls.criar(**kwargs)

    @classmethod
    def criar_fornecedor_usuario(cls, **kwargs) -> Usuario:
        """Shortcut para criar usuário fornecedor"""
        kwargs.setdefault('perfil', TipoUsuario.FORNECEDOR)
        return cls.criar(**kwargs)


class FornecedorFactory(BaseFactory[Fornecedor]):
    """Factory para criar fornecedores de teste"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        # Herda dados de usuário e adiciona específicos de fornecedor
        dados_usuario = UsuarioFactory._dados_padrao()
        dados_usuario.update({
            'perfil': TipoUsuario.FORNECEDOR,
            'nome_empresa': fake.company(),
            'cnpj': fake.cnpj().replace('.', '').replace('/', '').replace('-', ''),
            'descricao': fake.text(max_nb_chars=200),
            'endereco': fake.address(),
            'verificado': False
        })
        return dados_usuario

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        return {
            'id': indice + 1,
            'nome': fake.name(),
            'email': fake.unique.email(),
            'nome_empresa': fake.company(),
            'verificado': indice % 3 == 0  # Alguns verificados
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Fornecedor:
        return Fornecedor(**dados)


class CategoriaFactory(BaseFactory[Categoria]):
    """Factory para criar categorias de teste"""

    NOMES_CATEGORIAS = [
        "Fotografia", "Buffet", "Decoração", "Música", "Floricultura",
        "Doces", "Bolo", "Vestidos", "Ternos", "Maquiagem",
        "Penteado", "Transporte", "Hospedagem", "Convites"
    ]

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'nome': random.choice(cls.NOMES_CATEGORIAS),
            'tipo_fornecimento': random.choice(list(TipoFornecimento)),
            'descricao': fake.text(max_nb_chars=100),
            'ativo': True
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        tipos = list(TipoFornecimento)
        return {
            'id': indice + 1,
            'nome': f"{cls.NOMES_CATEGORIAS[indice % len(cls.NOMES_CATEGORIAS)]} {indice + 1}",
            'tipo_fornecimento': tipos[indice % len(tipos)]
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Categoria:
        return Categoria(**dados)


class ItemFactory(BaseFactory[Item]):
    """Factory para criar itens de teste"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'id_fornecedor': 1,
            'tipo': random.choice(list(TipoFornecimento)),
            'nome': fake.word().title() + " Premium",
            'descricao': fake.text(max_nb_chars=200),
            'preco': Decimal(str(random.uniform(50.0, 5000.0))).quantize(Decimal('0.01')),
            'id_categoria': 1,
            'observacoes': fake.text(max_nb_chars=100) if random.choice([True, False]) else None,
            'ativo': True,
            'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        tipos = list(TipoFornecimento)
        return {
            'id': indice + 1,
            'id_fornecedor': (indice % 5) + 1,  # Distribui entre fornecedores
            'tipo': tipos[indice % len(tipos)],
            'nome': f"Item {indice + 1}",
            'preco': Decimal(str((indice + 1) * 100)).quantize(Decimal('0.01'))
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Item:
        return Item(**dados)


class TestDataBuilder:
    """
    Builder para criar conjuntos completos de dados de teste.
    Útil para testes de integração que precisam de dados relacionados.
    """

    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.fornecedores: List[Fornecedor] = []
        self.categorias: List[Categoria] = []
        self.itens: List[Item] = []

    def com_usuarios(self, quantidade: int = 5) -> 'TestDataBuilder':
        """Adiciona usuários variados"""
        self.usuarios = UsuarioFactory.criar_lista(quantidade)
        return self

    def com_fornecedores(self, quantidade: int = 3) -> 'TestDataBuilder':
        """Adiciona fornecedores"""
        self.fornecedores = FornecedorFactory.criar_lista(quantidade)
        return self

    def com_categorias(self, quantidade: int = 5) -> 'TestDataBuilder':
        """Adiciona categorias variadas"""
        self.categorias = CategoriaFactory.criar_lista(quantidade)
        return self

    def com_itens(self, quantidade: int = 10) -> 'TestDataBuilder':
        """Adiciona itens relacionados aos fornecedores"""
        if not self.fornecedores:
            self.com_fornecedores(3)

        self.itens = []
        for i in range(quantidade):
            fornecedor = self.fornecedores[i % len(self.fornecedores)]
            item = ItemFactory.criar(
                id_fornecedor=fornecedor.id or i + 1,
                nome=f"Item {i + 1} - {fornecedor.nome_empresa}"
            )
            self.itens.append(item)
        return self

    def construir(self) -> Dict[str, List]:
        """Retorna todos os dados criados"""
        return {
            'usuarios': self.usuarios,
            'fornecedores': self.fornecedores,
            'categorias': self.categorias,
            'itens': self.itens
        }
```

### 2. Simplificar conftest.py

#### Novo `tests/conftest.py` (Reduzido de 310 para ~60 linhas):
```python
"""
Configurações e fixtures básicas para testes.
Factories específicas estão em tests/factories.py
"""

import pytest
import os
import sys
import tempfile
from typing import Dict, Any

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.factories import (
    UsuarioFactory, FornecedorFactory, CategoriaFactory,
    ItemFactory, TestDataBuilder
)


@pytest.fixture
def test_db():
    """Cria um banco de dados temporário para testes"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path

    yield db_path

    # Cleanup
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def usuario_factory():
    """Factory para criar usuários nos testes"""
    return UsuarioFactory


@pytest.fixture
def fornecedor_factory():
    """Factory para criar fornecedores nos testes"""
    return FornecedorFactory


@pytest.fixture
def categoria_factory():
    """Factory para criar categorias nos testes"""
    return CategoriaFactory


@pytest.fixture
def item_factory():
    """Factory para criar itens nos testes"""
    return ItemFactory


@pytest.fixture
def test_data_builder():
    """Builder para criar conjuntos completos de dados"""
    return TestDataBuilder


@pytest.fixture
def dados_completos_teste(test_data_builder):
    """Conjunto completo de dados para testes de integração"""
    return test_data_builder.com_usuarios(5).com_fornecedores(3).com_categorias(5).com_itens(10).construir()


# Fixtures de conveniência (para compatibilidade com testes existentes)
@pytest.fixture
def usuario_exemplo(usuario_factory):
    """Usuário exemplo para compatibilidade"""
    return usuario_factory.criar()


@pytest.fixture
def admin_exemplo(usuario_factory):
    """Admin exemplo para compatibilidade"""
    return usuario_factory.criar_admin()


@pytest.fixture
def lista_usuarios_exemplo(usuario_factory):
    """Lista de usuários para compatibilidade"""
    return usuario_factory.criar_lista(10)
```

### 3. Exemplos de Testes Simplificados

#### `tests/test_usuario_repo_melhorado.py`:
```python
"""
Exemplo de teste usando factories - muito mais limpo e flexível
"""

import pytest
from repo.usuario_repo import UsuarioRepo
from util.exceptions import ValidacaoError, RecursoNaoEncontradoError


class TestUsuarioRepo:
    """Testes do repositório de usuários usando factories"""

    def test_inserir_usuario_sucesso(self, test_db, usuario_factory):
        """Teste de inserção bem-sucedida"""
        # Arrange
        repo = UsuarioRepo()
        repo.criar_tabela()
        usuario = usuario_factory.criar(nome="João Silva", email="joao@teste.com")

        # Act
        id_usuario = repo.inserir(usuario)

        # Assert
        assert id_usuario is not None
        assert id_usuario > 0

        # Verificar se foi realmente inserido
        usuario_inserido = repo.obter_por_id(id_usuario)
        assert usuario_inserido.nome == "João Silva"
        assert usuario_inserido.email == "joao@teste.com"

    def test_obter_usuario_inexistente(self, test_db, usuario_factory):
        """Teste de busca por usuário inexistente"""
        # Arrange
        repo = UsuarioRepo()
        repo.criar_tabela()

        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            repo.obter_por_id(999)

        assert "Usuário não encontrado" in str(exc_info.value)
        assert "999" in str(exc_info.value)

    def test_inserir_email_duplicado(self, test_db, usuario_factory):
        """Teste de inserção com email duplicado"""
        # Arrange
        repo = UsuarioRepo()
        repo.criar_tabela()

        email_duplicado = "duplicado@teste.com"
        usuario1 = usuario_factory.criar(email=email_duplicado)
        usuario2 = usuario_factory.criar(email=email_duplicado)

        # Act
        repo.inserir(usuario1)

        # Assert
        with pytest.raises(BancoDadosError) as exc_info:
            repo.inserir(usuario2)

        assert "já existe" in str(exc_info.value).lower()

    def test_listar_usuarios_com_filtros(self, test_db, usuario_factory):
        """Teste de listagem com diferentes filtros"""
        # Arrange
        repo = UsuarioRepo()
        repo.criar_tabela()

        # Criar usuários variados
        admin = usuario_factory.criar_admin()
        noivos = usuario_factory.criar_lista(3, perfil=TipoUsuario.NOIVO)
        fornecedores = usuario_factory.criar_lista(2, perfil=TipoUsuario.FORNECEDOR)

        # Inserir todos
        for usuario in [admin] + noivos + fornecedores:
            repo.inserir(usuario)

        # Act & Assert
        todos_usuarios = repo.listar_todos()
        assert len(todos_usuarios) == 6

        # Testar filtros específicos (assumindo que existam métodos)
        # admins = repo.listar_por_perfil(TipoUsuario.ADMIN)
        # assert len(admins) == 1

    @pytest.mark.parametrize("nome,email_valido,deve_passar", [
        ("João Silva", "joao@teste.com", True),
        ("", "email@teste.com", False),  # Nome vazio
        ("Maria", "email_inválido", False),  # Email inválido
        ("A" * 101, "teste@teste.com", False),  # Nome muito longo
    ])
    def test_validacao_dados_usuario(self, test_db, usuario_factory, nome, email_valido, deve_passar):
        """Teste parametrizado para validações"""
        # Arrange
        repo = UsuarioRepo()
        repo.criar_tabela()

        try:
            usuario = usuario_factory.criar(nome=nome, email=email_valido)
            # Act
            resultado = repo.inserir(usuario)
            # Assert
            if deve_passar:
                assert resultado is not None
            else:
                pytest.fail("Deveria ter falhado mas passou")
        except (ValidacaoError, ValueError):
            if deve_passar:
                pytest.fail("Deveria ter passado mas falharam")
            # Esperado falhar


class TestIntegracaoUsuarios:
    """Testes de integração usando TestDataBuilder"""

    def test_cenario_completo_casamento(self, test_db, test_data_builder):
        """Teste de um cenário completo do sistema"""
        # Arrange
        dados = test_data_builder.com_usuarios(2).com_fornecedores(3).com_categorias(2).com_itens(5).construir()

        # Simular criação de demandas, orçamentos, etc.
        # ... resto do teste de integração
```

### 4. Utilitários de Teste

#### `tests/test_helpers.py`:
```python
"""
Utilitários para facilitar escrita de testes
"""

from typing import Any, Dict, List
from contextlib import contextmanager

@contextmanager
def nao_deve_gerar_erro():
    """Context manager para garantir que não há erros"""
    try:
        yield
    except Exception as e:
        pytest.fail(f"Não deveria gerar erro, mas gerou: {e}")


def assert_objeto_possui_atributos(objeto: Any, atributos: Dict[str, Any]):
    """Verifica se objeto possui os atributos esperados"""
    for nome_attr, valor_esperado in atributos.items():
        assert hasattr(objeto, nome_attr), f"Objeto não possui atributo '{nome_attr}'"
        valor_atual = getattr(objeto, nome_attr)
        assert valor_atual == valor_esperado, f"Atributo '{nome_attr}': esperado {valor_esperado}, obtido {valor_atual}"


def assert_listas_equivalentes(lista1: List[Any], lista2: List[Any], comparar_por: str = 'id'):
    """Compara listas de objetos por um atributo específico"""
    ids1 = [getattr(obj, comparar_por) for obj in lista1]
    ids2 = [getattr(obj, comparar_por) for obj in lista2]
    assert set(ids1) == set(ids2), f"Listas não são equivalentes: {ids1} != {ids2}"
```

## 📊 Análise de Impacto

### Antes:
- **conftest.py**: 310 linhas de fixtures repetitivas
- **Dados fixos**: Dificulta testes variados
- **Manutenção custosa**: Mudanças quebram múltiplas fixtures
- **Testes limitados**: Difícil criar cenários específicos
- **Duplicação**: Mesmo padrão repetido 20+ vezes

### Depois:
- **conftest.py**: ~60 linhas focadas no essencial
- **factories.py**: ~200 linhas reutilizáveis
- **Total**: ~260 linhas vs 310 originais (**redução de 16%**)
- **Flexibilidade**: Dados dinâmicos e customizáveis
- **Cenários complexos**: TestDataBuilder para integração
- **Manutenção fácil**: Mudanças centralizadas

## 🎓 Conceitos Ensinados aos Alunos

1. **Factory Pattern**: Como criar objetos de forma flexível
2. **Builder Pattern**: Para construir cenários complexos
3. **Parametrized Tests**: Testar múltiplos casos com um teste
4. **Test Data Generation**: Faker para dados realistas
5. **Test Organization**: Como organizar testes limpos

## 📝 Passo a Passo da Implementação

### Passo 1: Criar Sistema de Factories
1. Implementar `tests/factories.py` com factories básicas
2. Começar com UsuarioFactory e CategoriaFactory
3. Testar factories isoladamente

### Passo 2: Simplificar conftest.py
1. Backup do conftest.py atual
2. Reescrever com factories
3. Manter fixtures de compatibilidade

### Passo 3: Migrar Testes Existentes
1. Escolher 2-3 arquivos de teste piloto
2. Reescrever usando factories
3. Verificar que todos passam

### Passo 4: Criar Testes Exemplares
1. Escrever testes modelo usando factories
2. Mostrar diferentes padrões (unit, integration, parametrized)
3. Documentar boas práticas

### Passo 5: Migração Completa
1. Migrar todos os testes restantes
2. Remover fixtures obsoletas
3. Adicionar documentação sobre factories

## ⚠️ Riscos e Mitigações

### Risco 1: Quebrar testes existentes
**Mitigação**: Manter fixtures de compatibilidade temporárias

### Risco 2: Factories muito complexas
**Mitigação**: Começar simples, adicionar complexidade gradualmente

### Risco 3: Dados de teste não realistas
**Mitigação**: Usar Faker com configuração brasileira

## ✅ Critérios de Sucesso

- [ ] Sistema de factories funcionando
- [ ] conftest.py reduzido significativamente
- [ ] 3+ arquivos de teste migrados
- [ ] Todos os testes passando
- [ ] Documentação de como usar factories

## 🔧 Ferramentas Adicionais

### Instalar Faker:
```bash
pip install faker
```

### Configuração no requirements.txt:
```txt
# Adicionar às dependências de teste
faker==19.6.2
```

## 🚀 Próximos Passos

Após completar a Fase 4:
- **Fase 5**: Limpeza final e organização do projeto

## 💬 Exemplo de Explicação para Alunos

> "Imaginem uma fábrica de carros: em vez de construir cada carro manualmente (fixtures), vocês têm uma linha de montagem (factory) que pode fazer carros diferentes apenas mudando algumas configurações. É mais eficiente e flexível!"

### Comparação Prática:

**Antes** (fixture tradicional):
```python
def test_usuario():
    usuario = Usuario(0, "João", "123", "1990-01-01", "joao@teste.com", ...)
    # Sempre os mesmos dados!
```

**Depois** (com factory):
```python
def test_usuario():
    usuario = UsuarioFactory.criar(nome="João")  # Outros dados gerados automaticamente
    # ou
    usuario = UsuarioFactory.criar_admin()  # Admin pronto
    # ou
    usuarios = UsuarioFactory.criar_lista(10)  # 10 usuários variados
```