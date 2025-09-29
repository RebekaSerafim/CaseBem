"""
Biblioteca centralizada de validações para DTOs
Contém funções reutilizáveis para validação de dados em formulários
"""

import re
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any


class ValidacaoError(ValueError):
    """Exceção personalizada para erros de validação"""
    pass


def validar_cpf(cpf: Optional[str]) -> Optional[str]:
    """
    Valida CPF brasileiro com dígitos verificadores

    Args:
        cpf: CPF a ser validado (pode conter máscaras)

    Returns:
        CPF limpo (apenas números) ou None se vazio

    Raises:
        ValidacaoError: Se CPF for inválido
    """
    if not cpf:
        return None

    # Remover caracteres especiais
    cpf_limpo = re.sub(r'[^0-9]', '', cpf)

    if len(cpf_limpo) != 11:
        raise ValidacaoError('CPF deve ter 11 dígitos')

    # Verificar se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValidacaoError('CPF inválido')

    # Validar dígito verificador
    def calcular_digito(cpf_parcial):
        soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    if int(cpf_limpo[9]) != calcular_digito(cpf_limpo[:9]):
        raise ValidacaoError('CPF inválido')

    if int(cpf_limpo[10]) != calcular_digito(cpf_limpo[:10]):
        raise ValidacaoError('CPF inválido')

    return cpf_limpo


