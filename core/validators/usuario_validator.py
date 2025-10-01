"""
Validador de dados de usuário.

Centraliza validações que estavam duplicadas em múltiplas rotas.
"""

from typing import Tuple, Optional
import re


class UsuarioValidator:
    """Validador centralizado para dados de usuário"""

    # Regex simples para validação de email
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    # Tamanho mínimo de senha
    TAMANHO_MINIMO_SENHA = 6

    # Tamanho máximo de nome
    TAMANHO_MAXIMO_NOME = 100

    @staticmethod
    def validar_nome(nome: str) -> Tuple[bool, Optional[str]]:
        """
        Valida nome de usuário.

        Args:
            nome: Nome a validar

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        nome = nome.strip() if nome else ""

        if not nome:
            return False, "Nome é obrigatório"

        if len(nome) > UsuarioValidator.TAMANHO_MAXIMO_NOME:
            return False, f"Nome não pode ter mais de {UsuarioValidator.TAMANHO_MAXIMO_NOME} caracteres"

        return True, None

    @staticmethod
    def validar_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Valida formato de email.

        Args:
            email: Email a validar

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        email = email.strip() if email else ""

        if not email:
            return False, "Email é obrigatório"

        if not UsuarioValidator.EMAIL_REGEX.match(email):
            return False, "Email inválido"

        return True, None

    @staticmethod
    def validar_senha(senha: str, confirmar: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Valida força da senha.

        Args:
            senha: Senha a validar
            confirmar: Se True, senha é obrigatória (para criação).
                      Se False, senha pode ser vazia (para atualização)

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        # Se não é obrigatória e está vazia, é válido (para updates)
        if not confirmar and not senha:
            return True, None

        # Se é obrigatória, deve existir
        if confirmar and not senha:
            return False, "Senha é obrigatória"

        # Se tem senha, validar tamanho
        if senha and len(senha) < UsuarioValidator.TAMANHO_MINIMO_SENHA:
            return False, f"Senha deve ter pelo menos {UsuarioValidator.TAMANHO_MINIMO_SENHA} caracteres"

        return True, None

    @staticmethod
    def validar_cpf(cpf: str) -> Tuple[bool, Optional[str]]:
        """
        Valida formato de CPF (validação básica de formato).

        Args:
            cpf: CPF a validar

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        if not cpf:
            return True, None  # CPF é opcional

        # Remove caracteres não numéricos
        cpf_numeros = re.sub(r'[^0-9]', '', cpf)

        # Valida tamanho
        if len(cpf_numeros) != 11:
            return False, "CPF deve ter 11 dígitos"

        # Valida se não são todos números iguais
        if cpf_numeros == cpf_numeros[0] * 11:
            return False, "CPF inválido"

        return True, None

    @staticmethod
    def validar_telefone(telefone: str) -> Tuple[bool, Optional[str]]:
        """
        Valida formato de telefone.

        Args:
            telefone: Telefone a validar

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        if not telefone:
            return True, None  # Telefone é opcional

        # Remove caracteres não numéricos
        telefone_numeros = re.sub(r'[^0-9]', '', telefone)

        # Valida tamanho (10 ou 11 dígitos)
        if len(telefone_numeros) not in [10, 11]:
            return False, "Telefone deve ter 10 ou 11 dígitos"

        return True, None

    @staticmethod
    def validar_dados_cadastro(
        nome: str,
        email: str,
        senha: str,
        cpf: Optional[str] = None,
        telefone: Optional[str] = None,
        id_excluir: Optional[int] = None  # Para atualização
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida dados completos de cadastro/atualização de usuário.

        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha: Senha do usuário
            cpf: CPF (opcional)
            telefone: Telefone (opcional)
            id_excluir: ID do usuário atual (para permitir manter mesmo email em updates)

        Returns:
            Tuple[bool, Optional[str]]: (valido, mensagem_erro)
        """
        # Validar nome
        valido, erro = UsuarioValidator.validar_nome(nome)
        if not valido:
            return False, erro

        # Validar email
        valido, erro = UsuarioValidator.validar_email(email)
        if not valido:
            return False, erro

        # Validar senha (obrigatória se for criação, id_excluir None)
        confirmar_senha = id_excluir is None
        valido, erro = UsuarioValidator.validar_senha(senha, confirmar=confirmar_senha)
        if not valido:
            return False, erro

        # Validar CPF se fornecido
        if cpf:
            valido, erro = UsuarioValidator.validar_cpf(cpf)
            if not valido:
                return False, erro

        # Validar telefone se fornecido
        if telefone:
            valido, erro = UsuarioValidator.validar_telefone(telefone)
            if not valido:
                return False, erro

        return True, None

    @staticmethod
    def validar_email_unico(email: str, id_excluir: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Verifica se email já está em uso por outro usuário.

        Args:
            email: Email a verificar
            id_excluir: ID do usuário atual (para permitir manter mesmo email em updates)

        Returns:
            Tuple[bool, Optional[str]]: (unico, mensagem_erro)
        """
        from core.repositories import usuario_repo

        usuario_existente = usuario_repo.obter_usuario_por_email(email)

        if usuario_existente:
            # Se está atualizando e o email é do próprio usuário, OK
            if id_excluir and usuario_existente.id == id_excluir:
                return True, None

            # Email já está em uso por outro usuário
            return False, f"Já existe um usuário cadastrado com o email {email}"

        return True, None
