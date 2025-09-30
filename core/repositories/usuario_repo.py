from typing import Optional, List
from core.repositories.base_repo import BaseRepo
from core.sql import usuario_sql
from core.models.usuario_model import TipoUsuario, Usuario


class UsuarioRepo(BaseRepo):
    """Repositório para operações com usuários"""

    def __init__(self):
        super().__init__("usuario", Usuario, usuario_sql)

    def criar_tabela(self) -> bool:
        """
        Cria a tabela de usuários no banco de dados.

        Inclui lógica específica para adicionar a coluna 'ativo' em versões
        antigas do banco que não possuem esta coluna.

        Returns:
            bool: True se tabela criada/atualizada com sucesso, False caso contrário
        """
        try:
            result = super().criar_tabela()
            if result:
                try:
                    self.executar_comando(usuario_sql.ADICIONAR_COLUNA_ATIVO)
                except Exception:
                    pass  # Coluna já existe
            return result
        except Exception as e:
            from infrastructure.logging.logger import CaseBemLogger

            logger = CaseBemLogger()
            logger.error("Erro ao criar tabela de usuários", extra={"erro": str(e)})
            return False

    def _objeto_para_tupla_insert(self, usuario: Usuario) -> tuple:
        """Prepara dados do usuário para inserção"""
        return (
            usuario.nome,
            usuario.cpf,
            usuario.data_nascimento,
            usuario.email,
            usuario.telefone,
            usuario.senha,
            usuario.perfil.value,
        )

    def _objeto_para_tupla_update(self, usuario: Usuario) -> tuple:
        """Prepara dados do usuário para atualização"""
        return (
            usuario.nome,
            usuario.cpf,
            usuario.data_nascimento,
            usuario.telefone,
            usuario.email,
            usuario.id,
        )

    def _linha_para_objeto(self, linha: dict) -> Usuario:
        """Converte linha do banco de dados em objeto Usuario"""
        return Usuario(
            id=linha["id"],
            nome=linha["nome"],
            cpf=linha["cpf"],
            data_nascimento=linha["data_nascimento"],
            email=linha["email"],
            telefone=linha["telefone"],
            senha=linha["senha"],
            perfil=TipoUsuario(linha["perfil"]),
            token_redefinicao=self._safe_get(linha, "token_redefinicao"),
            data_token=self._safe_get(linha, "data_token"),
            data_cadastro=self._safe_get(linha, "data_cadastro"),
            ativo=bool(self._safe_get(linha, "ativo", True)),
        )

    def atualizar_senha_usuario(self, id: int, senha_hash: str) -> bool:
        """Atualiza apenas a senha de um usuário"""
        return self.executar_comando(
            usuario_sql.ATUALIZAR_SENHA_USUARIO, (senha_hash, id)
        )

    def obter_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário pelo email"""
        resultados = self.executar_consulta(
            usuario_sql.OBTER_USUARIO_POR_EMAIL, (email,)
        )
        return self._linha_para_objeto(resultados[0]) if resultados else None

    def obter_usuarios_por_pagina(
        self, numero_pagina: int, tamanho_pagina: int
    ) -> List[Usuario]:
        """Lista usuários com paginação"""
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_consulta(
            usuario_sql.OBTER_USUARIOS_POR_PAGINA, (tamanho_pagina, offset)
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def obter_usuarios_por_tipo_por_pagina(
        self, tipo: TipoUsuario, numero_pagina: int, tamanho_pagina: int
    ) -> List[Usuario]:
        """Lista usuários de um tipo específico com paginação"""
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_consulta(
            usuario_sql.OBTER_USUARIOS_POR_TIPO_POR_PAGINA,
            (tipo.value, tamanho_pagina, offset),
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def contar_usuarios(self) -> int:
        """Conta o total de usuários no sistema"""
        return self.contar_registros()

    def contar_usuarios_por_tipo(self, tipo: TipoUsuario) -> int:
        """Conta o total de usuários de um tipo específico"""
        return self.contar_registros("perfil = ?", (tipo.value,))

    def buscar_usuarios(
        self,
        busca: str = "",
        tipo_usuario: str = "",
        status: str = "",
        numero_pagina: int = 1,
        tamanho_pagina: int = 100,
    ) -> List[Usuario]:
        """Busca usuários com filtros de nome/email, tipo e status"""
        offset = (numero_pagina - 1) * tamanho_pagina
        resultados = self.executar_consulta(
            usuario_sql.BUSCAR_USUARIOS,
            (
                busca,
                busca,
                busca,
                tipo_usuario,
                tipo_usuario,
                status,
                status,
                status,
                tamanho_pagina,
                offset,
            ),
        )
        return [self._linha_para_objeto(row) for row in resultados]

    def bloquear_usuario(self, id_usuario: int) -> bool:
        """Bloqueia (desativa) um usuário"""
        return self.desativar(id_usuario)

    def ativar_usuario(self, id_usuario: int) -> bool:
        """Ativa um usuário"""
        return self.ativar(id_usuario)

    def obter_usuarios_paginado(
        self, pagina: int, tamanho_pagina: int
    ) -> tuple[List[Usuario], int]:
        """Obtém usuários paginados e retorna lista de usuários e total"""
        return self.obter_paginado(pagina, tamanho_pagina)

    def buscar_usuarios_paginado(
        self,
        busca: str = "",
        tipo_usuario: str = "",
        status: str = "",
        pagina: int = 1,
        tamanho_pagina: int = 10,
    ) -> tuple[List[Usuario], int]:
        """Busca usuários paginados com filtros e retorna lista de usuários e total"""
        offset = (pagina - 1) * tamanho_pagina

        # Parâmetros seguem a ordem da query: busca, busca, busca, tipo, tipo, status, status, status
        parametros_count = [
            busca,
            busca,
            busca,
            tipo_usuario,
            tipo_usuario,
            status,
            status,
            status,
        ]
        parametros_select = parametros_count + [tamanho_pagina, offset]

        # Contar total usando query parametrizada
        total_resultado = self.executar_consulta(
            usuario_sql.CONTAR_USUARIOS_FILTRADOS, parametros_count
        )
        total = total_resultado[0]["total"] if total_resultado else 0

        # Buscar usuários usando query parametrizada
        resultados = self.executar_consulta(
            usuario_sql.BUSCAR_USUARIOS, parametros_select
        )
        usuarios = [self._linha_para_objeto(row) for row in resultados]

        return usuarios, total


# Instância singleton do repositório
usuario_repo = UsuarioRepo()