def validar_cnpj(cnpj: Optional[str]) -> Optional[str]:
    """
    Valida CNPJ brasileiro com dígitos verificadores

    Args:
        cnpj: CNPJ a ser validado (pode conter máscaras)

    Returns:
        CNPJ limpo (apenas números) ou None se vazio

    Raises:
        ValidacaoError: Se CNPJ for inválido
    """
    if not cnpj:
        return None

    # Remover caracteres especiais
    cnpj_limpo = re.sub(r'[^0-9]', '', cnpj)

    if len(cnpj_limpo) != 14:
        raise ValidacaoError('CNPJ deve ter 14 dígitos')

    # Verificar se todos os dígitos são iguais
    if cnpj_limpo == cnpj_limpo[0] * 14:
        raise ValidacaoError('CNPJ inválido')

    # Validar dígitos verificadores
    def calcular_digito_cnpj(cnpj_parcial, pesos):
        soma = sum(int(cnpj_parcial[i]) * pesos[i] for i in range(len(cnpj_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    if int(cnpj_limpo[12]) != calcular_digito_cnpj(cnpj_limpo[:12], pesos1):
        raise ValidacaoError('CNPJ inválido')

    if int(cnpj_limpo[13]) != calcular_digito_cnpj(cnpj_limpo[:13], pesos2):
        raise ValidacaoError('CNPJ inválido')

    return cnpj_limpo


def validar_telefone(telefone: str) -> str:
    """
    Valida telefone brasileiro (DDD + número)

    Args:
        telefone: Telefone a ser validado (pode conter máscaras)

    Returns:
        Telefone limpo (apenas números)

    Raises:
        ValidacaoError: Se telefone for inválido
    """
    if not telefone:
        raise ValidacaoError('Telefone é obrigatório')

    # Remover caracteres especiais
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)

    if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
        raise ValidacaoError('Telefone deve ter 10 ou 11 dígitos')

    # Validar DDD
    ddd = telefone_limpo[:2]
    if not (11 <= int(ddd) <= 99):
        raise ValidacaoError('DDD inválido')

    return telefone_limpo


def validar_data_nascimento(data_str: Optional[str], idade_minima: int = 16) -> Optional[str]:
    """
    Valida data de nascimento

    Args:
        data_str: Data no formato YYYY-MM-DD
        idade_minima: Idade mínima permitida (padrão: 16 anos)

    Returns:
        Data validada ou None se vazia

    Raises:
        ValidacaoError: Se data for inválida
    """
    if not data_str:
        return None

    # Validar formato ISO (YYYY-MM-DD)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data_str):
        raise ValidacaoError('Data deve estar no formato YYYY-MM-DD')

    try:
        data_nasc = datetime.strptime(data_str, '%Y-%m-%d').date()
        hoje = date.today()

        if data_nasc > hoje:
            raise ValidacaoError('Data de nascimento não pode ser futura')

        # Verificar idade mínima
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        if idade < idade_minima:
            raise ValidacaoError(f'Idade mínima é {idade_minima} anos')

        # Verificar se não é uma idade absurda (mais de 120 anos)
        if idade > 120:
            raise ValidacaoError('Data de nascimento inválida')

    except ValueError as e:
        if "does not match format" in str(e):
            raise ValidacaoError('Data inválida')
        raise ValidacaoError(str(e))

    return data_str


def validar_nome_pessoa(nome: str, min_chars: int = 2, max_chars: int = 100) -> str:
    """
    Valida nome de pessoa (apenas letras, espaços e acentos)

    Args:
        nome: Nome a ser validado
        min_chars: Número mínimo de caracteres
        max_chars: Número máximo de caracteres

    Returns:
        Nome limpo (espaços extras removidos)

    Raises:
        ValidacaoError: Se nome for inválido
    """
    if not nome or not nome.strip():
        raise ValidacaoError('Nome é obrigatório')

    # Remover espaços extras
    nome_limpo = ' '.join(nome.split())

    if len(nome_limpo) < min_chars:
        raise ValidacaoError(f'Nome deve ter pelo menos {min_chars} caracteres')

    if len(nome_limpo) > max_chars:
        raise ValidacaoError(f'Nome deve ter no máximo {max_chars} caracteres')

    # Verificar se contém apenas letras, espaços e acentos
    if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome_limpo):
        raise ValidacaoError('Nome deve conter apenas letras e espaços')

    return nome_limpo


def validar_texto_obrigatorio(texto: str, campo: str, min_chars: int = 1, max_chars: int = 1000) -> str:
    """
    Valida texto obrigatório com limites de caracteres

    Args:
        texto: Texto a ser validado
        campo: Nome do campo (para mensagens de erro)
        min_chars: Número mínimo de caracteres
        max_chars: Número máximo de caracteres

    Returns:
        Texto limpo (espaços extras removidos)

    Raises:
        ValidacaoError: Se texto for inválido
    """
    if not texto or not texto.strip():
        raise ValidacaoError(f'{campo} é obrigatório')

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split())

    if len(texto_limpo) < min_chars:
        raise ValidacaoError(f'{campo} deve ter pelo menos {min_chars} caracteres')

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'{campo} deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_texto_opcional(texto: Optional[str], max_chars: int = 1000) -> Optional[str]:
    """
    Valida texto opcional com limite de caracteres

    Args:
        texto: Texto a ser validado
        max_chars: Número máximo de caracteres

    Returns:
        Texto limpo ou None se vazio

    Raises:
        ValidacaoError: Se texto exceder limite
    """
    if not texto:
        return None

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split()) if texto.strip() else None

    if texto_limpo and len(texto_limpo) > max_chars:
        raise ValidacaoError(f'Texto deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_valor_monetario(valor: Any, campo: str = "Valor", obrigatorio: bool = True,
                          min_valor: Decimal = Decimal('0')) -> Optional[Decimal]:
    """
    Valida valor monetário

    Args:
        valor: Valor a ser validado
        campo: Nome do campo (para mensagens de erro)
        obrigatorio: Se o valor é obrigatório
        min_valor: Valor mínimo permitido

    Returns:
        Valor decimal validado ou None se opcional e vazio

    Raises:
        ValidacaoError: Se valor for inválido
    """
    if valor is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    try:
        valor_decimal = Decimal(str(valor))
    except:
        raise ValidacaoError(f'{campo} deve ser um número válido')

    if valor_decimal < min_valor:
        if min_valor == 0:
            raise ValidacaoError(f'{campo} não pode ser negativo')
        else:
            raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    # Verificar se tem no máximo 2 casas decimais
    if valor_decimal != round(valor_decimal, 2):
        raise ValidacaoError(f'{campo} deve ter no máximo 2 casas decimais')

    # Verificar se não é um valor absurdamente alto
    if valor_decimal > Decimal('9999999.99'):
        raise ValidacaoError(f'{campo} não pode ser superior a R$ 9.999.999,99')

    return valor_decimal


def validar_numero_inteiro(numero: Any, campo: str = "Número", obrigatorio: bool = True,
                          min_valor: int = 0, max_valor: int = 9999) -> Optional[int]:
    """
    Valida número inteiro

    Args:
        numero: Número a ser validado
        campo: Nome do campo (para mensagens de erro)
        obrigatorio: Se o número é obrigatório
        min_valor: Valor mínimo permitido
        max_valor: Valor máximo permitido

    Returns:
        Número inteiro validado ou None se opcional e vazio

    Raises:
        ValidacaoError: Se número for inválido
    """
    if numero is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    try:
        numero_int = int(numero)
    except:
        raise ValidacaoError(f'{campo} deve ser um número inteiro válido')

    if numero_int < min_valor:
        raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    if numero_int > max_valor:
        raise ValidacaoError(f'{campo} deve ser menor ou igual a {max_valor}')

    return numero_int


