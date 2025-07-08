from datetime import datetime
import pytest
import os
import sys
import tempfile

from model.usuario_model import Usuario

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
    usuario = Usuario(0, "Usuário Teste", "(28) 99999-0000", "usuario@email.com", "123456", "ADMIN", "123.456.789-00")
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
def noivo_exemplo():
    # Cria um noivo de exemplo para os testes
    from model.usuario_model import Usuario
    noivo = Usuario(0, "Noivo Teste", "(28) 99999-0000", "noivo@email.com", "123456", "NOIVO", "123.456.789-00")
    return noivo

@pytest.fixture
def lista_noivos_exemplo():
    # Cria uma lista de 10 noivos de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Noivo {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "NOIVO", f"123.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def prestador_exemplo():
    # Cria um prestador de exemplo para os testes
    from model.usuario_model import Usuario
    prestador = Usuario(0, "Prestador Teste", "(28) 99999-0000", "prestador@email.com", "123456", "PRESTADOR", "223.456.789-00")
    return prestador

@pytest.fixture
def lista_prestadores_exemplo():
    # Cria uma lista de 10 prestadores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Prestador {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "PRESTADOR", f"223.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def fornecedor_exemplo():
    # Cria um fornecedor de exemplo para os testes
    from model.usuario_model import Usuario
    fornecedor = Usuario(0, "Fornecedor Teste", "(28) 99999-0000", "fornecedor@email.com", "123456", "FORNECEDOR", "323.456.789-00")
    return fornecedor

@pytest.fixture
def lista_fornecedores_exemplo():
    # Cria uma lista de 10 fornecedores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Fornecedor {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "FORNECEDOR", f"323.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def administrador_exemplo():
    # Cria um administrador de exemplo para os testes
    from model.usuario_model import Usuario
    administrador = Usuario(0, "Administrador Teste", "(28) 99999-0000", "admin@email.com", "123456", "ADMIN", "423.456.789-00")
    return administrador

@pytest.fixture
def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo para os testes
    from model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Administrador {i:02d}", f"(28) 99999-00{i:02d}", f"usuario{i:02d}@email.com", "123456", "ADMIN", f"423.456.789-{i:02d}")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def casal_exemplo():
    # Cria um casal de exemplo para os testes    
    from model.casal_model import Casal
    casal = Casal(0, 1, 2, 10000.0)
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
def demanda_exemplo():
    # Cria um demanda de exemplo para os testes
    from model.demanda_model import Demanda
    demanda = Demanda(0, "Contrato Teste", datetime.now(), 1000.0, "Descrição do demanda teste")
    return demanda

@pytest.fixture
def lista_demandas_exemplo():
    # Cria uma lista de 10 demandas de exemplo para os testes
    from model.demanda_model import Demanda
    demandas = []
    for i in range(1, 11):
        demanda = Demanda(0, f"Contrato {i:02d}", datetime.now(), 1000.0 + (i * 100), f"Descrição do demanda {i:02d}")
        demandas.append(demanda)
    return demandas
