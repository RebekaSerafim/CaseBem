"""
Serviço de usuários - Lógica de negócio centralizada

Este serviço concentra todas as regras de negócio relacionadas aos usuários,
incluindo criação, autenticação, validações e operações complexas.
"""

from typing import Optional, List
from util.exceptions import RegraDeNegocioError, RecursoNaoEncontradoError, ValidacaoError
from core.models.usuario_model import Usuario, TipoUsuario
from util.logger import logger


class UsuarioService:
    """
    Serviço para operações de negócio com usuários

    Centraliza toda a lógica de negócio relacionada aos usuários,
    aplicando validações, regras de domínio e orquestrando
    operações entre diferentes repositórios quando necessário.
    """

    def __init__(self):
        from core.repositories import usuario_repo
        from util.security import hash_password, verify_password

        self.repo = usuario_repo
        self.hash_password = hash_password
        self.verify_password = verify_password

    def criar_usuario(self, dados: dict) -> int:
        """
        Cria um novo usuário aplicando regras de negócio

        Args:
            dados: Dados validados do usuário (dict temporário, será DTO depois)

        Returns:
            ID do usuário criado

        Raises:
            RegraDeNegocioError: Se regra de negócio for violada
            ValidacaoError: Se dados inválidos
        """
        # Verificar se email já existe
        if self._email_ja_existe(dados['email']):
            raise RegraDeNegocioError(
                "Este email já está cadastrado no sistema",
                regra="EMAIL_UNICO"
            )

        # Aplicar hash na senha
        senha_hash = self.hash_password(dados['senha'])

        # Criar objeto do modelo
        usuario = Usuario(
            id=0,
            nome=dados['nome'],
            cpf=dados.get('cpf'),
            data_nascimento=dados.get('data_nascimento'),
            email=dados['email'],
            telefone=dados['telefone'],
            senha=senha_hash,
            perfil=dados.get('perfil', TipoUsuario.NOIVO),
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            ativo=True
        )

        # Inserir no banco
        id_usuario = self.repo.inserir(usuario)

        logger.log_info("Usuário criado com sucesso", extra={
            'id_usuario': id_usuario,
            'email': dados['email'],
            'perfil': dados.get('perfil', TipoUsuario.NOIVO).value if isinstance(dados.get('perfil'), TipoUsuario) else str(dados.get('perfil'))
        })

        return id_usuario

    def autenticar_usuario(self, email: str, senha: str) -> Optional[Usuario]:
        """
        Autentica usuário por email e senha

        Args:
            email: Email do usuário
            senha: Senha em texto plano

        Returns:
            Usuário se autenticado, None caso contrário

        Raises:
            RegraDeNegocioError: Se usuário inativo
        """
        try:
            usuario = self.repo.obter_usuario_por_email(email)

            if usuario and self.verify_password(senha, usuario.senha):
                if not usuario.ativo:
                    raise RegraDeNegocioError(
                        "Usuário está inativo. Contate o administrador.",
                        regra="USUARIO_ATIVO"
                    )

                logger.log_info("Usuário autenticado com sucesso", extra={
                    'usuario_id': usuario.id,
                    'email': email
                })
                return usuario

        except RecursoNaoEncontradoError:
            pass  # Email não encontrado

        logger.log_warning("Tentativa de autenticação falhada", extra={'email': email})
        return None

    def obter_usuario_por_id(self, user_id: int) -> Usuario:
        """
        Obtém usuário por ID aplicando validações de negócio

        Args:
            user_id: ID do usuário

        Returns:
            Usuario encontrado

        Raises:
            ValidacaoError: Se ID inválido
            RecursoNaoEncontradoError: Se usuário não encontrado
        """
        if user_id <= 0:
            raise ValidacaoError("ID do usuário deve ser um número positivo", "user_id", user_id)

        return self.repo.obter_por_id(user_id)

    def listar_usuarios_ativos(self, pagina: int = 1, por_pagina: int = 10) -> List[Usuario]:
        """
        Lista usuários ativos com paginação

        Args:
            pagina: Número da página (começa em 1)
            por_pagina: Usuários por página

        Returns:
            Lista de usuários ativos

        Raises:
            ValidacaoError: Se parâmetros de paginação inválidos
        """
        if pagina <= 0:
            raise ValidacaoError("Página deve ser um número positivo", "pagina", pagina)

        if por_pagina <= 0 or por_pagina > 100:
            raise ValidacaoError("Por página deve estar entre 1 e 100", "por_pagina", por_pagina)

        usuarios = self.repo.obter_usuarios_por_pagina(pagina, por_pagina)

        # Filtrar apenas usuários ativos (regra de negócio)
        return [u for u in usuarios if u.ativo]

    def desativar_usuario(self, user_id: int, admin_id: int) -> bool:
        """
        Desativa usuário (soft delete) aplicando regras de autorização

        Args:
            user_id: ID do usuário a ser desativado
            admin_id: ID do admin que está desativando

        Returns:
            True se desativado com sucesso

        Raises:
            RegraDeNegocioError: Se violação de regra de negócio
            RecursoNaoEncontradoError: Se usuário não encontrado
        """
        # Verificar se admin tem permissão
        admin = self.repo.obter_por_id(admin_id)
        if admin.perfil != TipoUsuario.ADMIN:
            raise RegraDeNegocioError(
                "Apenas administradores podem desativar usuários",
                regra="APENAS_ADMIN_DESATIVA"
            )

        # Não pode desativar a si mesmo
        if user_id == admin_id:
            raise RegraDeNegocioError(
                "Administrador não pode desativar a si mesmo",
                regra="ADMIN_NAO_AUTODESATIVA"
            )

        # Obter usuário e desativar
        usuario = self.repo.obter_por_id(user_id)
        usuario.ativo = False

        resultado = self.repo.atualizar(usuario)

        if resultado:
            logger.log_info("Usuário desativado", extra={
                'usuario_id': user_id,
                'admin_id': admin_id
            })

        return resultado

    def _email_ja_existe(self, email: str) -> bool:
        """
        Verifica se email já está em uso

        Args:
            email: Email a verificar

        Returns:
            True se email já existe, False caso contrário
        """
        try:
            self.repo.obter_usuario_por_email(email)
            return True
        except RecursoNaoEncontradoError:
            return False

    def atualizar_perfil_usuario(self, user_id: int, dados: dict) -> bool:
        """
        Atualiza dados do perfil do usuário

        Args:
            user_id: ID do usuário
            dados: Dados a serem atualizados

        Returns:
            True se atualizado com sucesso

        Raises:
            RecursoNaoEncontradoError: Se usuário não encontrado
            ValidacaoError: Se dados inválidos
        """
        usuario = self.repo.obter_por_id(user_id)

        # Aplicar apenas campos permitidos para atualização de perfil
        campos_permitidos = ['nome', 'telefone', 'data_nascimento']

        for campo, valor in dados.items():
            if campo in campos_permitidos and valor is not None:
                setattr(usuario, campo, valor)

        resultado = self.repo.atualizar(usuario)

        if resultado:
            logger.log_info("Perfil de usuário atualizado", extra={
                'usuario_id': user_id,
                'campos_atualizados': list(dados.keys())
            })

        return resultado


# Instância global do serviço
usuario_service = UsuarioService()