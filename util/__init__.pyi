"""Type stubs for util package"""

# Este arquivo ajuda o Pylance/Pyright a entender a estrutura do pacote
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import exceptions as exceptions
    from . import logger as logger
    from . import error_handlers as error_handlers
    from . import base_repo as base_repo
    from . import validacoes_dto as validacoes_dto
    from . import security as security
    from . import database as database

__all__ = [
    'exceptions',
    'logger',
    'error_handlers',
    'base_repo',
    'validacoes_dto',
    'security',
    'database',
]