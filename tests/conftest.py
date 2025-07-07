from datetime import datetime
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def usuario_exemplo():
    # Cria um usuário de exemplo para os testes
    from model.usuario_model import Usuario
    usuario = Usuario(0, "Usuário Teste", "(28) 99999-0000", "usuario@email.com", "123456", "ADMIN")
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    tipos = ["ADMIN", "NOIVO", "PRESTADOR", "FORNECEDOR"]
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", tipos[i % 4])
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def lista_noivos_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "NOIVO")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def casal_exemplo():
    # Cria um casal de exemplo para os testes    
    from model.casal_model import Casal
    casal = Casal(1, 2, 10000.0)
    return casal

@pytest.fixture
def lista_casais_exemplo():
    # Cria uma lista de 10 casais de exemplo para os testes    
    from model.casal_model import Casal
    casais = []
    for i in range(1, 11, 2):
        casal = Casal(i, i + 1, 10000.0 + (i * 100))
        casais.append(casal)
    return casais

@pytest.fixture
def prestador_exemplo():
    # Cria um prestador de serviços de exemplo para os testes
    from model.prestador_model import Prestador
    prestador = Prestador(0, "Prestador Teste", "(28) 99999-0000", "prestador@email.com", "123456", "PRESTADOR", "FISICA", "123.456.789-00")
    return prestador

@pytest.fixture
def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo para os testes
    from model.administrador_model import Administrador
    administradores = []
    for i in range(1, 11):
        administrador = Administrador(0, "Administrador Teste", "(28) 99999-9999", "administrador@email.com", "654321", "ADMIN")
        administradores.append(administrador)
    return administradores

@pytest.fixture
def servicos_exemplo():
    # Cria um serviço de exemplo para os testes
    from model.servico_model import Servico
    servico = Servico(0, "Serviço Teste", "Descrição do serviço", 100.0)
    return servico

@pytest.fixture
def lista_servicos_exemplo():
    # Cria uma lista de 10 serviços de exemplo para os testes
    from model.servico_model import Servico
    servicos = []
    for i in range(1, 11):
        servico = Servico(0, f"Serviço {i:02d}", f"Descrição do serviço {i:02d}", 100.0 * i)
        servicos.append(servico)
    return servicos

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from model.produto_model import Produto
    produto = Produto(0, "Produto Teste", 19.99, 10, "Descrição do produto teste")
    return produto

@pytest.fixture
def lista_produtos_exemplo():  
    # Cria uma lista de 10 produtos de exemplo para os testes
    from model.produto_model import Produto
    produtos = []
    for i in range(1, 11):
        produto = Produto(0, f"Produto {i:02d}", 19.99 + i, 10 + i, f"Descrição do produto {i:02d}")
        produtos.append(produto)
    return produtos    

@pytest.fixture
def contrato_exemplo():
    # Cria um contrato de exemplo para os testes
    from model.contrato_model import Contrato
    contrato = Contrato(0, "Contrato Teste", datetime.now(), 1000.0, "Descrição do contrato teste")
    return contrato

@pytest.fixture
def lista_contratos_exemplo():
    # Cria uma lista de 10 contratos de exemplo para os testes
    from model.contrato_model import Contrato
    contratos = []
    for i in range(1, 11):
        contrato = Contrato(0, f"Contrato {i:02d}", datetime.now(), 1000.0 + (i * 100), f"Descrição do contrato {i:02d}")
        contratos.append(contrato)
    return contratos
