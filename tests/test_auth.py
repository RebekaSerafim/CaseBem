"""
Testes para sistema de autenticação e autorização
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routes.admin_routes import router as admin_router
from routes.public_routes import router as public_router
from model.usuario_model import TipoUsuario, Usuario
from util.security import criar_hash_senha
from util.usuario_util import usuario_para_sessao, eh_admin, validar_permissao


@pytest.fixture
def app():
    """Fixture para criar app de teste"""
    test_app = FastAPI()
    test_app.add_middleware(
        SessionMiddleware,
        secret_key="test-secret-key",
        max_age=3600
    )
    test_app.include_router(public_router)
    test_app.include_router(admin_router)
    return test_app


@pytest.fixture
def client(app):
    """Fixture para cliente de teste"""
    return TestClient(app)


@pytest.fixture
def usuario_admin():
    """Fixture para usuário administrador"""
    return Usuario(
        id=1,
        nome="Admin Teste",
        cpf=None,
        data_nascimento=None,
        email="admin@teste.com",
        telefone="11999999999",
        senha=criar_hash_senha("senha123"),
        perfil=TipoUsuario.ADMIN,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )


@pytest.fixture
def usuario_noivo():
    """Fixture para usuário noivo"""
    return Usuario(
        id=2,
        nome="Noivo Teste",
        cpf=None,
        data_nascimento=None,
        email="noivo@teste.com",
        telefone="11999999999",
        senha=criar_hash_senha("senha123"),
        perfil=TipoUsuario.NOIVO,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )


class TestUsuarioUtil:
    """Testes para utilitários de usuário"""

    def test_usuario_para_sessao(self, usuario_admin):
        """Testa conversão de usuário para sessão"""
        sessao_dict = usuario_para_sessao(usuario_admin)

        assert sessao_dict["id"] == 1
        assert sessao_dict["nome"] == "Admin Teste"
        assert sessao_dict["email"] == "admin@teste.com"
        assert sessao_dict["perfil"] == "ADMIN"  # Enum convertido para string
        assert sessao_dict["foto"] is None

    def test_eh_admin(self, usuario_admin):
        """Testa verificação de administrador"""
        sessao_admin = usuario_para_sessao(usuario_admin)
        assert eh_admin(sessao_admin) is True

    def test_nao_eh_admin(self, usuario_noivo):
        """Testa verificação de não administrador"""
        sessao_noivo = usuario_para_sessao(usuario_noivo)
        assert eh_admin(sessao_noivo) is False

    def test_validar_permissao_sucesso(self):
        """Testa validação de permissão com sucesso"""
        assert validar_permissao("ADMIN", ["ADMIN", "NOIVO"]) is True

    def test_validar_permissao_falha(self):
        """Testa validação de permissão com falha"""
        assert validar_permissao("FORNECEDOR", ["ADMIN", "NOIVO"]) is False


class TestAuth:
    """Testes de autenticação e autorização"""

    def test_acesso_publico_permitido(self, client):
        """Testa que páginas públicas são acessíveis"""
        response = client.get("/")
        assert response.status_code == 200

    def test_acesso_admin_sem_login_negado(self, client):
        """Testa que páginas admin redirecionam para login quando não logado"""
        response = client.get("/admin/dashboard", follow_redirects=False)
        assert response.status_code == 303  # Redirect
        assert "/login" in response.headers["location"]

    def test_login_pagina_acessivel(self, client):
        """Testa que página de login é acessível"""
        response = client.get("/login")
        assert response.status_code == 200

    def test_cadastro_pagina_acessivel(self, client):
        """Testa que página de cadastro é acessível"""
        response = client.get("/cadastro")
        assert response.status_code == 200


class TestSecurity:
    """Testes de segurança"""

    def test_senha_hash_criado(self):
        """Testa que hash de senha é criado corretamente"""
        senha = "minha_senha_secreta"
        hash_senha = criar_hash_senha(senha)

        assert hash_senha != senha
        assert len(hash_senha) > 20  # Hash deve ser longo
        assert hash_senha.startswith("$2b$")  # bcrypt hash

    def test_senhas_diferentes_geram_hashes_diferentes(self):
        """Testa que senhas diferentes geram hashes diferentes"""
        senha1 = "senha123"
        senha2 = "senha456"

        hash1 = criar_hash_senha(senha1)
        hash2 = criar_hash_senha(senha2)

        assert hash1 != hash2

    def test_mesmo_senha_gera_hashes_diferentes(self):
        """Testa que a mesma senha gera hashes diferentes (salt)"""
        senha = "senha123"

        hash1 = criar_hash_senha(senha)
        hash2 = criar_hash_senha(senha)

        assert hash1 != hash2  # Due to salt


if __name__ == "__main__":
    pytest.main([__file__])