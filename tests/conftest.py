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
    from model.usuario_model import Usuario, TipoUsuario
    usuario = Usuario(0, "Usuário Teste", "123.456.789-00", "1990-01-01", "usuario@email.com", "(28) 99999-0000", "123456", TipoUsuario.ADMIN, None, None, None, None)
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo para os testes
    from model.usuario_model import Usuario, TipoUsuario
    tipos = [TipoUsuario.ADMIN, TipoUsuario.NOIVO, TipoUsuario.FORNECEDOR]
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Usuário {i:02d}", f"123.456.78{i:01d}-00", f"199{i:01d}-01-01", f"usuario{i:02d}@email.com", f"(28) 99999-00{i:02d}", "123456", tipos[i % 3], None, None, None, None)
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def noivo_exemplo():
    # Cria um noivo de exemplo para os testes
    from model.usuario_model import Usuario, TipoUsuario
    noivo = Usuario(0, "Noivo Teste", "987.654.321-00", "1995-05-15", "noivo@email.com", "(28) 99999-0000", "123456", TipoUsuario.NOIVO, None, None, None, None)
    return noivo

@pytest.fixture
def lista_noivos_exemplo():
    # Cria uma lista de 10 noivos de exemplo para os testes
    from model.usuario_model import Usuario, TipoUsuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Noivo {i:02d}", f"987.654.32{i:01d}-00", f"199{i:01d}-05-15", f"noivo{i:02d}@email.com", f"(28) 99999-00{i:02d}", "123456", TipoUsuario.NOIVO, None, None, None, None)
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def fornecedor_exemplo():
    # Cria um fornecedor de exemplo para os testes
    from model.fornecedor_model import Fornecedor
    from model.usuario_model import TipoUsuario
    fornecedor = Fornecedor(
        # Campos de Usuario na ordem correta
        id=0,
        nome="Fornecedor Teste",
        cpf="111.222.333-44",
        data_nascimento="1985-03-20",
        email="fornecedor@email.com",
        telefone="(28) 99999-5000",
        senha="123456",
        perfil=TipoUsuario.FORNECEDOR,

        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Fornecedor
        nome_empresa="Empresa Teste",
        cnpj="12.345.678/0001-90",
        descricao="Descrição dos serviços"
    )
    return fornecedor

@pytest.fixture
def lista_fornecedores_exemplo():
    # Cria uma lista de 10 fornecedores de exemplo para os testes
    from model.fornecedor_model import Fornecedor
    from model.usuario_model import TipoUsuario
    fornecedores = []
    for i in range(1, 11):
        fornecedor = Fornecedor(
            # Campos de Usuario na ordem correta
            id=0,
            nome=f"Fornecedor {i:02d}",
            cpf=f"111.222.33{i:01d}-44",
            data_nascimento=f"198{i:01d}-03-20",
            email=f"fornecedor{i:02d}@email.com",
            telefone=f"(28) 99999-50{i:02d}",
            senha="123456",
            perfil=TipoUsuario.FORNECEDOR,
    
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            # Campos específicos de Fornecedor
            nome_empresa=f"Empresa {i:02d}",
            cnpj=f"12.345.67{i:01d}/0001-90",
            descricao=f"Descrição dos serviços {i:02d}"
        )
        fornecedores.append(fornecedor)
    return fornecedores

@pytest.fixture
def administrador_exemplo():
    # Cria um administrador de exemplo para os testes
    from model.usuario_model import Usuario, TipoUsuario
    administrador = Usuario(0, "Administrador Teste", "444.555.666-77", "1980-12-10", "admin@email.com", "(28) 99999-4000", "123456", TipoUsuario.ADMIN, None, None, None, None)
    return administrador

@pytest.fixture
def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo para os testes
    from model.usuario_model import Usuario, TipoUsuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(0, f"Administrador {i:02d}", f"444.555.66{i:01d}-77", f"198{i:01d}-12-10", f"admin{i:02d}@email.com", f"(28) 99999-40{i:02d}", "123456", TipoUsuario.ADMIN, None, None, None, None)
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
        casal = Casal(0, i, i + 1, 10000.0 + (i * 100))
        casais.append(casal)
    return casais

@pytest.fixture
def servico_exemplo():
    # Cria um serviço de exemplo para os testes
    from model.servico_model import Servico
    servico = Servico(0, "Serviço Teste", 100.0, "Descrição do serviço")
    return servico

@pytest.fixture
def lista_servicos_exemplo():
    # Cria uma lista de 10 serviços de exemplo para os testes
    from model.servico_model import Servico
    servicos = []
    for i in range(1, 11):
        servico = Servico(0, f"Serviço {i:02d}", 100.0 * i, f"Descrição do serviço {i:02d}")
        servicos.append(servico)
    return servicos

