"""
Arquivo de teste para verificar imports.
Se este arquivo não mostrar erros no VS Code, os imports estão funcionando.
"""

# Teste 1: Import absoluto de exceptions
from util.exceptions import CaseBemError, TipoErro, ValidacaoError

# Teste 2: Import absoluto de logger
from infrastructure.logging import logger, CaseBemLogger

# Teste 3: Import absoluto de error_handlers
from util.error_handlers import tratar_erro_banco_dados, validar_parametros

# Teste 4: Import do base_repo (agora está em core.repositories)
from core.repositories.base_repo import BaseRepo, BaseRepoChaveComposta

# Teste 5: Usar as classes para verificar que funcionam
def teste_basico():
    """Teste básico de funcionalidade"""
    # Criar exceção
    erro = ValidacaoError("Teste", campo="teste")
    print(f"Erro criado: {erro}")

    # Usar logger
    logger.info("Teste de log")
    print("Logger funcionando")

    # Verificar TipoErro
    print(f"Tipo de erro: {TipoErro.VALIDACAO}")

    print("✓ Todos os imports funcionam corretamente!")

if __name__ == "__main__":
    teste_basico()