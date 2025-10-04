"""
Builders de dados para testes E2E
"""
from datetime import datetime, timedelta
from faker import Faker
import unicodedata

fake = Faker('pt_BR')

def remove_accents(text: str) -> str:
    """Remove acentos e caracteres especiais, mantendo apenas letras e espaços"""
    # Normaliza para separar caracteres base de acentos
    nfd = unicodedata.normalize('NFD', text)
    # Remove marcas diacríticas (acentos)
    without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
    # Remove caracteres que não são letras ou espaços
    return ''.join(char for char in without_accents if char.isalpha() or char.isspace())

class DemandaBuilder:
    """Builder para criar dados de demanda"""

    @staticmethod
    def build(titulo: str = None, descricao: str = None) -> dict:
        """
        Cria dados de demanda para testes

        Args:
            titulo: Título customizado (opcional)
            descricao: Descrição customizada (opcional)

        Returns:
            Dicionário com dados da demanda
        """
        return {
            "titulo": titulo or f"Demanda Teste - {fake.word().title()}",
            "descricao": descricao or fake.text(200),
            "data_necessaria": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "orcamento_estimado": f"{fake.random_int(500, 5000)}.00"
        }

class ItemBuilder:
    """Builder para criar dados de item"""

    @staticmethod
    def build(tipo: str = "PRODUTO", nome: str = None) -> dict:
        """
        Cria dados de item para testes

        Args:
            tipo: Tipo do item (PRODUTO, SERVICO, ESPACO)
            nome: Nome customizado (opcional)

        Returns:
            Dicionário com dados do item
        """
        return {
            "tipo": tipo,
            "nome": nome or f"Item Teste - {fake.word().title()}",
            "descricao": fake.text(150),
            "preco": f"{fake.random_int(50, 1000)}.00",
            "categoria": "1",  # Ajustar conforme categorias disponíveis
            "observacoes": fake.sentence()
        }

class OrcamentoBuilder:
    """Builder para criar dados de orçamento"""

    @staticmethod
    def build(valor: float = None, descricao: str = None) -> dict:
        """
        Cria dados de orçamento para testes

        Args:
            valor: Valor customizado (opcional)
            descricao: Descrição customizada (opcional)

        Returns:
            Dicionário com dados do orçamento
        """
        return {
            "valor": valor or f"{fake.random_int(1000, 10000)}.00",
            "descricao": descricao or fake.text(200),
            "prazo_entrega": f"{fake.random_int(7, 30)} dias",
            "forma_pagamento": fake.random_element(["À vista", "Parcelado", "Entrada + Saldo"])
        }

class NoivosBuilder:
    """Builder para cadastro de noivos"""

    @staticmethod
    def build() -> dict:
        """
        Cria dados completos para cadastro de casal

        Returns:
            Dicionário com dados dos dois noivos e do casamento
        """
        # Senha forte que atende aos requisitos: min 8 caracteres, maiúscula, minúscula, número, caractere especial
        senha = "TestE2e@2024"

        # Gerar telefones no formato brasileiro
        telefone1 = f"({fake.random_int(11, 99)}) {fake.random_int(90000, 99999)}-{fake.random_int(1000, 9999)}"
        telefone2 = f"({fake.random_int(11, 99)}) {fake.random_int(90000, 99999)}-{fake.random_int(1000, 9999)}"

        return {
            # Noivo 1 - nomes sem acentos para passar validação
            "nome1": remove_accents(fake.name()),
            "email1": fake.email(),
            "telefone1": telefone1,
            "cpf1": fake.cpf(),
            "data_nascimento1": fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            "genero1": "masculino",  # Usar valor lowercase que corresponde ao value do radio

            # Noivo 2 - nomes sem acentos para passar validação
            "nome2": remove_accents(fake.name()),
            "email2": fake.email(),
            "telefone2": telefone2,
            "cpf2": fake.cpf(),
            "data_nascimento2": fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            "genero2": "feminino",  # Usar valor lowercase que corresponde ao value do radio

            # Dados do casamento (todos opcionais, deixar vazios para evitar problemas)
            "data_casamento": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
            "local_previsto": remove_accents(fake.city()),
            "numero_convidados": str(fake.random_int(50, 300)),

            # Senha
            "senha": senha,
            "confirmar_senha": senha
        }

class FornecedorBuilder:
    """Builder para cadastro de fornecedor"""

    @staticmethod
    def build(tipo: str = "PRODUTO") -> dict:
        """
        Cria dados completos para cadastro de fornecedor

        Args:
            tipo: Tipo de fornecimento (PRODUTO, SERVICO, ESPACO)

        Returns:
            Dicionário com dados do fornecedor
        """
        senha = "TestE2e@2024"
        return {
            "nome": fake.company(),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "cnpj": fake.cnpj(),
            "tipo_fornecimento": tipo,
            "descricao": fake.text(200),
            "endereco": fake.address(),
            "cidade": fake.city(),
            "estado": fake.estado_sigla(),
            "senha": senha,
            "confirmar_senha": senha
        }

class CategoriaBuilder:
    """Builder para criação de categorias"""

    @staticmethod
    def build(tipo: str = "PRODUTO", nome: str = None) -> dict:
        """
        Cria dados de categoria para testes

        Args:
            tipo: Tipo da categoria (PRODUTO, SERVICO, ESPACO)
            nome: Nome customizado (opcional)

        Returns:
            Dicionário com dados da categoria
        """
        return {
            "nome": nome or f"Categoria {fake.word().title()}",
            "descricao": fake.text(100),
            "tipo_fornecimento": tipo,
            "ativo": "true"
        }
