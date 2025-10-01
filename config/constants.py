"""
Constantes do sistema CaseBem.

Centraliza valores que estavam hardcoded espalhados pelo código.
"""

from enum import Enum


class ImageConstants:
    """Constantes para processamento de imagens"""

    # Tamanho máximo de arquivo
    MAX_SIZE_MB = 5
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

    # Tipos de arquivo permitidos
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    # Qualidade de compressão JPEG
    QUALITY = 85

    class Sizes(Enum):
        """Tamanhos padrão de imagens"""
        AVATAR = (300, 300)
        ITEM = (600, 600)
        THUMBNAIL = (150, 150)
        BANNER = (1200, 400)


class PaginationConstants:
    """Constantes para paginação"""

    # Tamanho padrão de página (admin)
    DEFAULT_PAGE_SIZE = 10

    # Tamanho de página para listagens públicas (mais visual)
    PUBLIC_PAGE_SIZE = 12

    # Tamanho máximo permitido
    MAX_PAGE_SIZE = 100

    # Número máximo de links de página para exibir
    MAX_PAGE_LINKS = 10


class ValidationConstants:
    """Constantes para validações"""

    # Senha
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 100

    # Nome
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 100

    # Email
    MAX_EMAIL_LENGTH = 255

    # Telefone
    MIN_PHONE_DIGITS = 10
    MAX_PHONE_DIGITS = 11

    # CPF
    CPF_LENGTH = 11

    # Endereço
    MAX_ADDRESS_LENGTH = 200
    MAX_CITY_LENGTH = 100
    MAX_STATE_LENGTH = 2
    CEP_LENGTH = 8

    # Descrições
    MAX_SHORT_DESCRIPTION_LENGTH = 255
    MAX_LONG_DESCRIPTION_LENGTH = 5000


class DatabaseConstants:
    """Constantes para banco de dados"""

    # Timeout padrão para operações (segundos)
    DEFAULT_TIMEOUT = 30

    # Tamanho máximo de lote para operações em massa
    MAX_BATCH_SIZE = 1000


class BusinessConstants:
    """Constantes de regras de negócio"""

    # Tipos de usuário
    class TipoUsuario:
        ADMIN = 1
        FORNECEDOR = 2
        NOIVO = 3

    # Status de orçamento
    class StatusOrcamento:
        PENDENTE = "pendente"
        ACEITO = "aceito"
        REJEITADO = "rejeitado"
        CANCELADO = "cancelado"

    # Status de demanda
    class StatusDemanda:
        ABERTA = "aberta"
        EM_ANDAMENTO = "em_andamento"
        CONCLUIDA = "concluida"
        CANCELADA = "cancelada"

    # Tipos de item
    class TipoItem:
        PRODUTO = "produto"
        SERVICO = "servico"


class FileConstants:
    """Constantes para gerenciamento de arquivos"""

    # Diretórios base
    STATIC_DIR = "static"
    UPLOAD_DIR = "static/uploads"
    IMG_DIR = "static/img"

    # Subdiretórios de imagens
    USUARIOS_DIR = "static/img/usuarios"
    ITENS_DIR = "static/img/itens"

    # URLs base
    STATIC_URL = "/static"
    IMG_URL = "/static/img"

    # Arquivos padrão
    DEFAULT_USER_AVATAR = "/static/img/user-default.svg"
    DEFAULT_ITEM_IMAGE = "/static/img/item-default.svg"


class EmailConstants:
    """Constantes para emails"""

    # Timeouts
    SMTP_TIMEOUT = 30

    # Limites
    MAX_RECIPIENTS = 50
    MAX_ATTACHMENTS = 10
    MAX_ATTACHMENT_SIZE_MB = 25


class CacheConstants:
    """Constantes para cache"""

    # TTL padrão (segundos)
    DEFAULT_TTL = 300  # 5 minutos

    # TTL para diferentes tipos de dados
    USER_TTL = 600  # 10 minutos
    CATEGORY_TTL = 1800  # 30 minutos
    ITEM_TTL = 300  # 5 minutos


# Alias para manter compatibilidade com código existente
TAMANHO_PAGINA_PADRAO = PaginationConstants.DEFAULT_PAGE_SIZE
TAMANHO_MAXIMO_ARQUIVO_MB = ImageConstants.MAX_SIZE_MB
TIPOS_ARQUIVO_PERMITIDOS = ImageConstants.ALLOWED_TYPES
