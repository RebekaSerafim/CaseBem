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
from core.models.usuario_model import Usuario, TipoUsuario
from core.models.fornecedor_model import Fornecedor
from core.models.categoria_model import Categoria
from core.models.item_model import Item
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.models.casal_model import Casal
from core.models.demanda_model import Demanda, StatusDemanda
from core.models.orcamento_model import Orcamento
from core.models.item_demanda_model import ItemDemanda
from core.models.item_orcamento_model import ItemOrcamento

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
            'verificado': False,
            'data_verificacao': None,
            'newsletter': random.choice([True, False])
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
            'preco': float(random.uniform(50.0, 5000.0)),  # Usar float em vez de Decimal para SQLite
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
            'preco': float((indice + 1) * 100)
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Item:
        return Item(**dados)


class CasalFactory(BaseFactory[Casal]):
    """Factory para criar casais de teste"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'id_noivo1': 1,
            'id_noivo2': 2,
            'data_casamento': fake.date_between(start_date='+30d', end_date='+2y').strftime('%Y-%m-%d'),
            'local_previsto': fake.city(),
            'orcamento_estimado': random.choice(['10k_25k', '25k_50k', '50k_100k', '100k_mais']),
            'numero_convidados': random.randint(50, 300)
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        return {
            'id': indice + 1,
            'id_noivo1': (indice * 2) + 1,
            'id_noivo2': (indice * 2) + 2,
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Casal:
        return Casal(**dados)


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
        self.casais: List[Casal] = []

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

    def com_casais(self, quantidade: int = 2) -> 'TestDataBuilder':
        """Adiciona casais"""
        if len(self.usuarios) < quantidade * 2:
            self.com_usuarios(quantidade * 2)

        self.casais = CasalFactory.criar_lista(quantidade)
        return self

    def construir(self) -> Dict[str, List]:
        """Retorna todos os dados criados"""
        return {
            'usuarios': self.usuarios,
            'fornecedores': self.fornecedores,
            'categorias': self.categorias,
            'itens': self.itens,
            'casais': self.casais
        }


class DemandaFactory(BaseFactory[Demanda]):
    """Factory para criar demandas de teste (V2: com descrição livre, sem id_categoria)"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'id_casal': 1,
            'descricao': fake.text(max_nb_chars=200),
            'orcamento_total': round(random.uniform(1000, 10000), 2),
            'data_casamento': fake.future_date(end_date='+365d').strftime('%Y-%m-%d'),
            'cidade_casamento': fake.city(),
            'prazo_entrega': fake.future_date(end_date='+30d').strftime('%Y-%m-%d'),
            'status': StatusDemanda.ATIVA,
            'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'observacoes': fake.text(max_nb_chars=100) if random.choice([True, False]) else None
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        """Cria variações nos dados para listas"""
        status_list = list(StatusDemanda)
        return {
            'id': indice + 1,
            'id_casal': (indice % 5) + 1,
            'descricao': fake.text(max_nb_chars=200),
            'cidade_casamento': fake.city(),
            'status': status_list[indice % len(status_list)]
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Demanda:
        return Demanda(**dados)


class OrcamentoFactory(BaseFactory[Orcamento]):
    """Factory para criar orçamentos de teste"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,
            'id_demanda': 1,
            'id_fornecedor_prestador': 2,  # Assumindo que fornecedor tem ID > 1
            'data_hora_cadastro': datetime.now(),
            'data_hora_validade': fake.future_datetime(end_date='+15d'),
            'status': 'PENDENTE',
            'observacoes': fake.text(max_nb_chars=100) if random.choice([True, False]) else None,
            'valor_total': round(random.uniform(1000, 8000), 2),
            'demanda': None,  # Será preenchido conforme necessário
            'fornecedor_prestador': None  # Será preenchido conforme necessário
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        """Cria variações nos dados para listas"""
        status_list = ['PENDENTE', 'ACEITO', 'REJEITADO']
        return {
            'id': indice + 1,
            'id_demanda': (indice % 5) + 1,
            'id_fornecedor_prestador': (indice % 3) + 2,  # Varia entre fornecedores
            'status': status_list[indice % len(status_list)],
            'valor_total': round(random.uniform(1000 + indice*100, 8000 + indice*200), 2)
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> Orcamento:
        return Orcamento(**dados)


class ItemDemandaFactory(BaseFactory[ItemDemanda]):
    """Factory para criar itens de demanda de teste (V2: descrição livre, sem id_item)"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        tipos = list(TipoFornecimento)
        return {
            'id': 0,
            'id_demanda': 1,
            'tipo': random.choice(tipos),
            'id_categoria': 1,
            'descricao': fake.text(max_nb_chars=150),
            'quantidade': random.randint(1, 10),
            'preco_maximo': round(random.uniform(50, 500), 2) if random.choice([True, False]) else None,
            'observacoes': fake.text(max_nb_chars=100) if random.choice([True, False]) else None
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        tipos = list(TipoFornecimento)
        return {
            'id': indice + 1,
            'id_demanda': (indice % 3) + 1,
            'tipo': tipos[indice % len(tipos)],
            'id_categoria': (indice % 10) + 1,
            'descricao': fake.text(max_nb_chars=150),
            'quantidade': indice + 1,
            'preco_maximo': round(random.uniform(100 + indice*20, 500 + indice*20), 2)
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> ItemDemanda:
        return ItemDemanda(**dados)


class ItemOrcamentoFactory(BaseFactory[ItemOrcamento]):
    """Factory para criar associações item-orçamento de teste (V2: com id_item_demanda)"""

    @classmethod
    def _dados_padrao(cls) -> Dict[str, Any]:
        return {
            'id': 0,  # Será gerado automaticamente pelo banco
            'id_orcamento': 1,
            'id_item_demanda': 1,
            'id_item': 1,
            'quantidade': random.randint(1, 10),
            'preco_unitario': round(random.uniform(50, 500), 2),
            'observacoes': fake.text(max_nb_chars=100) if random.choice([True, False]) else None,
            'desconto': round(random.uniform(0, 50), 2)
        }

    @classmethod
    def _variar_dados(cls, indice: int) -> Dict[str, Any]:
        return {
            'id': 0,  # Será gerado automaticamente
            'id_orcamento': (indice % 3) + 1,
            'id_item_demanda': (indice % 5) + 1,
            'id_item': (indice % 5) + 1,
            'quantidade': indice + 1,
            'preco_unitario': round(random.uniform(50 + indice*10, 500 + indice*10), 2),
            'desconto': round(random.uniform(0, 20), 2)
        }

    @classmethod
    def _construir_objeto(cls, dados: Dict[str, Any]) -> ItemOrcamento:
        return ItemOrcamento(**dados)