def validar_estado_brasileiro(estado: Optional[str]) -> Optional[str]:
    """
    Valida sigla de estado brasileiro

    Args:
        estado: Sigla do estado (2 caracteres)

    Returns:
        Estado em maiúsculo ou None se vazio

    Raises:
        ValidacaoError: Se estado for inválido
    """
    if not estado:
        return None

    estado_upper = estado.strip().upper()

    if len(estado_upper) != 2:
        raise ValidacaoError('Estado deve ter exatamente 2 caracteres (sigla UF)')

    # Lista de estados brasileiros válidos
    estados_validos = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]

    if estado_upper not in estados_validos:
        raise ValidacaoError('Sigla de estado inválida')

    return estado_upper


def validar_senha(senha: Optional[str], min_chars: int = 6, max_chars: int = 128,
                  obrigatorio: bool = True) -> Optional[str]:
    """
    Valida senha

    Args:
        senha: Senha a ser validada
        min_chars: Número mínimo de caracteres
        max_chars: Número máximo de caracteres
        obrigatorio: Se a senha é obrigatória

    Returns:
        Senha validada ou None se opcional e vazia

    Raises:
        ValidacaoError: Se senha for inválida
    """
    if not senha:
        if obrigatorio:
            raise ValidacaoError('Senha é obrigatória')
        return None

    if len(senha) < min_chars:
        raise ValidacaoError(f'Senha deve ter pelo menos {min_chars} caracteres')

    if len(senha) > max_chars:
        raise ValidacaoError(f'Senha deve ter no máximo {max_chars} caracteres')

    return senha


def validar_senhas_coincidem(senha: str, confirmar_senha: str) -> str:
    """
    Valida se duas senhas coincidem

    Args:
        senha: Senha principal
        confirmar_senha: Confirmação da senha

    Returns:
        Senha confirmada

    Raises:
        ValidacaoError: Se senhas não coincidirem
    """
    if senha != confirmar_senha:
        raise ValidacaoError('As senhas não coincidem')

    return confirmar_senha


def converter_checkbox_para_bool(valor: Any) -> bool:
    """
    Converte valor de checkbox HTML para boolean

    Args:
        valor: Valor do checkbox (pode ser 'on', True, False, etc.)

    Returns:
        Boolean correspondente
    """
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str):
        return valor.lower() in ['on', 'true', '1', 'yes']
    return bool(valor)


def validar_enum_valor(valor: Any, enum_class, campo: str = "Campo") -> Any:
    """
    Valida se valor está em um enum

    Args:
        valor: Valor a ser validado
        enum_class: Classe do enum
        campo: Nome do campo (para mensagens de erro)

    Returns:
        Valor do enum validado

    Raises:
        ValidacaoError: Se valor não estiver no enum
    """
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    if valor not in enum_class:
        valores_validos = [item.value for item in enum_class]
        raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    return valor


# =====================================================
# WRAPPER PARA SIMPLIFICAR USO EM FIELD_VALIDATORS
# =====================================================

class ValidadorWrapper:
    """
    Classe para facilitar o uso de validadores em field_validators.
    Reduz código repetitivo e padroniza tratamento de erros.
    """

    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria um validador pronto para usar com @field_validator.

        Args:
            funcao_validacao: Função de validação a ser chamada
            campo_nome: Nome do campo para mensagens de erro
            **kwargs: Argumentos adicionais para a função

        Returns:
            Função validador pronta para usar

        Exemplo:
            validar_nome = ValidadorWrapper.criar_validador(
                validar_nome_pessoa, "Nome", min_chars=2, max_chars=100
            )
        """
        def validador(valor):
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador

    @staticmethod
    def criar_validador_opcional(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria validador para campos opcionais.
        Retorna None se o valor for vazio, senão valida normalmente.

        Args:
            funcao_validacao: Função de validação a ser chamada
            campo_nome: Nome do campo para mensagens de erro
            **kwargs: Argumentos adicionais para a função

        Returns:
            Função validador para campos opcionais
        """
        def validador(valor):
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                return None
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador


# =====================================================
# VALIDADORES PRÉ-CONFIGURADOS COMUNS
# =====================================================

# Validadores mais usados, pré-configurados para facilitar uso
VALIDADOR_NOME = ValidadorWrapper.criar_validador(validar_nome_pessoa, "Nome")
VALIDADOR_CPF = ValidadorWrapper.criar_validador_opcional(validar_cpf, "CPF")
VALIDADOR_TELEFONE = ValidadorWrapper.criar_validador(validar_telefone, "Telefone")
VALIDADOR_SENHA = ValidadorWrapper.criar_validador(validar_senha, "Senha")
VALIDADOR_EMAIL = ValidadorWrapper.criar_validador_opcional(lambda v, c: v, "Email")  # Pydantic já valida
VALIDADOR_DATA_NASCIMENTO = ValidadorWrapper.criar_validador_opcional(validar_data_nascimento, "Data de nascimento", idade_minima=16)