@pytest.fixture
def produto_exemplo():
    # Cria um produto de exemplo para os testes
    from model.produto_model import Produto
    produto = Produto(0, "Produto Teste", 19.99, "Descrição do produto teste")
    return produto

@pytest.fixture
def lista_produtos_exemplo():  
    # Cria uma lista de 10 produtos de exemplo para os testes
    from model.produto_model import Produto
    produtos = []
    for i in range(1, 11):
        produto = Produto(0, f"Produto {i:02d}", 19.99 + i, f"Descrição do produto {i:02d}")
        produtos.append(produto)
    return produtos    

@pytest.fixture
def demanda_exemplo():
    # Cria um demanda de exemplo para os testes
    from model.demanda_model import Demanda
    demanda = Demanda(
        id=0,
        id_casal=1,
        id_categoria=1,
        titulo="Demanda de teste",
        descricao="Descrição da demanda de teste"
    )
    return demanda

@pytest.fixture
def lista_demandas_exemplo():
    # Cria uma lista de 10 demandas de exemplo para os testes
    from model.demanda_model import Demanda
    demandas = []
    for i in range(1, 11):
        demanda = Demanda(
            id=0,
            id_casal=i,
            id_categoria=1,
            titulo=f"Demanda {i:02d}",
            descricao=f"Descrição da demanda {i:02d}"
        )
        demandas.append(demanda)
    return demandas

@pytest.fixture
def chat_exemplo():
    # Cria um chat de exemplo para os testes
    from model.chat_model import Chat
    chat = Chat(1, 2, datetime.now(), "Mensagem de teste", None)
    return chat

@pytest.fixture
def fornecedor_produto_exemplo():
    # Cria uma relação fornecedor-produto de exemplo para os testes
    from model.fornecedor_produto_model import FornecedorProduto
    fp = FornecedorProduto(1, 1, "Observações teste", 50.0)
    return fp

@pytest.fixture
def prestador_servico_exemplo():
    # Cria uma relação prestador-serviço de exemplo para os testes
    from model.prestador_servico_model import PrestadorServico
    ps = PrestadorServico(1, 1, "Observações teste", 100.0)
    return ps

@pytest.fixture
def item_demanda_produto_exemplo():
    # Cria um item demanda produto de exemplo para os testes
    from model.item_demanda_produto_model import ItemDemandaProduto
    item = ItemDemandaProduto(1, 1, 2, "Observações do item")
    return item

@pytest.fixture
def item_demanda_servico_exemplo():
    # Cria um item demanda serviço de exemplo para os testes
    from model.item_demanda_servico_model import ItemDemandaServico
    item = ItemDemandaServico(1, 1, 1, "Observações do serviço")
    return item

@pytest.fixture
def orcamento_exemplo():
    # Cria um orçamento de exemplo para os testes
    from model.orcamento_model import Orcamento
    orcamento = Orcamento(
        id=0,
        id_demanda=1,
        id_fornecedor_prestador=1,
        data_hora_cadastro=datetime.now(),
        data_hora_validade=None,
        status="PENDENTE",
        observacoes="Orçamento de teste",
        valor_total=1000.00
    )
    return orcamento

@pytest.fixture
def lista_orcamentos_exemplo():
    # Cria uma lista de 10 orçamentos de exemplo para os testes
    from model.orcamento_model import Orcamento
    orcamentos = []
    for i in range(1, 11):
        orcamento = Orcamento(
            id=0,
            id_demanda=1,
            id_fornecedor_prestador=i,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=None,
            status="PENDENTE",
            observacoes=f"Orçamento {i:02d}",
            valor_total=1000.00 * i
        )
        orcamentos.append(orcamento)
    return orcamentos

@pytest.fixture
def item_orcamento_produto_exemplo():
    # Cria um item orçamento produto de exemplo para os testes
    from model.item_orcamento_produto_model import ItemOrcamentoProduto
    item = ItemOrcamentoProduto(
        id_orcamento=1,
        id_produto=1,
        preco_unitario=50.00,
        quantidade=2,
        observacoes="Item de produto de teste"
    )
    return item

@pytest.fixture
def item_orcamento_servico_exemplo():
    # Cria um item orçamento serviço de exemplo para os testes
    from model.item_orcamento_servico_model import ItemOrcamentoServico
    item = ItemOrcamentoServico(
        id_orcamento=1,
        id_servico=1,
        preco_unitario=200.00,
        quantidade=1,
        observacoes="Item de serviço de teste"
    )
    return item
