# .gitignore

```
.venv
__pycache__
*.pyc
*.pyo
*.pyd

```

# .vscode/launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

# .vscode/settings.json

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

# dados.db

This is a binary file of the type: Binary

# data/insert_categorias.sql

```sql
INSERT INTO categoria (id, nome) VALUES
(1, 'Eletrônicos'),
(2, 'Roupas'),
(3, 'Calçados'),
(4, 'Alimentos'),
(5, 'Bebidas'),
(6, 'Móveis'),
(7, 'Decoração'),
(8, 'Livros'),
(9, 'Brinquedos'),
(10, 'Ferramentas');
```

# data/insert_clientes.sql

```sql
INSERT INTO cliente (nome, cpf, email, telefone, senha) VALUES
('Ana Silva', '123.456.789-01', 'ana.silva@email.com', '(11) 98765-4321', 'senha123'),
('Carlos Oliveira', '987.654.321-09', 'carlos.oliveira@email.com', '(11) 91234-5678', 'senha456'),
('Mariana Santos', '456.789.123-45', 'mariana.santos@email.com', '(21) 99876-5432', 'senha789'),
('João Pereira', '789.123.456-78', 'joao.pereira@email.com', '(21) 95432-1098', 'senha321'),
('Juliana Costa', '234.567.890-12', 'juliana.costa@email.com', '(31) 97654-3210', 'senha654'),
('Pedro Almeida', '345.678.901-23', 'pedro.almeida@email.com', '(31) 93210-9876', 'senha987'),
('Fernanda Lima', '567.890.123-45', 'fernanda.lima@email.com', '(41) 98765-1234', 'senha234'),
('Ricardo Souza', '678.901.234-56', 'ricardo.souza@email.com', '(41) 91234-5678', 'senha567'),
('Camila Ferreira', '890.123.456-67', 'camila.ferreira@email.com', '(51) 99876-2345', 'senha890'),
('Gustavo Ribeiro', '901.234.567-89', 'gustavo.ribeiro@email.com', '(51) 95432-7654', 'senha012'),
('Patrícia Martins', '012.345.678-90', 'patricia.martins@email.com', '(61) 97654-8901', 'senha345'),
('Lucas Rodrigues', '234.567.890-01', 'lucas.rodrigues@email.com', '(61) 93210-4321', 'senha678'),
('Amanda Gomes', '345.678.901-12', 'amanda.gomes@email.com', '(71) 98765-4567', 'senha901'),
('Rafael Barbosa', '456.789.012-23', 'rafael.barbosa@email.com', '(71) 91234-7890', 'senha234'),
('Thaís Carvalho', '567.890.123-34', 'thais.carvalho@email.com', '(81) 99876-0123', 'senha567'),
('Bruno Mendes', '678.901.234-45', 'bruno.mendes@email.com', '(81) 95432-3456', 'senha890'),
('Larissa Castro', '789.012.345-56', 'larissa.castro@email.com', '(91) 97654-6789', 'senha123'),
('Felipe Nunes', '890.123.456-67', 'felipe.nunes@email.com', '(91) 93210-9012', 'senha456'),
('Vanessa Cardoso', '901.234.567-78', 'vanessa.cardoso@email.com', '(12) 98765-3456', 'senha789'),
('Matheus Alves', '012.345.678-89', 'matheus.alves@email.com', '(12) 91234-6789', 'senha012'),
('Natália Torres', '123.456.789-90', 'natalia.torres@email.com', '(13) 99876-9012', 'senha345'),
('Diego Lopes', '234.567.890-01', 'diego.lopes@email.com', '(13) 95432-4567', 'senha678'),
('Bianca Moreira', '345.678.901-12', 'bianca.moreira@email.com', '(14) 97654-7890', 'senha901'),
('Vitor Pinto', '456.789.012-23', 'vitor.pinto@email.com', '(14) 93210-0123', 'senha234'),
('Letícia Araújo', '567.890.123-34', 'leticia.araujo@email.com', '(15) 98765-3456', 'senha567'),
('Henrique Farias', '678.901.234-45', 'henrique.farias@email.com', '(15) 91234-6789', 'senha890'),
('Carolina Rocha', '789.012.345-56', 'carolina.rocha@email.com', '(16) 99876-9012', 'senha123'),
('Alexandre Ramos', '890.123.456-67', 'alexandre.ramos@email.com', '(16) 95432-4567', 'senha456'),
('Daniela Vieira', '901.234.567-78', 'daniela.vieira@email.com', '(17) 97654-7890', 'senha789'),
('Leonardo Dias', '012.345.678-89', 'leonardo.dias@email.com', '(17) 93210-0123', 'senha012');
```

# data/insert_produtos.sql

```sql
INSERT INTO produto (nome, descricao, preco, quantidade) VALUES
('Smartphone Galaxy S23', 'Smartphone Samsung Galaxy S23 com 256GB de armazenamento e 8GB de RAM', 3999.99, 50),
('Notebook Dell Inspiron', 'Notebook Dell Inspiron com processador Intel Core i7, 16GB RAM e SSD de 512GB', 5499.90, 25),
('Smart TV LG 55"', 'Smart TV LG 55 polegadas 4K com webOS e HDR', 2899.00, 30),
('Fone de Ouvido JBL', 'Fone de ouvido JBL sem fio com cancelamento de ruído', 349.90, 100),
('Tablet iPad Air', 'Tablet Apple iPad Air com tela de 10.9 polegadas e 256GB', 4999.00, 20),
('Console PlayStation 5', 'Console PlayStation 5 com leitor de disco e controle DualSense', 4499.90, 15),
('Câmera Canon EOS', 'Câmera DSLR Canon EOS Rebel T7 com lente 18-55mm', 2599.00, 10),
('Monitor Samsung 27"', 'Monitor Samsung de 27 polegadas Full HD com taxa de atualização de 144Hz', 1599.90, 35),
('Impressora HP', 'Impressora multifuncional HP com Wi-Fi e scanner', 799.90, 40),
('Teclado Mecânico', 'Teclado mecânico gamer com iluminação RGB', 299.90, 60),
('Mouse Logitech', 'Mouse sem fio Logitech com sensor de alta precisão', 129.90, 75),
('Caixa de Som Bluetooth', 'Caixa de som portátil com Bluetooth e resistência à água', 249.90, 45),
('Smartwatch Apple Watch', 'Smartwatch Apple Watch Series 7 com GPS e caixa de alumínio', 2499.90, 30),
('Roteador Wi-Fi 6', 'Roteador Wi-Fi 6 dual band com suporte a Mesh', 599.90, 25),
('Webcam Logitech', 'Webcam Logitech Full HD para chamadas e streams', 399.90, 20),
('SSD Samsung 1TB', 'SSD Samsung 1TB com interface NVMe PCIe 4.0', 799.90, 40),
('Console Xbox Series X', 'Console Xbox Series X com 1TB de armazenamento', 4299.90, 15),
('Drone DJI Mini', 'Drone DJI Mini 2 com câmera 4K e autonomia de 31 minutos', 3999.90, 10),
('Máquina de Café', 'Máquina de café expresso automática com moedor de grãos', 1999.90, 18),
('Aspirador Robô', 'Aspirador robô inteligente com mapeamento a laser', 1499.90, 25),
('Purificador de Ar', 'Purificador de ar com filtro HEPA e sensor de qualidade', 899.90, 30),
('Fritadeira Elétrica', 'Fritadeira elétrica sem óleo com 4L de capacidade', 499.90, 50),
('Fogão 5 Bocas', 'Fogão 5 bocas com acendimento automático e forno autolimpante', 1299.90, 15),
('Refrigerador Duplex', 'Refrigerador duplex frost free com 450L de capacidade', 3499.90, 12),
('Lavadora de Roupas', 'Lavadora de roupas automática com capacidade para 12kg', 2199.90, 18),
('Ar Condicionado Split', 'Ar condicionado split inverter 12000 BTUs quente e frio', 1799.90, 20),
('Ventilador de Teto', 'Ventilador de teto com controle remoto e 3 velocidades', 399.90, 35),
('Micro-ondas', 'Micro-ondas 32L com painel digital e 10 níveis de potência', 699.90, 25),
('Smart Speaker Alexa', 'Smart speaker Amazon Echo com assistente virtual Alexa integrado', 349.90, 40),
('Cadeira Gamer', 'Cadeira gamer ergonômica com ajuste de altura e encosto reclinável', 899.90, 30);
```

# main.py

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets
import uvicorn

from repo import usuario_repo
from repo import admin_repo
from repo import cliente_repo
from repo import produto_repo
from repo import forma_pagamento_repo
from repo import categoria_repo

from routes.public_routes import router as public_router
from routes.admin_categorias_routes import router as admin_categorias_router
from routes.admin_produtos_routes import router as admin_produtos_router
from routes.admin_clientes_routes import router as admin_clientes_router
from routes.admin_formas_routes import router as admin_formas_pagamento_router
from routes.auth_routes import router as auth_router
from routes.perfil_routes import router as perfil_router
from routes.admin_usuarios_routes import router as admin_usuarios_router

app = FastAPI()

# Configurar SessionMiddleware com uma chave secreta segura
SECRET_KEY = "LgywzDkuDTHCvW0zW3KELYrNGCyI7C1grkVcLaEP4MelYy7VCgY4b42dJWgOLM3vLPGNX4ig4xHWDoEmPsc0IcGN7DvUNg3mTC04sieAYnERERz0Dn2USgoKrJOyEbDK"

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, defina como True se usar HTTPS
)

app.mount("/static", StaticFiles(directory="static"), name="static")

categoria_repo.criar_tabela()
produto_repo.criar_tabela()
usuario_repo.criar_tabela()
admin_repo.criar_tabela()
cliente_repo.criar_tabela()
forma_pagamento_repo.criar_tabela()

# Criar admin padrão ao inicializar
from util.criar_admin import criar_admin_padrao
criar_admin_padrao()

app.include_router(public_router)
app.include_router(admin_categorias_router, prefix="/admin/categorias")
app.include_router(admin_produtos_router, prefix="/admin/produtos")
app.include_router(admin_clientes_router, prefix="/admin/clientes")
app.include_router(admin_formas_pagamento_router, prefix="/admin/formas")
app.include_router(auth_router)
app.include_router(perfil_router)
app.include_router(admin_usuarios_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

```

# model/admin_model.py

```py
from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    master: bool

```

# model/categoria_model.py

```py
from dataclasses import dataclass


@dataclass
class Categoria:
    id: int
    nome: str
```

# model/cliente_model.py

```py
from dataclasses import dataclass


@dataclass
class Cliente:
    id: int
    cpf: str
    telefone: str

```

# model/forma_pagamento_model.py

```py
from dataclasses import dataclass


@dataclass
class FormaPagamento:
    id: int
    nome: str
    desconto: float

```

# model/produto_model.py

```py
from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
    categoria_id: int
    categoria_nome: str = None

    
```

# model/usuario_model.py

```py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    perfil: str = 'cliente'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None
```

# package.json

```json
{
  "dependencies": {
    "@anthropic-ai/claude-code": "^1.0.102"
  }
}

```

# repo/admin_repo.py

```py
from typing import Optional
from repo import usuario_repo
from model.admin_model import Admin
from sql.admin_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(admin: Admin) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            admin.nome, 
            admin.email, 
            admin.senha)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            id_usuario,
            admin.master))
        return id_usuario
    
def alterar(admin: Admin) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(admin.id, 
            admin.nome, 
            admin.email, 
            admin.senha)
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (
            admin.master,
            admin.id))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)

def obter_por_id(id: int) -> Optional[Admin]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        admin = Admin(
            id=row["id"],
            nome=row["nome"],            
            email=row["email"],
            senha=row["senha"],
            master=row["master"])
        return admin
    
def obter_todos() -> list[Admin]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        admins = [
            Admin(
                id=row["id"],
                nome=row["nome"],            
                email=row["email"],
                senha=row["senha"],
                master=row["master"]) 
                for row in rows]
        return admins
```

# repo/categoria_repo.py

```py
from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    
def inserir(categoria: Categoria) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome,))
        return cursor.lastrowid
    
def obter_todos() -> list[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        categorias = [
            Categoria(id=row["id"], nome=row["nome"])
            for row in rows]
        return categorias
    
def obter_por_id(id: int) -> Optional[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Categoria(id=row["id"], nome=row["nome"])
        return None
    
def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return (cursor.rowcount > 0)
    
def atualizar(categoria: Categoria) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (categoria.nome, categoria.id))
        return (cursor.rowcount > 0)
```

# repo/cliente_repo.py

```py
from typing import Optional
from repo import usuario_repo
from model.cliente_model import Cliente
from sql.cliente_sql import *
from model.usuario_model import Usuario
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(cliente: Cliente) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            cliente.nome, 
            cliente.email, 
            cliente.senha)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            id_usuario,
            cliente.cpf,
            cliente.telefone))
        return id_usuario
    
def alterar(cliente: Cliente) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(cliente.id, 
            cliente.nome, 
            cliente.email, 
            cliente.senha)
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (
            cliente.cpf,
            cliente.telefone,
            cliente.id))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)

def obter_por_id(id: int) -> Optional[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        cliente = Cliente(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            email=row["email"],
            telefone=row["telefone"],
            senha=row["senha"])
        return cliente
    
def obter_todos() -> list[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        clientes = [
            Cliente(
                id=row["id"], 
                nome=row["nome"], 
                cpf=row["cpf"],
                email=row["email"],
                telefone=row["telefone"],
                senha=row["senha"]) 
                for row in rows]
        return clientes
```

# repo/forma_pagamento_repo.py

```py
from typing import Optional
from model.forma_pagamento_model import FormaPagamento
from sql.forma_pagamento_sql import *
from util.db_util import get_connection


def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0


def inserir(forma_pagamento: FormaPagamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            forma_pagamento.nome, 
            forma_pagamento.desconto))
        id_inserido = cursor.lastrowid
        return id_inserido


def obter_todas() -> list[FormaPagamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [FormaPagamento(
            id=row["id"], 
            nome=row["nome"], 
            desconto=row["desconto"])
            for row in rows]


def obter_por_id(id: int) -> Optional[FormaPagamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return FormaPagamento(
                id=row["id"],
                nome=row["nome"],
                desconto=row["desconto"]
            )
        return None


def atualizar(forma_pagamento: FormaPagamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            forma_pagamento.nome,
            forma_pagamento.desconto,
            forma_pagamento.id
        ))
        return cursor.rowcount > 0


def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return cursor.rowcount > 0

```

# repo/produto_repo.py

```py
from typing import Optional
from model.produto_model import Produto
from sql.produto_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produto'")
        tabela_existe = cursor.fetchone() is not None
        
        if tabela_existe:
            # Verifica se a coluna categoria_id existe
            cursor.execute("PRAGMA table_info(produto)")
            colunas = cursor.fetchall()
            tem_categoria = any(col[1] == 'categoria_id' for col in colunas)
            
            if not tem_categoria:
                try:
                    # Adiciona a coluna categoria_id com valor padrão 1
                    cursor.execute("ALTER TABLE produto ADD COLUMN categoria_id INTEGER DEFAULT 1")
                    conn.commit()
                except:
                    pass
        else:
            # Cria a tabela nova com categoria_id
            cursor.execute(CRIAR_TABELA)
        
        return True

def inserir(produto: Produto) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            produto.nome, 
            produto.descricao, 
            produto.preco, 
            produto.quantidade,
            produto.categoria_id))
        return cursor.lastrowid

def obter_todos() -> list[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        produtos = [
            Produto(
                id=row["id"], 
                nome=row["nome"], 
                descricao=row["descricao"], 
                preco=row["preco"], 
                quantidade=row["quantidade"],
                categoria_id=row["categoria_id"],
                categoria_nome=row["categoria_nome"])
            for row in rows]
        return produtos
    
def obter_por_id(id: int) -> Optional[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            produto = Produto(
                id=row["id"], 
                nome=row["nome"], 
                descricao=row["descricao"], 
                preco=row["preco"], 
                quantidade=row["quantidade"],
                categoria_id=row["categoria_id"],
                categoria_nome=row["categoria_nome"])
            return produto
        return None
    

def excluir_por_id(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_POR_ID, (id,))
        return (cursor.rowcount > 0)

def alterar(produto: Produto) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.quantidade,
            produto.categoria_id,
            produto.id))
        return cursor.rowcount > 0
```

# repo/usuario_repo.py

```py
from typing import Any, Optional
from datetime import datetime
from model.usuario_model import Usuario
from sql.usuario_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return (cursor.rowcount > 0)

def inserir(usuario: Usuario, cursor: Any = None) -> Optional[int]:
    if cursor:
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.perfil))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.perfil))
            return cursor.lastrowid
    
def alterar(usuario: Usuario, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.id))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ALTERAR, (
                usuario.nome,
                usuario.email,
                usuario.id))
            return (cursor.rowcount > 0)
    
def atualizar_senha(id: int, senha: str, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(ALTERAR_SENHA, (senha, id))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ALTERAR_SENHA, (senha, id))
            return (cursor.rowcount > 0)
    
def excluir(id: int, cursor: Any = None) -> bool:
    if cursor:
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(EXCLUIR, (id,))
            return (cursor.rowcount > 0)
    
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"])
            return usuario
        return None

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"]) 
                for row in rows]
        return usuarios

def obter_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"])
            return usuario
        return None

def atualizar_token(email: str, token: str, data_expiracao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TOKEN, (token, data_expiracao, email))
        return (cursor.rowcount > 0)

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return (cursor.rowcount > 0)

def obter_por_token(token: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                    id=row["id"], 
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    perfil=row["perfil"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"])
            return usuario
        return None

def limpar_token(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET token_redefinicao=NULL, data_token=NULL WHERE id=?", (id,))
        return (cursor.rowcount > 0)

def obter_todos_por_perfil(perfil: str) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE perfil=? ORDER BY nome", (perfil,))
        rows = cursor.fetchall()
        usuarios = []
        for row in rows:
            usuario = Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                foto=row["foto"],
                data_cadastro=row["data_cadastro"]
            )
            usuarios.append(usuario)
        return usuarios
```

# requirements.txt

```txt
# pip install -r .\requirements.txt
fastapi[standard]
uvicorn[standard]
jinja2
python-multipart
passlib[bcrypt]
python-jose[cryptography]
itsdangerous
Pillow
```

# routes/admin_categorias_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.categoria_model import Categoria
from repo import categoria_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/categorias")

@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(request: Request, nome: str = Form(...), usuario_logado: dict = None):
    categoria = Categoria(id=0, nome=nome)
    categoria_id = categoria_repo.inserir(categoria)
    if categoria_id:
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar categoria."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(request: Request, id: int = Form(...), nome: str = Form(...), usuario_logado: dict = None):
    categoria = Categoria(id=id, nome=nome)
    if categoria_repo.atualizar(categoria):
        response = RedirectResponse(
            "/admin/categorias", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "mensagem": "Erro ao alterar categoria."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if categoria_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "mensagem": "Erro ao excluir categoria."},
    )

```

# routes/admin_clientes_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.cliente_model import Cliente
from repo import cliente_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/clientes")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    clientes = cliente_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "clientes": clientes}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: dict = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    cliente = Cliente(
        id=0,
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        senha=senha
    )
    cliente_id = cliente_repo.inserir(cliente)
    if cliente_id:
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar cliente."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(None),
    usuario_logado: dict = None
):
    # Se a senha não foi fornecida, buscar a senha atual
    if not senha:
        cliente_atual = cliente_repo.obter_por_id(id)
        senha = cliente_atual.senha if cliente_atual else ""
    
    cliente = Cliente(
        id=id,
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        senha=senha
    )
    if cliente_repo.alterar(cliente):
        response = RedirectResponse(
            "/admin/clientes", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao alterar cliente."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    cliente = cliente_repo.obter_por_id(id)
    if cliente:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "cliente": cliente}
        )
        return response
    return RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if cliente_repo.excluir(id):
        response = RedirectResponse("/admin/clientes", status.HTTP_303_SEE_OTHER)
        return response
    cliente = cliente_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "cliente": cliente, "mensagem": "Erro ao excluir cliente."},
    )
```

# routes/admin_formas_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.forma_pagamento_model import FormaPagamento
from repo import forma_pagamento_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/formas")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    formas = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "formas": formas}
    )
    return response


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(request: Request, nome: str = Form(...), desconto: float = Form(...), usuario_logado: dict = None):
    forma = FormaPagamento(id=0, nome=nome, desconto=desconto)
    forma_id = forma_pagamento_repo.inserir(forma)
    if forma_id:
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "cadastrar.html",
        {"request": request, "mensagem": "Erro ao cadastrar forma de pagamento."},
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(request: Request, id: int = Form(...), nome: str = Form(...), desconto: float = Form(...), usuario_logado: dict = None):
    forma = FormaPagamento(id=id, nome=nome, desconto=desconto)
    if forma_pagamento_repo.atualizar(forma):
        response = RedirectResponse(
            "/admin/formas", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "forma": forma, "mensagem": "Erro ao alterar forma de pagamento."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    forma = forma_pagamento_repo.obter_por_id(id)
    if forma:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "forma": forma}
        )
        return response
    return RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if forma_pagamento_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/formas", status.HTTP_303_SEE_OTHER)
        return response
    forma = forma_pagamento_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "forma": forma, "mensagem": "Erro ao excluir forma de pagamento."},
    )
```

# routes/admin_produtos_routes.py

```py
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
import os
from typing import Optional

from model.produto_model import Produto
from repo import produto_repo, categoria_repo
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao
from util.foto_util import (
    salvar_nova_foto, obter_foto_principal, obter_todas_fotos,
    excluir_foto, reordenar_fotos, obter_proximo_numero
)


router = APIRouter()
templates = criar_templates("templates/admin/produtos")


@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    produtos = produto_repo.obter_todos()

    # Adicionar informação de foto para cada produto
    for produto in produtos:
        produto.foto_principal = obter_foto_principal(produto.id)

    response = templates.TemplateResponse(
        "listar.html", {"request": request, "produtos": produtos}
    )
    return response


@router.get("/detalhar/{id}")
@requer_autenticacao(["admin"])
async def get_detalhar(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "detalhar.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "cadastrar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
    foto: Optional[UploadFile] = File(None),
    usuario_logado: dict = None
):
    produto = Produto(
        id=0,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        categoria_id=categoria_id,
    )
    produto_id = produto_repo.inserir(produto)
    if produto_id:
        # Salvar foto se foi enviada
        if foto and foto.filename:
            try:
                salvar_nova_foto(produto_id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto: {e}")

        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    categorias = categoria_repo.obter_todos()
    return templates.TemplateResponse(
        "cadastrar.html",
        {
            "request": request,
            "categorias": categorias,
            "mensagem": "Erro ao cadastrar produto.",
        },
    )


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    categorias = categoria_repo.obter_todos()
    if produto:
        foto_principal = obter_foto_principal(id)
        response = templates.TemplateResponse(
            "alterar.html",
            {
                "request": request,
                "produto": produto,
                "categorias": categorias,
                "foto_principal": foto_principal
            },
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
    foto: Optional[UploadFile] = File(None),
    usuario_logado: dict = None
):
    produto = Produto(
        id=id,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        categoria_id=categoria_id,
    )
    if produto_repo.alterar(produto):
        # Salvar nova foto se foi enviada
        if foto and foto.filename:
            try:
                salvar_nova_foto(id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto: {e}")

        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    categorias = categoria_repo.obter_todos()
    foto_principal = obter_foto_principal(id)
    return templates.TemplateResponse(
        "alterar.html",
        {
            "request": request,
            "produto": produto,
            "categorias": categorias,
            "foto_principal": foto_principal,
            "mensagem": "Erro ao alterar produto.",
        },
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "produto": produto}
        )
        return response
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if produto_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        return response
    produto = produto_repo.obter_por_id(id)
    return templates.TemplateResponse(
        "excluir.html",
        {
            "request": request,
            "produto": produto,
            "mensagem": "Erro ao excluir produto.",
        },
    )


@router.get("/{id}/galeria")
@requer_autenticacao(["admin"])
async def get_galeria(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    fotos = obter_todas_fotos(id)
    response = templates.TemplateResponse(
        "galeria.html",
        {
            "request": request,
            "produto": produto,
            "fotos": fotos
        }
    )
    return response


@router.post("/{id}/galeria/upload")
@requer_autenticacao(["admin"])
async def post_galeria_upload(
    request: Request,
    id: int,
    fotos: list[UploadFile] = File(...),
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    sucesso = 0
    for foto in fotos:
        if foto.filename:
            try:
                salvar_nova_foto(id, foto.file, como_principal=False)
                sucesso += 1
            except Exception as e:
                print(f"Erro ao salvar foto {foto.filename}: {e}")

    # Adicionar mensagem de sucesso via session ou query param
    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)


@router.post("/{id}/galeria/excluir/{numero}")
@requer_autenticacao(["admin"])
async def post_galeria_excluir(
    request: Request,
    id: int,
    numero: int,
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        excluir_foto(id, numero)
    except Exception as e:
        print(f"Erro ao excluir foto: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)


@router.post("/{id}/galeria/reordenar")
@requer_autenticacao(["admin"])
async def post_galeria_reordenar(
    request: Request,
    id: int,
    nova_ordem: str = Form(...),
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        # Converter string de números separados por vírgula em lista de inteiros
        ordem_lista = [int(x.strip()) for x in nova_ordem.split(",")]
        reordenar_fotos(id, ordem_lista)
    except Exception as e:
        print(f"Erro ao reordenar fotos: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)

```

# routes/admin_usuarios_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse

from model.usuario_model import Usuario
from repo import usuario_repo
from util.security import criar_hash_senha
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter(prefix="/admin/usuarios")
templates = criar_templates("templates/admin/usuarios")


@router.get("/lista")
@requer_autenticacao(["admin"])
async def get_lista(request: Request, usuario_logado: dict = None):
    usuarios_admin = usuario_repo.obter_todos_por_perfil("admin")
    return templates.TemplateResponse(
        "lista.html",
        {"request": request, "usuarios": usuarios_admin}
    )


@router.get("/cadastro")
@requer_autenticacao(["admin"])
async def get_cadastro(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request}
    )


@router.post("/cadastro")
@requer_autenticacao(["admin"])
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    # Verificar se o email já existe
    usuario_existente = usuario_repo.obter_por_email(email)
    if usuario_existente:
        return RedirectResponse(
            "/admin/usuarios/cadastro?erro=email_existe",
            status.HTTP_303_SEE_OTHER
        )
    
    # Criar o novo administrador
    senha_hash = criar_hash_senha(senha)
    usuario = Usuario(
        id=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        perfil="admin"
    )
    
    usuario_repo.inserir(usuario)
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )


@router.get("/alterar/{id:int}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )
    
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "usuario": usuario}
    )


@router.post("/alterar/{id:int}")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request,
    id: int,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(None),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )
    
    # Verificar se o novo email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_email(email)
    if usuario_existente and usuario_existente.id != id:
        return RedirectResponse(
            f"/admin/usuarios/alterar/{id}?erro=email_existe",
            status.HTTP_303_SEE_OTHER
        )
    
    # Atualizar dados
    usuario.nome = nome
    usuario.email = email
    
    # Se uma nova senha foi fornecida, atualizar
    if senha:
        senha_hash = criar_hash_senha(senha)
        usuario.senha = senha_hash
    
    usuario_repo.alterar(usuario)
    
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )


@router.get("/excluir/{id:int}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    # Não permitir auto-exclusão
    if id == usuario_logado['id']:
        return RedirectResponse(
            "/admin/usuarios/lista?erro=auto_exclusao",
            status.HTTP_303_SEE_OTHER
        )
    
    usuario = usuario_repo.obter_por_id(id)
    if not usuario or usuario.perfil != "admin":
        return RedirectResponse(
            "/admin/usuarios/lista",
            status.HTTP_303_SEE_OTHER
        )
    
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "usuario": usuario}
    )


@router.post("/excluir/{id:int}")
@requer_autenticacao(["admin"])
async def post_excluir(
    request: Request, 
    id: int, 
    usuario_logado: dict = None):
    # Não permitir auto-exclusão
    if id == usuario_logado['id']:
        return RedirectResponse(
            "/admin/usuarios/lista?erro=auto_exclusao",
            status.HTTP_303_SEE_OTHER
        )
    
    usuario = usuario_repo.obter_por_id(id)
    if usuario and usuario.perfil == "admin":
        usuario_repo.excluir(usuario)
    
    return RedirectResponse(
        "/admin/usuarios/lista",
        status.HTTP_303_SEE_OTHER
    )
```

# routes/auth_routes.py

```py
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from model.usuario_model import Usuario
from model.cliente_model import Cliente
from repo import usuario_repo, cliente_repo
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token, validar_forca_senha
from util.auth_decorator import criar_sessao, destruir_sessao, obter_usuario_logado, esta_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/auth")


@router.get("/login")
async def get_login(request: Request, redirect: str = None):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "redirect": redirect}
    )


@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    # Buscar usuário pelo email
    usuario = usuario_repo.obter_por_email(email)
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erro": "Email ou senha inválidos",
                "email": email,
                "redirect": redirect
            }
        )
    
    # Criar sessão
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    # Redirecionar para a página solicitada ou home
    url_redirect = redirect if redirect else "/"
    return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request):
    destruir_sessao(request)
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("cadastro.html", {"request": request})


@router.post("/cadastro")
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    # Validações
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": "As senhas não coincidem",
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone
            }
        )
    
    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": msg_erro,
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone
            }
        )
    
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": "Este email já está cadastrado",
                "nome": nome,
                "cpf": cpf,
                "telefone": telefone
            }
        )
    
    try:
        # Criar usuário com senha hash
        usuario = Usuario(
            id=0,
            nome=nome,
            email=email,
            senha=criar_hash_senha(senha),
            perfil='cliente'
        )
        
        # Inserir usuário e cliente
        from util.db_util import get_connection
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Inserir usuário
            usuario_id = usuario_repo.inserir(usuario, cursor)
            
            # Inserir dados do cliente
            cliente = Cliente(
                id=usuario_id,
                cpf=cpf,
                telefone=telefone
            )
            cursor.execute(
                "INSERT INTO cliente (id, cpf, telefone) VALUES (?, ?, ?)",
                (cliente.id, cliente.cpf, cliente.telefone)
            )
            
            conn.commit()
        
        # Fazer login automático após cadastro
        usuario_dict = {
            "id": usuario_id,
            "nome": nome,
            "email": email,
            "perfil": 'cliente',
            "foto": None
        }
        criar_sessao(request, usuario_dict)
        
        return RedirectResponse("/perfil", status.HTTP_303_SEE_OTHER)
        
    except Exception as e:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": f"Erro ao criar cadastro. Tente novamente. {e}",
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone
            }
        )


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})


@router.post("/esqueci-senha")
async def post_esqueci_senha(
    request: Request,
    email: str = Form(...)
):
    usuario = usuario_repo.obter_por_email(email)
    
    # Sempre mostrar mensagem de sucesso por segurança (não revelar emails válidos)
    mensagem_sucesso = "Se o email estiver cadastrado, você receberá instruções para redefinir sua senha."
    
    if usuario:
        # Gerar token e salvar no banco
        token = gerar_token_redefinicao()
        data_expiracao = obter_data_expiracao_token(24)  # 24 horas
        usuario_repo.atualizar_token(email, token, data_expiracao)
        
        # TODO: Enviar email com o link de redefinição
        # Por enquanto, vamos apenas mostrar o link (em produção, remover isso)
        link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
        
        return templates.TemplateResponse(
            "esqueci_senha.html",
            {
                "request": request,
                "sucesso": mensagem_sucesso,
                "debug_link": link_redefinicao  # Remover em produção
            }
        )
    
    return templates.TemplateResponse(
        "esqueci_senha.html",
        {
            "request": request,
            "sucesso": mensagem_sucesso
        }
    )


@router.get("/redefinir-senha/{token}")
async def get_redefinir_senha(request: Request, token: str):
    usuario = usuario_repo.obter_por_token(token)
    
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )
    
    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/redefinir-senha/{token}")
async def post_redefinir_senha(
    request: Request,
    token: str,
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    usuario = usuario_repo.obter_por_token(token)
    
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )
    
    # Validações
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": "As senhas não coincidem"
            }
        )
    
    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha e limpar token
    senha_hash = criar_hash_senha(senha)
    usuario_repo.atualizar_senha(usuario.id, senha_hash)
    usuario_repo.limpar_token(usuario.id)
    
    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "sucesso": "Senha redefinida com sucesso! Você já pode fazer login."
        }
    )
```

# routes/perfil_routes.py

```py
import os
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from model.usuario_model import Usuario
from model.cliente_model import Cliente
from repo import usuario_repo, cliente_repo
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/perfil")


@router.get("/perfil")
@requer_autenticacao()
async def get_perfil(request: Request, usuario_logado: dict = None):
    # Buscar dados completos do usuário
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Se for cliente, buscar dados adicionais
    cliente_dados = None
    if usuario.perfil == 'cliente':
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT cpf, telefone FROM cliente WHERE id=?", (usuario.id,))
                row = cursor.fetchone()
                if row:
                    cliente_dados = {
                        'cpf': row['cpf'],
                        'telefone': row['telefone']
                    }
        except:
            pass
    
    return templates.TemplateResponse(
        "dados.html",
        {
            "request": request,
            "usuario": usuario,
            "cliente_dados": cliente_dados
        }
    )


@router.post("/perfil")
@requer_autenticacao()
async def post_perfil(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(None),
    telefone: str = Form(None),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Verificar se o email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_email(email)
    if usuario_existente and usuario_existente.id != usuario.id:
        cliente_dados = None
        if usuario.perfil == 'cliente':
            try:
                from util.db_util import get_connection
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT cpf, telefone FROM cliente WHERE id=?", (usuario.id,))
                    row = cursor.fetchone()
                    if row:
                        cliente_dados = {
                            'cpf': row['cpf'],
                            'telefone': row['telefone']
                        }
            except:
                pass
        
        return templates.TemplateResponse(
            "dados.html",
            {
                "request": request,
                "usuario": usuario,
                "cliente_dados": cliente_dados,
                "erro": "Este email já está em uso"
            }
        )
    
    # Atualizar dados do usuário
    usuario.nome = nome
    usuario.email = email
    usuario_repo.alterar(usuario)
    
    # Se for cliente, atualizar dados adicionais
    if usuario.perfil == 'cliente' and cpf and telefone:
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE cliente SET cpf=?, telefone=? WHERE id=?",
                    (cpf, telefone, usuario.id)
                )
                conn.commit()
        except:
            pass
    
    # Atualizar sessão
    from util.auth_decorator import criar_sessao
    usuario_dict = {
        "id": usuario.id,
        "nome": nome,
        "email": email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    return RedirectResponse("/perfil?sucesso=1", status.HTTP_303_SEE_OTHER)


@router.get("/perfil/alterar-senha")
@requer_autenticacao()
async def get_alterar_senha(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "alterar_senha.html",
        {"request": request}
    )


@router.post("/perfil/alterar-senha")
@requer_autenticacao()
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    senha_nova: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = None
):
    usuario = usuario_repo.obter_por_id(usuario_logado['id'])
    
    # Verificar senha atual
    if not verificar_senha(senha_atual, usuario.senha):
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "Senha atual incorreta"
            }
        )
    
    # Verificar se as novas senhas coincidem
    if senha_nova != confirmar_senha:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "As novas senhas não coincidem"
            }
        )
    
    # Validar força da nova senha
    senha_valida, msg_erro = validar_forca_senha(senha_nova)
    if not senha_valida:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha
    senha_hash = criar_hash_senha(senha_nova)
    usuario_repo.atualizar_senha(usuario.id, senha_hash)
    
    return templates.TemplateResponse(
        "alterar_senha.html",
        {
            "request": request,
            "sucesso": "Senha alterada com sucesso!"
        }
    )


@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)
    
    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Gerar nome único para o arquivo
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)
    
    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
        
        # Atualizar caminho no banco
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)
        
        # Atualizar sessão
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)
        
    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)
```

# routes/public_routes.py

```py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from repo import produto_repo
from util.foto_util import obter_foto_principal


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    produtos = produto_repo.obter_todos()

    # Adicionar informação de foto para cada produto
    for produto in produtos:
        produto.foto_principal = obter_foto_principal(produto.id)

    response = templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})
    return response
```

# sql/admin_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS admin (
id INTEGER PRIMARY KEY,
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES usuario(id));
"""

INSERIR = """
INSERT INTO admin (master) 
VALUES (?)
"""

ALTERAR = """
UPDATE admin
SET master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM admin
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
a.id, a.master, u.nome, u.email, u.senha
FROM admin a
INNER JOIN usuario u ON a.id = u.id
WHERE a.id=?
"""

OBTER_TODOS = """
SELECT 
a.id, a.master, u.nome, u.email, u.senha
FROM admin a
INNER JOIN usuario u ON a.id = u.id
ORDER BY u.nome
""" 
```

# sql/categoria_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL);
"""

INSERIR = """
INSERT INTO categoria (nome)
VALUES (?)
"""

OBTER_TODOS = """
SELECT 
id, nome
FROM categoria
ORDER BY nome
"""

OBTER_POR_ID = """
SELECT 
id, nome
FROM categoria
WHERE id = ?
"""

ALTERAR = """
UPDATE categoria
SET nome=?
WHERE id=?
"""

EXCLUIR_POR_ID = """
DELETE FROM categoria
WHERE id=?
"""
```

# sql/cliente_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cliente (
id INTEGER PRIMARY KEY,
cpf TEXT NOT NULL,
telefone TEXT NOT NULL,
FOREIGN KEY (id) REFERENCES usuario(id)
);"""

INSERIR = """
INSERT INTO cliente (cpf, telefone) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE cliente
SET cpf=?, telefone=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM cliente
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
c.id, c.cpf, c.telefone, u.nome, u.email, u.senha
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
WHERE c.id=?
"""

OBTER_TODOS = """
SELECT 
c.id, c.cpf, c.telefone, u.nome, u.email, u.senha
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
ORDER BY u.nome
""" 
```

# sql/forma_pagamento_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS forma_pagamento (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
desconto REAL NOT NULL)
"""

INSERIR = """
INSERT INTO forma_pagamento (nome, desconto)
VALUES (?, ?)
"""

OBTER_TODOS = """
SELECT
id, nome, desconto
FROM forma_pagamento
ORDER BY nome
"""

OBTER_POR_ID = """
SELECT
id, nome, desconto
FROM forma_pagamento
WHERE id = ?
"""

ATUALIZAR = """
UPDATE forma_pagamento
SET nome = ?, desconto = ?
WHERE id = ?
"""

EXCLUIR_POR_ID = """
DELETE FROM forma_pagamento
WHERE id = ?
"""
```

# sql/produto_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS produto (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
descricao TEXT NOT NULL,
preco REAL NOT NULL,
quantidade INTEGER NOT NULL,
categoria_id INTEGER NOT NULL,
FOREIGN KEY (categoria_id) REFERENCES categoria(id))
"""

INSERIR = """
INSERT INTO produto (nome, descricao, preco, quantidade, categoria_id) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
p.id, p.nome, p.descricao, p.preco, p.quantidade, 
COALESCE(p.categoria_id, 1) as categoria_id, 
COALESCE(c.nome, 'Sem Categoria') as categoria_nome 
FROM produto p
LEFT JOIN categoria c ON p.categoria_id = c.id
ORDER BY p.nome
""" 

OBTER_POR_ID = """
SELECT 
p.id, p.nome, p.descricao, p.preco, p.quantidade, 
COALESCE(p.categoria_id, 1) as categoria_id, 
COALESCE(c.nome, 'Sem Categoria') as categoria_nome 
FROM produto p
LEFT JOIN categoria c ON p.categoria_id = c.id
WHERE p.id = ?
""" 

EXCLUIR_POR_ID = """
DELETE FROM produto WHERE id = ?
"""

ALTERAR = """
UPDATE produto 
SET nome = ?, descricao = ?, preco = ?, quantidade = ?, categoria_id = ?
WHERE id = ?
"""

ALTERAR_TABELA_ADD_CATEGORIA = """
ALTER TABLE produto ADD COLUMN categoria_id INTEGER REFERENCES categoria(id)
"""
```

# sql/usuario_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
senha TEXT NOT NULL,
perfil TEXT NOT NULL DEFAULT 'cliente',
foto TEXT,
token_redefinicao TEXT,
data_token TIMESTAMP
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, perfil)
VALUES (?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome=?, email=?
WHERE id=?
"""

ALTERAR_SENHA = """
UPDATE usuario
SET senha=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
id, nome, email, senha, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE id=?
"""

OBTER_TODOS = """
SELECT 
id, nome, email, senha, perfil, foto
FROM usuario
ORDER BY nome
"""

OBTER_POR_EMAIL = """
SELECT 
id, nome, email, senha, perfil, foto
FROM usuario
WHERE email=?
"""

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao=?, data_token=?
WHERE email=?
"""

ATUALIZAR_FOTO = """
UPDATE usuario
SET foto=?
WHERE id=?
"""

OBTER_POR_TOKEN = """
SELECT 
id, nome, email, senha, perfil, foto, token_redefinicao, data_token
FROM usuario
WHERE token_redefinicao=? AND data_token > datetime('now')
"""
```

# static/css/bootstrap.min.css

```css
@charset "UTF-8";/*!
 * Bootswatch v5.3.5 (https://bootswatch.com)
 * Theme: journal
 * Copyright 2012-2025 Thomas Park
 * Licensed under MIT
 * Based on Bootstrap
*//*!
 * Bootstrap  v5.3.5 (https://getbootstrap.com/)
 * Copyright 2011-2025 The Bootstrap Authors
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
 */@import url(https://fonts.googleapis.com/css2?family=News+Cycle:wght@400;700&display=swap);:root,[data-bs-theme=light]{--bs-blue:#eb6864;--bs-indigo:#6610f2;--bs-purple:#6f42c1;--bs-pink:#e83e8c;--bs-red:#f57a00;--bs-orange:#fd7e14;--bs-yellow:#f5e625;--bs-green:#22b24c;--bs-teal:#20c997;--bs-cyan:#369;--bs-black:#000;--bs-white:#fff;--bs-gray:#777;--bs-gray-dark:#333;--bs-gray-100:#f8f9fa;--bs-gray-200:#eee;--bs-gray-300:#dee2e6;--bs-gray-400:#ced4da;--bs-gray-500:#aaa;--bs-gray-600:#777;--bs-gray-700:#495057;--bs-gray-800:#333;--bs-gray-900:#222;--bs-primary:#eb6864;--bs-secondary:#aaa;--bs-success:#22b24c;--bs-info:#369;--bs-warning:#f5e625;--bs-danger:#f57a00;--bs-light:#f8f9fa;--bs-dark:#222;--bs-primary-rgb:235,104,100;--bs-secondary-rgb:170,170,170;--bs-success-rgb:34,178,76;--bs-info-rgb:51,102,153;--bs-warning-rgb:245,230,37;--bs-danger-rgb:245,122,0;--bs-light-rgb:248,249,250;--bs-dark-rgb:34,34,34;--bs-primary-text-emphasis:#5e2a28;--bs-secondary-text-emphasis:#444444;--bs-success-text-emphasis:#0e471e;--bs-info-text-emphasis:#14293d;--bs-warning-text-emphasis:#625c0f;--bs-danger-text-emphasis:#623100;--bs-light-text-emphasis:#495057;--bs-dark-text-emphasis:#495057;--bs-primary-bg-subtle:#fbe1e0;--bs-secondary-bg-subtle:#eeeeee;--bs-success-bg-subtle:#d3f0db;--bs-info-bg-subtle:#d6e0eb;--bs-warning-bg-subtle:#fdfad3;--bs-danger-bg-subtle:#fde4cc;--bs-light-bg-subtle:#fcfcfd;--bs-dark-bg-subtle:#ced4da;--bs-primary-border-subtle:#f7c3c1;--bs-secondary-border-subtle:#dddddd;--bs-success-border-subtle:#a7e0b7;--bs-info-border-subtle:#adc2d6;--bs-warning-border-subtle:#fbf5a8;--bs-danger-border-subtle:#fbca99;--bs-light-border-subtle:#eee;--bs-dark-border-subtle:#aaa;--bs-white-rgb:255,255,255;--bs-black-rgb:0,0,0;--bs-font-sans-serif:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Liberation Sans",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";--bs-font-monospace:SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;--bs-gradient:linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0));--bs-body-font-family:var(--bs-font-sans-serif);--bs-body-font-size:1rem;--bs-body-font-weight:400;--bs-body-line-height:1.5;--bs-body-color:#222;--bs-body-color-rgb:34,34,34;--bs-body-bg:#fff;--bs-body-bg-rgb:255,255,255;--bs-emphasis-color:#000;--bs-emphasis-color-rgb:0,0,0;--bs-secondary-color:rgba(34, 34, 34, 0.75);--bs-secondary-color-rgb:34,34,34;--bs-secondary-bg:#eee;--bs-secondary-bg-rgb:238,238,238;--bs-tertiary-color:rgba(34, 34, 34, 0.5);--bs-tertiary-color-rgb:34,34,34;--bs-tertiary-bg:#f8f9fa;--bs-tertiary-bg-rgb:248,249,250;--bs-heading-color:inherit;--bs-link-color:#eb6864;--bs-link-color-rgb:235,104,100;--bs-link-decoration:underline;--bs-link-hover-color:#bc5350;--bs-link-hover-color-rgb:188,83,80;--bs-code-color:#e83e8c;--bs-highlight-color:#222;--bs-highlight-bg:#fdfad3;--bs-border-width:1px;--bs-border-style:solid;--bs-border-color:#dee2e6;--bs-border-color-translucent:rgba(0, 0, 0, 0.175);--bs-border-radius:0.375rem;--bs-border-radius-sm:0.25rem;--bs-border-radius-lg:0.5rem;--bs-border-radius-xl:1rem;--bs-border-radius-xxl:2rem;--bs-border-radius-2xl:var(--bs-border-radius-xxl);--bs-border-radius-pill:50rem;--bs-box-shadow:0 0.5rem 1rem rgba(0, 0, 0, 0.15);--bs-box-shadow-sm:0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);--bs-box-shadow-lg:0 1rem 3rem rgba(0, 0, 0, 0.175);--bs-box-shadow-inset:inset 0 1px 2px rgba(0, 0, 0, 0.075);--bs-focus-ring-width:0.25rem;--bs-focus-ring-opacity:0.25;--bs-focus-ring-color:rgba(235, 104, 100, 0.25);--bs-form-valid-color:#22b24c;--bs-form-valid-border-color:#22b24c;--bs-form-invalid-color:#f57a00;--bs-form-invalid-border-color:#f57a00}[data-bs-theme=dark]{color-scheme:dark;--bs-body-color:#dee2e6;--bs-body-color-rgb:222,226,230;--bs-body-bg:#222;--bs-body-bg-rgb:34,34,34;--bs-emphasis-color:#fff;--bs-emphasis-color-rgb:255,255,255;--bs-secondary-color:rgba(222, 226, 230, 0.75);--bs-secondary-color-rgb:222,226,230;--bs-secondary-bg:#333;--bs-secondary-bg-rgb:51,51,51;--bs-tertiary-color:rgba(222, 226, 230, 0.5);--bs-tertiary-color-rgb:222,226,230;--bs-tertiary-bg:#2b2b2b;--bs-tertiary-bg-rgb:43,43,43;--bs-primary-text-emphasis:#f3a4a2;--bs-secondary-text-emphasis:#cccccc;--bs-success-text-emphasis:#7ad194;--bs-info-text-emphasis:#85a3c2;--bs-warning-text-emphasis:#f9f07c;--bs-danger-text-emphasis:#f9af66;--bs-light-text-emphasis:#f8f9fa;--bs-dark-text-emphasis:#dee2e6;--bs-primary-bg-subtle:#2f1514;--bs-secondary-bg-subtle:#222222;--bs-success-bg-subtle:#07240f;--bs-info-bg-subtle:#0a141f;--bs-warning-bg-subtle:#312e07;--bs-danger-bg-subtle:#311800;--bs-light-bg-subtle:#333;--bs-dark-bg-subtle:#1a1a1a;--bs-primary-border-subtle:#8d3e3c;--bs-secondary-border-subtle:#666666;--bs-success-border-subtle:#146b2e;--bs-info-border-subtle:#1f3d5c;--bs-warning-border-subtle:#938a16;--bs-danger-border-subtle:#934900;--bs-light-border-subtle:#495057;--bs-dark-border-subtle:#333;--bs-heading-color:inherit;--bs-link-color:#f3a4a2;--bs-link-hover-color:#f5b6b5;--bs-link-color-rgb:243,164,162;--bs-link-hover-color-rgb:245,182,181;--bs-code-color:#f18bba;--bs-highlight-color:#dee2e6;--bs-highlight-bg:#625c0f;--bs-border-color:#495057;--bs-border-color-translucent:rgba(255, 255, 255, 0.15);--bs-form-valid-color:#7ad194;--bs-form-valid-border-color:#7ad194;--bs-form-invalid-color:#f9af66;--bs-form-invalid-border-color:#f9af66}*,::after,::before{box-sizing:border-box}@media (prefers-reduced-motion:no-preference){:root{scroll-behavior:smooth}}body{margin:0;font-family:var(--bs-body-font-family);font-size:var(--bs-body-font-size);font-weight:var(--bs-body-font-weight);line-height:var(--bs-body-line-height);color:var(--bs-body-color);text-align:var(--bs-body-text-align);background-color:var(--bs-body-bg);-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}hr{margin:1rem 0;color:inherit;border:0;border-top:var(--bs-border-width) solid;opacity:.25}.h1,.h2,.h3,.h4,.h5,.h6,h1,h2,h3,h4,h5,h6{margin-top:0;margin-bottom:.5rem;font-family:"News Cycle","Arial Narrow Bold",sans-serif;font-weight:700;line-height:1.1;color:var(--bs-heading-color)}.h1,h1{font-size:calc(1.375rem + 1.5vw)}@media (min-width:1200px){.h1,h1{font-size:2.5rem}}.h2,h2{font-size:calc(1.325rem + .9vw)}@media (min-width:1200px){.h2,h2{font-size:2rem}}.h3,h3{font-size:calc(1.3rem + .6vw)}@media (min-width:1200px){.h3,h3{font-size:1.75rem}}.h4,h4{font-size:calc(1.275rem + .3vw)}@media (min-width:1200px){.h4,h4{font-size:1.5rem}}.h5,h5{font-size:1.25rem}.h6,h6{font-size:1rem}p{margin-top:0;margin-bottom:1rem}abbr[title]{-webkit-text-decoration:underline dotted;text-decoration:underline dotted;cursor:help;-webkit-text-decoration-skip-ink:none;text-decoration-skip-ink:none}address{margin-bottom:1rem;font-style:normal;line-height:inherit}ol,ul{padding-left:2rem}dl,ol,ul{margin-top:0;margin-bottom:1rem}ol ol,ol ul,ul ol,ul ul{margin-bottom:0}dt{font-weight:700}dd{margin-bottom:.5rem;margin-left:0}blockquote{margin:0 0 1rem}b,strong{font-weight:bolder}.small,small{font-size:.875em}.mark,mark{padding:.1875em;color:var(--bs-highlight-color);background-color:var(--bs-highlight-bg)}sub,sup{position:relative;font-size:.75em;line-height:0;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}a{color:rgba(var(--bs-link-color-rgb),var(--bs-link-opacity,1));text-decoration:underline}a:hover{--bs-link-color-rgb:var(--bs-link-hover-color-rgb)}a:not([href]):not([class]),a:not([href]):not([class]):hover{color:inherit;text-decoration:none}code,kbd,pre,samp{font-family:var(--bs-font-monospace);font-size:1em}pre{display:block;margin-top:0;margin-bottom:1rem;overflow:auto;font-size:.875em}pre code{font-size:inherit;color:inherit;word-break:normal}code{font-size:.875em;color:var(--bs-code-color);word-wrap:break-word}a>code{color:inherit}kbd{padding:.1875rem .375rem;font-size:.875em;color:var(--bs-body-bg);background-color:var(--bs-body-color);border-radius:.25rem}kbd kbd{padding:0;font-size:1em}figure{margin:0 0 1rem}img,svg{vertical-align:middle}table{caption-side:bottom;border-collapse:collapse}caption{padding-top:.5rem;padding-bottom:.5rem;color:var(--bs-secondary-color);text-align:left}th{text-align:inherit;text-align:-webkit-match-parent}tbody,td,tfoot,th,thead,tr{border-color:inherit;border-style:solid;border-width:0}label{display:inline-block}button{border-radius:0}button:focus:not(:focus-visible){outline:0}button,input,optgroup,select,textarea{margin:0;font-family:inherit;font-size:inherit;line-height:inherit}button,select{text-transform:none}[role=button]{cursor:pointer}select{word-wrap:normal}select:disabled{opacity:1}[list]:not([type=date]):not([type=datetime-local]):not([type=month]):not([type=week]):not([type=time])::-webkit-calendar-picker-indicator{display:none!important}[type=button],[type=reset],[type=submit],button{-webkit-appearance:button}[type=button]:not(:disabled),[type=reset]:not(:disabled),[type=submit]:not(:disabled),button:not(:disabled){cursor:pointer}::-moz-focus-inner{padding:0;border-style:none}textarea{resize:vertical}fieldset{min-width:0;padding:0;margin:0;border:0}legend{float:left;width:100%;padding:0;margin-bottom:.5rem;line-height:inherit;font-size:calc(1.275rem + .3vw)}@media (min-width:1200px){legend{font-size:1.5rem}}legend+*{clear:left}::-webkit-datetime-edit-day-field,::-webkit-datetime-edit-fields-wrapper,::-webkit-datetime-edit-hour-field,::-webkit-datetime-edit-minute,::-webkit-datetime-edit-month-field,::-webkit-datetime-edit-text,::-webkit-datetime-edit-year-field{padding:0}::-webkit-inner-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-color-swatch-wrapper{padding:0}::-webkit-file-upload-button{font:inherit;-webkit-appearance:button}::file-selector-button{font:inherit;-webkit-appearance:button}output{display:inline-block}iframe{border:0}summary{display:list-item;cursor:pointer}progress{vertical-align:baseline}[hidden]{display:none!important}.lead{font-size:1.25rem;font-weight:300}.display-1{font-weight:300;line-height:1.1;font-size:calc(1.625rem + 4.5vw)}@media (min-width:1200px){.display-1{font-size:5rem}}.display-2{font-weight:300;line-height:1.1;font-size:calc(1.575rem + 3.9vw)}@media (min-width:1200px){.display-2{font-size:4.5rem}}.display-3{font-weight:300;line-height:1.1;font-size:calc(1.525rem + 3.3vw)}@media (min-width:1200px){.display-3{font-size:4rem}}.display-4{font-weight:300;line-height:1.1;font-size:calc(1.475rem + 2.7vw)}@media (min-width:1200px){.display-4{font-size:3.5rem}}.display-5{font-weight:300;line-height:1.1;font-size:calc(1.425rem + 2.1vw)}@media (min-width:1200px){.display-5{font-size:3rem}}.display-6{font-weight:300;line-height:1.1;font-size:calc(1.375rem + 1.5vw)}@media (min-width:1200px){.display-6{font-size:2.5rem}}.list-unstyled{padding-left:0;list-style:none}.list-inline{padding-left:0;list-style:none}.list-inline-item{display:inline-block}.list-inline-item:not(:last-child){margin-right:.5rem}.initialism{font-size:.875em;text-transform:uppercase}.blockquote{margin-bottom:1rem;font-size:1.25rem}.blockquote>:last-child{margin-bottom:0}.blockquote-footer{margin-top:-1rem;margin-bottom:1rem;font-size:.875em;color:#777}.blockquote-footer::before{content:"— "}.img-fluid{max-width:100%;height:auto}.img-thumbnail{padding:.25rem;background-color:var(--bs-body-bg);border:var(--bs-border-width) solid var(--bs-border-color);border-radius:var(--bs-border-radius);max-width:100%;height:auto}.figure{display:inline-block}.figure-img{margin-bottom:.5rem;line-height:1}.figure-caption{font-size:.875em;color:var(--bs-secondary-color)}.container,.container-fluid,.container-lg,.container-md,.container-sm,.container-xl,.container-xxl{--bs-gutter-x:1.5rem;--bs-gutter-y:0;width:100%;padding-right:calc(var(--bs-gutter-x) * .5);padding-left:calc(var(--bs-gutter-x) * .5);margin-right:auto;margin-left:auto}@media (min-width:576px){.container,.container-sm{max-width:540px}}@media (min-width:768px){.container,.container-md,.container-sm{max-width:720px}}@media (min-width:992px){.container,.container-lg,.container-md,.container-sm{max-width:960px}}@media (min-width:1200px){.container,.container-lg,.container-md,.container-sm,.container-xl{max-width:1140px}}@media (min-width:1400px){.container,.container-lg,.container-md,.container-sm,.container-xl,.container-xxl{max-width:1320px}}:root{--bs-breakpoint-xs:0;--bs-breakpoint-sm:576px;--bs-breakpoint-md:768px;--bs-breakpoint-lg:992px;--bs-breakpoint-xl:1200px;--bs-breakpoint-xxl:1400px}.row{--bs-gutter-x:1.5rem;--bs-gutter-y:0;display:flex;flex-wrap:wrap;margin-top:calc(-1 * var(--bs-gutter-y));margin-right:calc(-.5 * var(--bs-gutter-x));margin-left:calc(-.5 * var(--bs-gutter-x))}.row>*{flex-shrink:0;width:100%;max-width:100%;padding-right:calc(var(--bs-gutter-x) * .5);padding-left:calc(var(--bs-gutter-x) * .5);margin-top:var(--bs-gutter-y)}.col{flex:1 0 0}.row-cols-auto>*{flex:0 0 auto;width:auto}.row-cols-1>*{flex:0 0 auto;width:100%}.row-cols-2>*{flex:0 0 auto;width:50%}.row-cols-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-4>*{flex:0 0 auto;width:25%}.row-cols-5>*{flex:0 0 auto;width:20%}.row-cols-6>*{flex:0 0 auto;width:16.66666667%}.col-auto{flex:0 0 auto;width:auto}.col-1{flex:0 0 auto;width:8.33333333%}.col-2{flex:0 0 auto;width:16.66666667%}.col-3{flex:0 0 auto;width:25%}.col-4{flex:0 0 auto;width:33.33333333%}.col-5{flex:0 0 auto;width:41.66666667%}.col-6{flex:0 0 auto;width:50%}.col-7{flex:0 0 auto;width:58.33333333%}.col-8{flex:0 0 auto;width:66.66666667%}.col-9{flex:0 0 auto;width:75%}.col-10{flex:0 0 auto;width:83.33333333%}.col-11{flex:0 0 auto;width:91.66666667%}.col-12{flex:0 0 auto;width:100%}.offset-1{margin-left:8.33333333%}.offset-2{margin-left:16.66666667%}.offset-3{margin-left:25%}.offset-4{margin-left:33.33333333%}.offset-5{margin-left:41.66666667%}.offset-6{margin-left:50%}.offset-7{margin-left:58.33333333%}.offset-8{margin-left:66.66666667%}.offset-9{margin-left:75%}.offset-10{margin-left:83.33333333%}.offset-11{margin-left:91.66666667%}.g-0,.gx-0{--bs-gutter-x:0}.g-0,.gy-0{--bs-gutter-y:0}.g-1,.gx-1{--bs-gutter-x:0.25rem}.g-1,.gy-1{--bs-gutter-y:0.25rem}.g-2,.gx-2{--bs-gutter-x:0.5rem}.g-2,.gy-2{--bs-gutter-y:0.5rem}.g-3,.gx-3{--bs-gutter-x:1rem}.g-3,.gy-3{--bs-gutter-y:1rem}.g-4,.gx-4{--bs-gutter-x:1.5rem}.g-4,.gy-4{--bs-gutter-y:1.5rem}.g-5,.gx-5{--bs-gutter-x:3rem}.g-5,.gy-5{--bs-gutter-y:3rem}@media (min-width:576px){.col-sm{flex:1 0 0}.row-cols-sm-auto>*{flex:0 0 auto;width:auto}.row-cols-sm-1>*{flex:0 0 auto;width:100%}.row-cols-sm-2>*{flex:0 0 auto;width:50%}.row-cols-sm-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-sm-4>*{flex:0 0 auto;width:25%}.row-cols-sm-5>*{flex:0 0 auto;width:20%}.row-cols-sm-6>*{flex:0 0 auto;width:16.66666667%}.col-sm-auto{flex:0 0 auto;width:auto}.col-sm-1{flex:0 0 auto;width:8.33333333%}.col-sm-2{flex:0 0 auto;width:16.66666667%}.col-sm-3{flex:0 0 auto;width:25%}.col-sm-4{flex:0 0 auto;width:33.33333333%}.col-sm-5{flex:0 0 auto;width:41.66666667%}.col-sm-6{flex:0 0 auto;width:50%}.col-sm-7{flex:0 0 auto;width:58.33333333%}.col-sm-8{flex:0 0 auto;width:66.66666667%}.col-sm-9{flex:0 0 auto;width:75%}.col-sm-10{flex:0 0 auto;width:83.33333333%}.col-sm-11{flex:0 0 auto;width:91.66666667%}.col-sm-12{flex:0 0 auto;width:100%}.offset-sm-0{margin-left:0}.offset-sm-1{margin-left:8.33333333%}.offset-sm-2{margin-left:16.66666667%}.offset-sm-3{margin-left:25%}.offset-sm-4{margin-left:33.33333333%}.offset-sm-5{margin-left:41.66666667%}.offset-sm-6{margin-left:50%}.offset-sm-7{margin-left:58.33333333%}.offset-sm-8{margin-left:66.66666667%}.offset-sm-9{margin-left:75%}.offset-sm-10{margin-left:83.33333333%}.offset-sm-11{margin-left:91.66666667%}.g-sm-0,.gx-sm-0{--bs-gutter-x:0}.g-sm-0,.gy-sm-0{--bs-gutter-y:0}.g-sm-1,.gx-sm-1{--bs-gutter-x:0.25rem}.g-sm-1,.gy-sm-1{--bs-gutter-y:0.25rem}.g-sm-2,.gx-sm-2{--bs-gutter-x:0.5rem}.g-sm-2,.gy-sm-2{--bs-gutter-y:0.5rem}.g-sm-3,.gx-sm-3{--bs-gutter-x:1rem}.g-sm-3,.gy-sm-3{--bs-gutter-y:1rem}.g-sm-4,.gx-sm-4{--bs-gutter-x:1.5rem}.g-sm-4,.gy-sm-4{--bs-gutter-y:1.5rem}.g-sm-5,.gx-sm-5{--bs-gutter-x:3rem}.g-sm-5,.gy-sm-5{--bs-gutter-y:3rem}}@media (min-width:768px){.col-md{flex:1 0 0}.row-cols-md-auto>*{flex:0 0 auto;width:auto}.row-cols-md-1>*{flex:0 0 auto;width:100%}.row-cols-md-2>*{flex:0 0 auto;width:50%}.row-cols-md-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-md-4>*{flex:0 0 auto;width:25%}.row-cols-md-5>*{flex:0 0 auto;width:20%}.row-cols-md-6>*{flex:0 0 auto;width:16.66666667%}.col-md-auto{flex:0 0 auto;width:auto}.col-md-1{flex:0 0 auto;width:8.33333333%}.col-md-2{flex:0 0 auto;width:16.66666667%}.col-md-3{flex:0 0 auto;width:25%}.col-md-4{flex:0 0 auto;width:33.33333333%}.col-md-5{flex:0 0 auto;width:41.66666667%}.col-md-6{flex:0 0 auto;width:50%}.col-md-7{flex:0 0 auto;width:58.33333333%}.col-md-8{flex:0 0 auto;width:66.66666667%}.col-md-9{flex:0 0 auto;width:75%}.col-md-10{flex:0 0 auto;width:83.33333333%}.col-md-11{flex:0 0 auto;width:91.66666667%}.col-md-12{flex:0 0 auto;width:100%}.offset-md-0{margin-left:0}.offset-md-1{margin-left:8.33333333%}.offset-md-2{margin-left:16.66666667%}.offset-md-3{margin-left:25%}.offset-md-4{margin-left:33.33333333%}.offset-md-5{margin-left:41.66666667%}.offset-md-6{margin-left:50%}.offset-md-7{margin-left:58.33333333%}.offset-md-8{margin-left:66.66666667%}.offset-md-9{margin-left:75%}.offset-md-10{margin-left:83.33333333%}.offset-md-11{margin-left:91.66666667%}.g-md-0,.gx-md-0{--bs-gutter-x:0}.g-md-0,.gy-md-0{--bs-gutter-y:0}.g-md-1,.gx-md-1{--bs-gutter-x:0.25rem}.g-md-1,.gy-md-1{--bs-gutter-y:0.25rem}.g-md-2,.gx-md-2{--bs-gutter-x:0.5rem}.g-md-2,.gy-md-2{--bs-gutter-y:0.5rem}.g-md-3,.gx-md-3{--bs-gutter-x:1rem}.g-md-3,.gy-md-3{--bs-gutter-y:1rem}.g-md-4,.gx-md-4{--bs-gutter-x:1.5rem}.g-md-4,.gy-md-4{--bs-gutter-y:1.5rem}.g-md-5,.gx-md-5{--bs-gutter-x:3rem}.g-md-5,.gy-md-5{--bs-gutter-y:3rem}}@media (min-width:992px){.col-lg{flex:1 0 0}.row-cols-lg-auto>*{flex:0 0 auto;width:auto}.row-cols-lg-1>*{flex:0 0 auto;width:100%}.row-cols-lg-2>*{flex:0 0 auto;width:50%}.row-cols-lg-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-lg-4>*{flex:0 0 auto;width:25%}.row-cols-lg-5>*{flex:0 0 auto;width:20%}.row-cols-lg-6>*{flex:0 0 auto;width:16.66666667%}.col-lg-auto{flex:0 0 auto;width:auto}.col-lg-1{flex:0 0 auto;width:8.33333333%}.col-lg-2{flex:0 0 auto;width:16.66666667%}.col-lg-3{flex:0 0 auto;width:25%}.col-lg-4{flex:0 0 auto;width:33.33333333%}.col-lg-5{flex:0 0 auto;width:41.66666667%}.col-lg-6{flex:0 0 auto;width:50%}.col-lg-7{flex:0 0 auto;width:58.33333333%}.col-lg-8{flex:0 0 auto;width:66.66666667%}.col-lg-9{flex:0 0 auto;width:75%}.col-lg-10{flex:0 0 auto;width:83.33333333%}.col-lg-11{flex:0 0 auto;width:91.66666667%}.col-lg-12{flex:0 0 auto;width:100%}.offset-lg-0{margin-left:0}.offset-lg-1{margin-left:8.33333333%}.offset-lg-2{margin-left:16.66666667%}.offset-lg-3{margin-left:25%}.offset-lg-4{margin-left:33.33333333%}.offset-lg-5{margin-left:41.66666667%}.offset-lg-6{margin-left:50%}.offset-lg-7{margin-left:58.33333333%}.offset-lg-8{margin-left:66.66666667%}.offset-lg-9{margin-left:75%}.offset-lg-10{margin-left:83.33333333%}.offset-lg-11{margin-left:91.66666667%}.g-lg-0,.gx-lg-0{--bs-gutter-x:0}.g-lg-0,.gy-lg-0{--bs-gutter-y:0}.g-lg-1,.gx-lg-1{--bs-gutter-x:0.25rem}.g-lg-1,.gy-lg-1{--bs-gutter-y:0.25rem}.g-lg-2,.gx-lg-2{--bs-gutter-x:0.5rem}.g-lg-2,.gy-lg-2{--bs-gutter-y:0.5rem}.g-lg-3,.gx-lg-3{--bs-gutter-x:1rem}.g-lg-3,.gy-lg-3{--bs-gutter-y:1rem}.g-lg-4,.gx-lg-4{--bs-gutter-x:1.5rem}.g-lg-4,.gy-lg-4{--bs-gutter-y:1.5rem}.g-lg-5,.gx-lg-5{--bs-gutter-x:3rem}.g-lg-5,.gy-lg-5{--bs-gutter-y:3rem}}@media (min-width:1200px){.col-xl{flex:1 0 0}.row-cols-xl-auto>*{flex:0 0 auto;width:auto}.row-cols-xl-1>*{flex:0 0 auto;width:100%}.row-cols-xl-2>*{flex:0 0 auto;width:50%}.row-cols-xl-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-xl-4>*{flex:0 0 auto;width:25%}.row-cols-xl-5>*{flex:0 0 auto;width:20%}.row-cols-xl-6>*{flex:0 0 auto;width:16.66666667%}.col-xl-auto{flex:0 0 auto;width:auto}.col-xl-1{flex:0 0 auto;width:8.33333333%}.col-xl-2{flex:0 0 auto;width:16.66666667%}.col-xl-3{flex:0 0 auto;width:25%}.col-xl-4{flex:0 0 auto;width:33.33333333%}.col-xl-5{flex:0 0 auto;width:41.66666667%}.col-xl-6{flex:0 0 auto;width:50%}.col-xl-7{flex:0 0 auto;width:58.33333333%}.col-xl-8{flex:0 0 auto;width:66.66666667%}.col-xl-9{flex:0 0 auto;width:75%}.col-xl-10{flex:0 0 auto;width:83.33333333%}.col-xl-11{flex:0 0 auto;width:91.66666667%}.col-xl-12{flex:0 0 auto;width:100%}.offset-xl-0{margin-left:0}.offset-xl-1{margin-left:8.33333333%}.offset-xl-2{margin-left:16.66666667%}.offset-xl-3{margin-left:25%}.offset-xl-4{margin-left:33.33333333%}.offset-xl-5{margin-left:41.66666667%}.offset-xl-6{margin-left:50%}.offset-xl-7{margin-left:58.33333333%}.offset-xl-8{margin-left:66.66666667%}.offset-xl-9{margin-left:75%}.offset-xl-10{margin-left:83.33333333%}.offset-xl-11{margin-left:91.66666667%}.g-xl-0,.gx-xl-0{--bs-gutter-x:0}.g-xl-0,.gy-xl-0{--bs-gutter-y:0}.g-xl-1,.gx-xl-1{--bs-gutter-x:0.25rem}.g-xl-1,.gy-xl-1{--bs-gutter-y:0.25rem}.g-xl-2,.gx-xl-2{--bs-gutter-x:0.5rem}.g-xl-2,.gy-xl-2{--bs-gutter-y:0.5rem}.g-xl-3,.gx-xl-3{--bs-gutter-x:1rem}.g-xl-3,.gy-xl-3{--bs-gutter-y:1rem}.g-xl-4,.gx-xl-4{--bs-gutter-x:1.5rem}.g-xl-4,.gy-xl-4{--bs-gutter-y:1.5rem}.g-xl-5,.gx-xl-5{--bs-gutter-x:3rem}.g-xl-5,.gy-xl-5{--bs-gutter-y:3rem}}@media (min-width:1400px){.col-xxl{flex:1 0 0}.row-cols-xxl-auto>*{flex:0 0 auto;width:auto}.row-cols-xxl-1>*{flex:0 0 auto;width:100%}.row-cols-xxl-2>*{flex:0 0 auto;width:50%}.row-cols-xxl-3>*{flex:0 0 auto;width:33.33333333%}.row-cols-xxl-4>*{flex:0 0 auto;width:25%}.row-cols-xxl-5>*{flex:0 0 auto;width:20%}.row-cols-xxl-6>*{flex:0 0 auto;width:16.66666667%}.col-xxl-auto{flex:0 0 auto;width:auto}.col-xxl-1{flex:0 0 auto;width:8.33333333%}.col-xxl-2{flex:0 0 auto;width:16.66666667%}.col-xxl-3{flex:0 0 auto;width:25%}.col-xxl-4{flex:0 0 auto;width:33.33333333%}.col-xxl-5{flex:0 0 auto;width:41.66666667%}.col-xxl-6{flex:0 0 auto;width:50%}.col-xxl-7{flex:0 0 auto;width:58.33333333%}.col-xxl-8{flex:0 0 auto;width:66.66666667%}.col-xxl-9{flex:0 0 auto;width:75%}.col-xxl-10{flex:0 0 auto;width:83.33333333%}.col-xxl-11{flex:0 0 auto;width:91.66666667%}.col-xxl-12{flex:0 0 auto;width:100%}.offset-xxl-0{margin-left:0}.offset-xxl-1{margin-left:8.33333333%}.offset-xxl-2{margin-left:16.66666667%}.offset-xxl-3{margin-left:25%}.offset-xxl-4{margin-left:33.33333333%}.offset-xxl-5{margin-left:41.66666667%}.offset-xxl-6{margin-left:50%}.offset-xxl-7{margin-left:58.33333333%}.offset-xxl-8{margin-left:66.66666667%}.offset-xxl-9{margin-left:75%}.offset-xxl-10{margin-left:83.33333333%}.offset-xxl-11{margin-left:91.66666667%}.g-xxl-0,.gx-xxl-0{--bs-gutter-x:0}.g-xxl-0,.gy-xxl-0{--bs-gutter-y:0}.g-xxl-1,.gx-xxl-1{--bs-gutter-x:0.25rem}.g-xxl-1,.gy-xxl-1{--bs-gutter-y:0.25rem}.g-xxl-2,.gx-xxl-2{--bs-gutter-x:0.5rem}.g-xxl-2,.gy-xxl-2{--bs-gutter-y:0.5rem}.g-xxl-3,.gx-xxl-3{--bs-gutter-x:1rem}.g-xxl-3,.gy-xxl-3{--bs-gutter-y:1rem}.g-xxl-4,.gx-xxl-4{--bs-gutter-x:1.5rem}.g-xxl-4,.gy-xxl-4{--bs-gutter-y:1.5rem}.g-xxl-5,.gx-xxl-5{--bs-gutter-x:3rem}.g-xxl-5,.gy-xxl-5{--bs-gutter-y:3rem}}.table{--bs-table-color-type:initial;--bs-table-bg-type:initial;--bs-table-color-state:initial;--bs-table-bg-state:initial;--bs-table-color:initial;--bs-table-bg:var(--bs-body-bg);--bs-table-border-color:var(--bs-border-color);--bs-table-accent-bg:transparent;--bs-table-striped-color:initial;--bs-table-striped-bg:rgba(var(--bs-emphasis-color-rgb), 0.05);--bs-table-active-color:initial;--bs-table-active-bg:rgba(var(--bs-emphasis-color-rgb), 0.1);--bs-table-hover-color:initial;--bs-table-hover-bg:rgba(var(--bs-emphasis-color-rgb), 0.075);width:100%;margin-bottom:1rem;vertical-align:top;border-color:var(--bs-table-border-color)}.table>:not(caption)>*>*{padding:.5rem .5rem;color:var(--bs-table-color-state,var(--bs-table-color-type,var(--bs-table-color)));background-color:var(--bs-table-bg);border-bottom-width:var(--bs-border-width);box-shadow:inset 0 0 0 9999px var(--bs-table-bg-state,var(--bs-table-bg-type,var(--bs-table-accent-bg)))}.table>tbody{vertical-align:inherit}.table>thead{vertical-align:bottom}.table-group-divider{border-top:calc(var(--bs-border-width) * 2) solid currentcolor}.caption-top{caption-side:top}.table-sm>:not(caption)>*>*{padding:.25rem .25rem}.table-bordered>:not(caption)>*{border-width:var(--bs-border-width) 0}.table-bordered>:not(caption)>*>*{border-width:0 var(--bs-border-width)}.table-borderless>:not(caption)>*>*{border-bottom-width:0}.table-borderless>:not(:first-child){border-top-width:0}.table-striped>tbody>tr:nth-of-type(odd)>*{--bs-table-color-type:var(--bs-table-striped-color);--bs-table-bg-type:var(--bs-table-striped-bg)}.table-striped-columns>:not(caption)>tr>:nth-child(2n){--bs-table-color-type:var(--bs-table-striped-color);--bs-table-bg-type:var(--bs-table-striped-bg)}.table-active{--bs-table-color-state:var(--bs-table-active-color);--bs-table-bg-state:var(--bs-table-active-bg)}.table-hover>tbody>tr:hover>*{--bs-table-color-state:var(--bs-table-hover-color);--bs-table-bg-state:var(--bs-table-hover-bg)}.table-primary{--bs-table-color:#000;--bs-table-bg:#fbe1e0;--bs-table-border-color:#c9b4b3;--bs-table-striped-bg:#eed6d5;--bs-table-striped-color:#fff;--bs-table-active-bg:#e2cbca;--bs-table-active-color:#fff;--bs-table-hover-bg:#e8d0cf;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-secondary{--bs-table-color:#000;--bs-table-bg:#eeeeee;--bs-table-border-color:#bebebe;--bs-table-striped-bg:#e2e2e2;--bs-table-striped-color:#fff;--bs-table-active-bg:#d6d6d6;--bs-table-active-color:#fff;--bs-table-hover-bg:gainsboro;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-success{--bs-table-color:#000;--bs-table-bg:#d3f0db;--bs-table-border-color:#a9c0af;--bs-table-striped-bg:#c8e4d0;--bs-table-striped-color:#fff;--bs-table-active-bg:#bed8c5;--bs-table-active-color:#fff;--bs-table-hover-bg:#c3decb;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-info{--bs-table-color:#fff;--bs-table-bg:#d6e0eb;--bs-table-border-color:#dee6ef;--bs-table-striped-bg:#d8e2ec;--bs-table-striped-color:#fff;--bs-table-active-bg:#dae3ed;--bs-table-active-color:#fff;--bs-table-hover-bg:#d9e2ed;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-warning{--bs-table-color:#000;--bs-table-bg:#fdfad3;--bs-table-border-color:#cac8a9;--bs-table-striped-bg:#f0eec8;--bs-table-striped-color:#000;--bs-table-active-bg:#e4e1be;--bs-table-active-color:#fff;--bs-table-hover-bg:#eae7c3;--bs-table-hover-color:#000;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-danger{--bs-table-color:#000;--bs-table-bg:#fde4cc;--bs-table-border-color:#cab6a3;--bs-table-striped-bg:#f0d9c2;--bs-table-striped-color:#fff;--bs-table-active-bg:#e4cdb8;--bs-table-active-color:#fff;--bs-table-hover-bg:#ead3bd;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-light{--bs-table-color:#000;--bs-table-bg:#f8f9fa;--bs-table-border-color:#c6c7c8;--bs-table-striped-bg:#ecedee;--bs-table-striped-color:#000;--bs-table-active-bg:#dfe0e1;--bs-table-active-color:#fff;--bs-table-hover-bg:#e5e6e7;--bs-table-hover-color:#000;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-dark{--bs-table-color:#fff;--bs-table-bg:#222;--bs-table-border-color:#4e4e4e;--bs-table-striped-bg:#2d2d2d;--bs-table-striped-color:#fff;--bs-table-active-bg:#383838;--bs-table-active-color:#fff;--bs-table-hover-bg:#333333;--bs-table-hover-color:#fff;color:var(--bs-table-color);border-color:var(--bs-table-border-color)}.table-responsive{overflow-x:auto;-webkit-overflow-scrolling:touch}@media (max-width:575.98px){.table-responsive-sm{overflow-x:auto;-webkit-overflow-scrolling:touch}}@media (max-width:767.98px){.table-responsive-md{overflow-x:auto;-webkit-overflow-scrolling:touch}}@media (max-width:991.98px){.table-responsive-lg{overflow-x:auto;-webkit-overflow-scrolling:touch}}@media (max-width:1199.98px){.table-responsive-xl{overflow-x:auto;-webkit-overflow-scrolling:touch}}@media (max-width:1399.98px){.table-responsive-xxl{overflow-x:auto;-webkit-overflow-scrolling:touch}}.form-label{margin-bottom:.5rem}.col-form-label{padding-top:calc(.375rem + var(--bs-border-width));padding-bottom:calc(.375rem + var(--bs-border-width));margin-bottom:0;font-size:inherit;line-height:1.5}.col-form-label-lg{padding-top:calc(.5rem + var(--bs-border-width));padding-bottom:calc(.5rem + var(--bs-border-width));font-size:1.25rem}.col-form-label-sm{padding-top:calc(.25rem + var(--bs-border-width));padding-bottom:calc(.25rem + var(--bs-border-width));font-size:.875rem}.form-text{margin-top:.25rem;font-size:.875em;color:var(--bs-secondary-color)}.form-control{display:block;width:100%;padding:.375rem 1rem;font-size:1rem;font-weight:400;line-height:1.5;color:var(--bs-body-color);-webkit-appearance:none;-moz-appearance:none;appearance:none;background-color:var(--bs-body-bg);background-clip:padding-box;border:var(--bs-border-width) solid var(--bs-border-color);border-radius:var(--bs-border-radius);transition:border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-control{transition:none}}.form-control[type=file]{overflow:hidden}.form-control[type=file]:not(:disabled):not([readonly]){cursor:pointer}.form-control:focus{color:var(--bs-body-color);background-color:var(--bs-body-bg);border-color:#f5b4b2;outline:0;box-shadow:0 0 0 .25rem rgba(235,104,100,.25)}.form-control::-webkit-date-and-time-value{min-width:85px;height:1.5em;margin:0}.form-control::-webkit-datetime-edit{display:block;padding:0}.form-control::-moz-placeholder{color:var(--bs-secondary-color);opacity:1}.form-control::placeholder{color:var(--bs-secondary-color);opacity:1}.form-control:disabled{background-color:var(--bs-secondary-bg);opacity:1}.form-control::-webkit-file-upload-button{padding:.375rem 1rem;margin:-.375rem -1rem;-webkit-margin-end:1rem;margin-inline-end:1rem;color:var(--bs-body-color);background-color:var(--bs-tertiary-bg);pointer-events:none;border-color:inherit;border-style:solid;border-width:0;border-inline-end-width:var(--bs-border-width);border-radius:0;-webkit-transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}.form-control::file-selector-button{padding:.375rem 1rem;margin:-.375rem -1rem;-webkit-margin-end:1rem;margin-inline-end:1rem;color:var(--bs-body-color);background-color:var(--bs-tertiary-bg);pointer-events:none;border-color:inherit;border-style:solid;border-width:0;border-inline-end-width:var(--bs-border-width);border-radius:0;transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-control::-webkit-file-upload-button{-webkit-transition:none;transition:none}.form-control::file-selector-button{transition:none}}.form-control:hover:not(:disabled):not([readonly])::-webkit-file-upload-button{background-color:var(--bs-secondary-bg)}.form-control:hover:not(:disabled):not([readonly])::file-selector-button{background-color:var(--bs-secondary-bg)}.form-control-plaintext{display:block;width:100%;padding:.375rem 0;margin-bottom:0;line-height:1.5;color:var(--bs-body-color);background-color:transparent;border:solid transparent;border-width:var(--bs-border-width) 0}.form-control-plaintext:focus{outline:0}.form-control-plaintext.form-control-lg,.form-control-plaintext.form-control-sm{padding-right:0;padding-left:0}.form-control-sm{min-height:calc(1.5em + .5rem + calc(var(--bs-border-width) * 2));padding:.25rem .5rem;font-size:.875rem;border-radius:var(--bs-border-radius-sm)}.form-control-sm::-webkit-file-upload-button{padding:.25rem .5rem;margin:-.25rem -.5rem;-webkit-margin-end:.5rem;margin-inline-end:.5rem}.form-control-sm::file-selector-button{padding:.25rem .5rem;margin:-.25rem -.5rem;-webkit-margin-end:.5rem;margin-inline-end:.5rem}.form-control-lg{min-height:calc(1.5em + 1rem + calc(var(--bs-border-width) * 2));padding:.5rem 1rem;font-size:1.25rem;border-radius:var(--bs-border-radius-lg)}.form-control-lg::-webkit-file-upload-button{padding:.5rem 1rem;margin:-.5rem -1rem;-webkit-margin-end:1rem;margin-inline-end:1rem}.form-control-lg::file-selector-button{padding:.5rem 1rem;margin:-.5rem -1rem;-webkit-margin-end:1rem;margin-inline-end:1rem}textarea.form-control{min-height:calc(1.5em + .75rem + calc(var(--bs-border-width) * 2))}textarea.form-control-sm{min-height:calc(1.5em + .5rem + calc(var(--bs-border-width) * 2))}textarea.form-control-lg{min-height:calc(1.5em + 1rem + calc(var(--bs-border-width) * 2))}.form-control-color{width:3rem;height:calc(1.5em + .75rem + calc(var(--bs-border-width) * 2));padding:.375rem}.form-control-color:not(:disabled):not([readonly]){cursor:pointer}.form-control-color::-moz-color-swatch{border:0!important;border-radius:var(--bs-border-radius)}.form-control-color::-webkit-color-swatch{border:0!important;border-radius:var(--bs-border-radius)}.form-control-color.form-control-sm{height:calc(1.5em + .5rem + calc(var(--bs-border-width) * 2))}.form-control-color.form-control-lg{height:calc(1.5em + 1rem + calc(var(--bs-border-width) * 2))}.form-select{--bs-form-select-bg-img:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23333' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");display:block;width:100%;padding:.375rem 3rem .375rem 1rem;font-size:1rem;font-weight:400;line-height:1.5;color:var(--bs-body-color);-webkit-appearance:none;-moz-appearance:none;appearance:none;background-color:var(--bs-body-bg);background-image:var(--bs-form-select-bg-img),var(--bs-form-select-bg-icon,none);background-repeat:no-repeat;background-position:right 1rem center;background-size:16px 12px;border:var(--bs-border-width) solid var(--bs-border-color);border-radius:var(--bs-border-radius);transition:border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-select{transition:none}}.form-select:focus{border-color:#f5b4b2;outline:0;box-shadow:0 0 0 .25rem rgba(235,104,100,.25)}.form-select[multiple],.form-select[size]:not([size="1"]){padding-right:1rem;background-image:none}.form-select:disabled{background-color:var(--bs-secondary-bg)}.form-select:-moz-focusring{color:transparent;text-shadow:0 0 0 var(--bs-body-color)}.form-select-sm{padding-top:.25rem;padding-bottom:.25rem;padding-left:.5rem;font-size:.875rem;border-radius:var(--bs-border-radius-sm)}.form-select-lg{padding-top:.5rem;padding-bottom:.5rem;padding-left:1rem;font-size:1.25rem;border-radius:var(--bs-border-radius-lg)}[data-bs-theme=dark] .form-select{--bs-form-select-bg-img:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23dee2e6' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e")}.form-check{display:block;min-height:1.5rem;padding-left:1.5em;margin-bottom:.125rem}.form-check .form-check-input{float:left;margin-left:-1.5em}.form-check-reverse{padding-right:1.5em;padding-left:0;text-align:right}.form-check-reverse .form-check-input{float:right;margin-right:-1.5em;margin-left:0}.form-check-input{--bs-form-check-bg:var(--bs-body-bg);flex-shrink:0;width:1em;height:1em;margin-top:.25em;vertical-align:top;-webkit-appearance:none;-moz-appearance:none;appearance:none;background-color:var(--bs-form-check-bg);background-image:var(--bs-form-check-bg-image);background-repeat:no-repeat;background-position:center;background-size:contain;border:var(--bs-border-width) solid var(--bs-border-color);-webkit-print-color-adjust:exact;color-adjust:exact;print-color-adjust:exact}.form-check-input[type=checkbox]{border-radius:.25em}.form-check-input[type=radio]{border-radius:50%}.form-check-input:active{filter:brightness(90%)}.form-check-input:focus{border-color:#f5b4b2;outline:0;box-shadow:0 0 0 .25rem rgba(235,104,100,.25)}.form-check-input:checked{background-color:#eb6864;border-color:#eb6864}.form-check-input:checked[type=checkbox]{--bs-form-check-bg-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3e%3cpath fill='none' stroke='%23fff' stroke-linecap='round' stroke-linejoin='round' stroke-width='3' d='m6 10 3 3 6-6'/%3e%3c/svg%3e")}.form-check-input:checked[type=radio]{--bs-form-check-bg-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='2' fill='%23fff'/%3e%3c/svg%3e")}.form-check-input[type=checkbox]:indeterminate{background-color:#eb6864;border-color:#eb6864;--bs-form-check-bg-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3e%3cpath fill='none' stroke='%23fff' stroke-linecap='round' stroke-linejoin='round' stroke-width='3' d='M6 10h8'/%3e%3c/svg%3e")}.form-check-input:disabled{pointer-events:none;filter:none;opacity:.5}.form-check-input:disabled~.form-check-label,.form-check-input[disabled]~.form-check-label{cursor:default;opacity:.5}.form-switch{padding-left:2.5em}.form-switch .form-check-input{--bs-form-switch-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba%280, 0, 0, 0.25%29'/%3e%3c/svg%3e");width:2em;margin-left:-2.5em;background-image:var(--bs-form-switch-bg);background-position:left center;border-radius:2em;transition:background-position .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-switch .form-check-input{transition:none}}.form-switch .form-check-input:focus{--bs-form-switch-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23f5b4b2'/%3e%3c/svg%3e")}.form-switch .form-check-input:checked{background-position:right center;--bs-form-switch-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23fff'/%3e%3c/svg%3e")}.form-switch.form-check-reverse{padding-right:2.5em;padding-left:0}.form-switch.form-check-reverse .form-check-input{margin-right:-2.5em;margin-left:0}.form-check-inline{display:inline-block;margin-right:1rem}.btn-check{position:absolute;clip:rect(0,0,0,0);pointer-events:none}.btn-check:disabled+.btn,.btn-check[disabled]+.btn{pointer-events:none;filter:none;opacity:.65}[data-bs-theme=dark] .form-switch .form-check-input:not(:checked):not(:focus){--bs-form-switch-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba%28255, 255, 255, 0.25%29'/%3e%3c/svg%3e")}.form-range{width:100%;height:1.5rem;padding:0;-webkit-appearance:none;-moz-appearance:none;appearance:none;background-color:transparent}.form-range:focus{outline:0}.form-range:focus::-webkit-slider-thumb{box-shadow:0 0 0 1px #fff,0 0 0 .25rem rgba(235,104,100,.25)}.form-range:focus::-moz-range-thumb{box-shadow:0 0 0 1px #fff,0 0 0 .25rem rgba(235,104,100,.25)}.form-range::-moz-focus-outer{border:0}.form-range::-webkit-slider-thumb{width:1rem;height:1rem;margin-top:-.25rem;-webkit-appearance:none;appearance:none;background-color:#eb6864;border:0;border-radius:1rem;-webkit-transition:background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;transition:background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-range::-webkit-slider-thumb{-webkit-transition:none;transition:none}}.form-range::-webkit-slider-thumb:active{background-color:#f9d2d1}.form-range::-webkit-slider-runnable-track{width:100%;height:.5rem;color:transparent;cursor:pointer;background-color:var(--bs-secondary-bg);border-color:transparent;border-radius:1rem}.form-range::-moz-range-thumb{width:1rem;height:1rem;-moz-appearance:none;appearance:none;background-color:#eb6864;border:0;border-radius:1rem;-moz-transition:background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;transition:background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.form-range::-moz-range-thumb{-moz-transition:none;transition:none}}.form-range::-moz-range-thumb:active{background-color:#f9d2d1}.form-range::-moz-range-track{width:100%;height:.5rem;color:transparent;cursor:pointer;background-color:var(--bs-secondary-bg);border-color:transparent;border-radius:1rem}.form-range:disabled{pointer-events:none}.form-range:disabled::-webkit-slider-thumb{background-color:var(--bs-secondary-color)}.form-range:disabled::-moz-range-thumb{background-color:var(--bs-secondary-color)}.form-floating{position:relative}.form-floating>.form-control,.form-floating>.form-control-plaintext,.form-floating>.form-select{height:calc(3.5rem + calc(var(--bs-border-width) * 2));min-height:calc(3.5rem + calc(var(--bs-border-width) * 2));line-height:1.25}.form-floating>label{position:absolute;top:0;left:0;z-index:2;max-width:100%;height:100%;padding:1rem 1rem;overflow:hidden;color:rgba(var(--bs-body-color-rgb),.65);text-align:start;text-overflow:ellipsis;white-space:nowrap;pointer-events:none;border:var(--bs-border-width) solid transparent;transform-origin:0 0;transition:opacity .1s ease-in-out,transform .1s ease-in-out}@media (prefers-reduced-motion:reduce){.form-floating>label{transition:none}}.form-floating>.form-control,.form-floating>.form-control-plaintext{padding:1rem 1rem}.form-floating>.form-control-plaintext::-moz-placeholder,.form-floating>.form-control::-moz-placeholder{color:transparent}.form-floating>.form-control-plaintext::placeholder,.form-floating>.form-control::placeholder{color:transparent}.form-floating>.form-control-plaintext:not(:-moz-placeholder-shown),.form-floating>.form-control:not(:-moz-placeholder-shown){padding-top:1.625rem;padding-bottom:.625rem}.form-floating>.form-control-plaintext:focus,.form-floating>.form-control-plaintext:not(:placeholder-shown),.form-floating>.form-control:focus,.form-floating>.form-control:not(:placeholder-shown){padding-top:1.625rem;padding-bottom:.625rem}.form-floating>.form-control-plaintext:-webkit-autofill,.form-floating>.form-control:-webkit-autofill{padding-top:1.625rem;padding-bottom:.625rem}.form-floating>.form-select{padding-top:1.625rem;padding-bottom:.625rem;padding-left:1rem}.form-floating>.form-control:not(:-moz-placeholder-shown)~label{transform:scale(.85) translateY(-.5rem) translateX(.15rem)}.form-floating>.form-control-plaintext~label,.form-floating>.form-control:focus~label,.form-floating>.form-control:not(:placeholder-shown)~label,.form-floating>.form-select~label{transform:scale(.85) translateY(-.5rem) translateX(.15rem)}.form-floating>.form-control:-webkit-autofill~label{transform:scale(.85) translateY(-.5rem) translateX(.15rem)}.form-floating>textarea:not(:-moz-placeholder-shown)~label::after{position:absolute;inset:1rem 0.5rem;z-index:-1;height:1.5em;content:"";background-color:var(--bs-body-bg);border-radius:var(--bs-border-radius)}.form-floating>textarea:focus~label::after,.form-floating>textarea:not(:placeholder-shown)~label::after{position:absolute;inset:1rem 0.5rem;z-index:-1;height:1.5em;content:"";background-color:var(--bs-body-bg);border-radius:var(--bs-border-radius)}.form-floating>textarea:disabled~label::after{background-color:var(--bs-secondary-bg)}.form-floating>.form-control-plaintext~label{border-width:var(--bs-border-width) 0}.form-floating>.form-control:disabled~label,.form-floating>:disabled~label{color:#777}.input-group{position:relative;display:flex;flex-wrap:wrap;align-items:stretch;width:100%}.input-group>.form-control,.input-group>.form-floating,.input-group>.form-select{position:relative;flex:1 1 auto;width:1%;min-width:0}.input-group>.form-control:focus,.input-group>.form-floating:focus-within,.input-group>.form-select:focus{z-index:5}.input-group .btn{position:relative;z-index:2}.input-group .btn:focus{z-index:5}.input-group-text{display:flex;align-items:center;padding:.375rem 1rem;font-size:1rem;font-weight:400;line-height:1.5;color:var(--bs-body-color);text-align:center;white-space:nowrap;background-color:var(--bs-tertiary-bg);border:var(--bs-border-width) solid var(--bs-border-color);border-radius:var(--bs-border-radius)}.input-group-lg>.btn,.input-group-lg>.form-control,.input-group-lg>.form-select,.input-group-lg>.input-group-text{padding:.5rem 1rem;font-size:1.25rem;border-radius:var(--bs-border-radius-lg)}.input-group-sm>.btn,.input-group-sm>.form-control,.input-group-sm>.form-select,.input-group-sm>.input-group-text{padding:.25rem .5rem;font-size:.875rem;border-radius:var(--bs-border-radius-sm)}.input-group-lg>.form-select,.input-group-sm>.form-select{padding-right:4rem}.input-group:not(.has-validation)>.dropdown-toggle:nth-last-child(n+3),.input-group:not(.has-validation)>.form-floating:not(:last-child)>.form-control,.input-group:not(.has-validation)>.form-floating:not(:last-child)>.form-select,.input-group:not(.has-validation)>:not(:last-child):not(.dropdown-toggle):not(.dropdown-menu):not(.form-floating){border-top-right-radius:0;border-bottom-right-radius:0}.input-group.has-validation>.dropdown-toggle:nth-last-child(n+4),.input-group.has-validation>.form-floating:nth-last-child(n+3)>.form-control,.input-group.has-validation>.form-floating:nth-last-child(n+3)>.form-select,.input-group.has-validation>:nth-last-child(n+3):not(.dropdown-toggle):not(.dropdown-menu):not(.form-floating){border-top-right-radius:0;border-bottom-right-radius:0}.input-group>:not(:first-child):not(.dropdown-menu):not(.valid-tooltip):not(.valid-feedback):not(.invalid-tooltip):not(.invalid-feedback){margin-left:calc(-1 * var(--bs-border-width));border-top-left-radius:0;border-bottom-left-radius:0}.input-group>.form-floating:not(:first-child)>.form-control,.input-group>.form-floating:not(:first-child)>.form-select{border-top-left-radius:0;border-bottom-left-radius:0}.valid-feedback{display:none;width:100%;margin-top:.25rem;font-size:.875em;color:var(--bs-form-valid-color)}.valid-tooltip{position:absolute;top:100%;z-index:5;display:none;max-width:100%;padding:.25rem .5rem;margin-top:.1rem;font-size:.875rem;color:#fff;background-color:var(--bs-success);border-radius:var(--bs-border-radius)}.is-valid~.valid-feedback,.is-valid~.valid-tooltip,.was-validated :valid~.valid-feedback,.was-validated :valid~.valid-tooltip{display:block}.form-control.is-valid,.was-validated .form-control:valid{border-color:var(--bs-form-valid-border-color);padding-right:calc(1.5em + .75rem);background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%2322b24c' d='M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1'/%3e%3c/svg%3e");background-repeat:no-repeat;background-position:right calc(.375em + .1875rem) center;background-size:calc(.75em + .375rem) calc(.75em + .375rem)}.form-control.is-valid:focus,.was-validated .form-control:valid:focus{border-color:var(--bs-form-valid-border-color);box-shadow:0 0 0 .25rem rgba(var(--bs-success-rgb),.25)}.was-validated textarea.form-control:valid,textarea.form-control.is-valid{padding-right:calc(1.5em + .75rem);background-position:top calc(.375em + .1875rem) right calc(.375em + .1875rem)}.form-select.is-valid,.was-validated .form-select:valid{border-color:var(--bs-form-valid-border-color)}.form-select.is-valid:not([multiple]):not([size]),.form-select.is-valid:not([multiple])[size="1"],.was-validated .form-select:valid:not([multiple]):not([size]),.was-validated .form-select:valid:not([multiple])[size="1"]{--bs-form-select-bg-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%2322b24c' d='M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1'/%3e%3c/svg%3e");padding-right:5.5rem;background-position:right 1rem center,center right 3rem;background-size:16px 12px,calc(.75em + .375rem) calc(.75em + .375rem)}.form-select.is-valid:focus,.was-validated .form-select:valid:focus{border-color:var(--bs-form-valid-border-color);box-shadow:0 0 0 .25rem rgba(var(--bs-success-rgb),.25)}.form-control-color.is-valid,.was-validated .form-control-color:valid{width:calc(3rem + calc(1.5em + .75rem))}.form-check-input.is-valid,.was-validated .form-check-input:valid{border-color:var(--bs-form-valid-border-color)}.form-check-input.is-valid:checked,.was-validated .form-check-input:valid:checked{background-color:var(--bs-form-valid-color)}.form-check-input.is-valid:focus,.was-validated .form-check-input:valid:focus{box-shadow:0 0 0 .25rem rgba(var(--bs-success-rgb),.25)}.form-check-input.is-valid~.form-check-label,.was-validated .form-check-input:valid~.form-check-label{color:var(--bs-form-valid-color)}.form-check-inline .form-check-input~.valid-feedback{margin-left:.5em}.input-group>.form-control:not(:focus).is-valid,.input-group>.form-floating:not(:focus-within).is-valid,.input-group>.form-select:not(:focus).is-valid,.was-validated .input-group>.form-control:not(:focus):valid,.was-validated .input-group>.form-floating:not(:focus-within):valid,.was-validated .input-group>.form-select:not(:focus):valid{z-index:3}.invalid-feedback{display:none;width:100%;margin-top:.25rem;font-size:.875em;color:var(--bs-form-invalid-color)}.invalid-tooltip{position:absolute;top:100%;z-index:5;display:none;max-width:100%;padding:.25rem .5rem;margin-top:.1rem;font-size:.875rem;color:#fff;background-color:var(--bs-danger);border-radius:var(--bs-border-radius)}.is-invalid~.invalid-feedback,.is-invalid~.invalid-tooltip,.was-validated :invalid~.invalid-feedback,.was-validated :invalid~.invalid-tooltip{display:block}.form-control.is-invalid,.was-validated .form-control:invalid{border-color:var(--bs-form-invalid-border-color);padding-right:calc(1.5em + .75rem);background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23f57a00'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23f57a00' stroke='none'/%3e%3c/svg%3e");background-repeat:no-repeat;background-position:right calc(.375em + .1875rem) center;background-size:calc(.75em + .375rem) calc(.75em + .375rem)}.form-control.is-invalid:focus,.was-validated .form-control:invalid:focus{border-color:var(--bs-form-invalid-border-color);box-shadow:0 0 0 .25rem rgba(var(--bs-danger-rgb),.25)}.was-validated textarea.form-control:invalid,textarea.form-control.is-invalid{padding-right:calc(1.5em + .75rem);background-position:top calc(.375em + .1875rem) right calc(.375em + .1875rem)}.form-select.is-invalid,.was-validated .form-select:invalid{border-color:var(--bs-form-invalid-border-color)}.form-select.is-invalid:not([multiple]):not([size]),.form-select.is-invalid:not([multiple])[size="1"],.was-validated .form-select:invalid:not([multiple]):not([size]),.was-validated .form-select:invalid:not([multiple])[size="1"]{--bs-form-select-bg-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23f57a00'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23f57a00' stroke='none'/%3e%3c/svg%3e");padding-right:5.5rem;background-position:right 1rem center,center right 3rem;background-size:16px 12px,calc(.75em + .375rem) calc(.75em + .375rem)}.form-select.is-invalid:focus,.was-validated .form-select:invalid:focus{border-color:var(--bs-form-invalid-border-color);box-shadow:0 0 0 .25rem rgba(var(--bs-danger-rgb),.25)}.form-control-color.is-invalid,.was-validated .form-control-color:invalid{width:calc(3rem + calc(1.5em + .75rem))}.form-check-input.is-invalid,.was-validated .form-check-input:invalid{border-color:var(--bs-form-invalid-border-color)}.form-check-input.is-invalid:checked,.was-validated .form-check-input:invalid:checked{background-color:var(--bs-form-invalid-color)}.form-check-input.is-invalid:focus,.was-validated .form-check-input:invalid:focus{box-shadow:0 0 0 .25rem rgba(var(--bs-danger-rgb),.25)}.form-check-input.is-invalid~.form-check-label,.was-validated .form-check-input:invalid~.form-check-label{color:var(--bs-form-invalid-color)}.form-check-inline .form-check-input~.invalid-feedback{margin-left:.5em}.input-group>.form-control:not(:focus).is-invalid,.input-group>.form-floating:not(:focus-within).is-invalid,.input-group>.form-select:not(:focus).is-invalid,.was-validated .input-group>.form-control:not(:focus):invalid,.was-validated .input-group>.form-floating:not(:focus-within):invalid,.was-validated .input-group>.form-select:not(:focus):invalid{z-index:4}.btn{--bs-btn-padding-x:1rem;--bs-btn-padding-y:0.375rem;--bs-btn-font-family: ;--bs-btn-font-size:1rem;--bs-btn-font-weight:400;--bs-btn-line-height:1.5;--bs-btn-color:var(--bs-body-color);--bs-btn-bg:transparent;--bs-btn-border-width:var(--bs-border-width);--bs-btn-border-color:transparent;--bs-btn-border-radius:var(--bs-border-radius);--bs-btn-hover-border-color:transparent;--bs-btn-box-shadow:inset 0 1px 0 rgba(255, 255, 255, 0.15),0 1px 1px rgba(0, 0, 0, 0.075);--bs-btn-disabled-opacity:0.65;--bs-btn-focus-box-shadow:0 0 0 0.25rem rgba(var(--bs-btn-focus-shadow-rgb), .5);display:inline-block;padding:var(--bs-btn-padding-y) var(--bs-btn-padding-x);font-family:var(--bs-btn-font-family);font-size:var(--bs-btn-font-size);font-weight:var(--bs-btn-font-weight);line-height:var(--bs-btn-line-height);color:var(--bs-btn-color);text-align:center;text-decoration:none;vertical-align:middle;cursor:pointer;-webkit-user-select:none;-moz-user-select:none;user-select:none;border:var(--bs-btn-border-width) solid var(--bs-btn-border-color);border-radius:var(--bs-btn-border-radius);background-color:var(--bs-btn-bg);transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.btn{transition:none}}.btn:hover{color:var(--bs-btn-hover-color);background-color:var(--bs-btn-hover-bg);border-color:var(--bs-btn-hover-border-color)}.btn-check+.btn:hover{color:var(--bs-btn-color);background-color:var(--bs-btn-bg);border-color:var(--bs-btn-border-color)}.btn:focus-visible{color:var(--bs-btn-hover-color);background-color:var(--bs-btn-hover-bg);border-color:var(--bs-btn-hover-border-color);outline:0;box-shadow:var(--bs-btn-focus-box-shadow)}.btn-check:focus-visible+.btn{border-color:var(--bs-btn-hover-border-color);outline:0;box-shadow:var(--bs-btn-focus-box-shadow)}.btn-check:checked+.btn,.btn.active,.btn.show,.btn:first-child:active,:not(.btn-check)+.btn:active{color:var(--bs-btn-active-color);background-color:var(--bs-btn-active-bg);border-color:var(--bs-btn-active-border-color)}.btn-check:checked+.btn:focus-visible,.btn.active:focus-visible,.btn.show:focus-visible,.btn:first-child:active:focus-visible,:not(.btn-check)+.btn:active:focus-visible{box-shadow:var(--bs-btn-focus-box-shadow)}.btn-check:checked:focus-visible+.btn{box-shadow:var(--bs-btn-focus-box-shadow)}.btn.disabled,.btn:disabled,fieldset:disabled .btn{color:var(--bs-btn-disabled-color);pointer-events:none;background-color:var(--bs-btn-disabled-bg);border-color:var(--bs-btn-disabled-border-color);opacity:var(--bs-btn-disabled-opacity)}.btn-primary{--bs-btn-color:#fff;--bs-btn-bg:#eb6864;--bs-btn-border-color:#eb6864;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#c85855;--bs-btn-hover-border-color:#bc5350;--bs-btn-focus-shadow-rgb:238,127,123;--bs-btn-active-color:#fff;--bs-btn-active-bg:#bc5350;--bs-btn-active-border-color:#b04e4b;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#eb6864;--bs-btn-disabled-border-color:#eb6864}.btn-secondary{--bs-btn-color:#fff;--bs-btn-bg:#aaa;--bs-btn-border-color:#aaa;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#919191;--bs-btn-hover-border-color:#888888;--bs-btn-focus-shadow-rgb:183,183,183;--bs-btn-active-color:#fff;--bs-btn-active-bg:#888888;--bs-btn-active-border-color:gray;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#aaa;--bs-btn-disabled-border-color:#aaa}.btn-success{--bs-btn-color:#fff;--bs-btn-bg:#22b24c;--bs-btn-border-color:#22b24c;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#1d9741;--bs-btn-hover-border-color:#1b8e3d;--bs-btn-focus-shadow-rgb:67,190,103;--bs-btn-active-color:#fff;--bs-btn-active-bg:#1b8e3d;--bs-btn-active-border-color:#1a8639;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#22b24c;--bs-btn-disabled-border-color:#22b24c}.btn-info{--bs-btn-color:#fff;--bs-btn-bg:#369;--bs-btn-border-color:#369;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#2b5782;--bs-btn-hover-border-color:#29527a;--bs-btn-focus-shadow-rgb:82,125,168;--bs-btn-active-color:#fff;--bs-btn-active-bg:#29527a;--bs-btn-active-border-color:#264d73;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#369;--bs-btn-disabled-border-color:#369}.btn-warning{--bs-btn-color:#fff;--bs-btn-bg:#f5e625;--bs-btn-border-color:#f5e625;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#d0c41f;--bs-btn-hover-border-color:#c4b81e;--bs-btn-focus-shadow-rgb:247,234,70;--bs-btn-active-color:#fff;--bs-btn-active-bg:#c4b81e;--bs-btn-active-border-color:#b8ad1c;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#f5e625;--bs-btn-disabled-border-color:#f5e625}.btn-danger{--bs-btn-color:#fff;--bs-btn-bg:#f57a00;--bs-btn-border-color:#f57a00;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#d06800;--bs-btn-hover-border-color:#c46200;--bs-btn-focus-shadow-rgb:247,142,38;--bs-btn-active-color:#fff;--bs-btn-active-bg:#c46200;--bs-btn-active-border-color:#b85c00;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#f57a00;--bs-btn-disabled-border-color:#f57a00}.btn-light{--bs-btn-color:#000;--bs-btn-bg:#f8f9fa;--bs-btn-border-color:#f8f9fa;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#d3d4d5;--bs-btn-hover-border-color:#c6c7c8;--bs-btn-focus-shadow-rgb:211,212,213;--bs-btn-active-color:#fff;--bs-btn-active-bg:#c6c7c8;--bs-btn-active-border-color:#babbbc;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#000;--bs-btn-disabled-bg:#f8f9fa;--bs-btn-disabled-border-color:#f8f9fa}.btn-dark{--bs-btn-color:#fff;--bs-btn-bg:#222;--bs-btn-border-color:#222;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#434343;--bs-btn-hover-border-color:#383838;--bs-btn-focus-shadow-rgb:67,67,67;--bs-btn-active-color:#fff;--bs-btn-active-bg:#4e4e4e;--bs-btn-active-border-color:#383838;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#fff;--bs-btn-disabled-bg:#222;--bs-btn-disabled-border-color:#222}.btn-outline-primary{--bs-btn-color:#eb6864;--bs-btn-border-color:#eb6864;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#eb6864;--bs-btn-hover-border-color:#eb6864;--bs-btn-focus-shadow-rgb:235,104,100;--bs-btn-active-color:#fff;--bs-btn-active-bg:#eb6864;--bs-btn-active-border-color:#eb6864;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#eb6864;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#eb6864;--bs-gradient:none}.btn-outline-secondary{--bs-btn-color:#aaa;--bs-btn-border-color:#aaa;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#aaa;--bs-btn-hover-border-color:#aaa;--bs-btn-focus-shadow-rgb:170,170,170;--bs-btn-active-color:#fff;--bs-btn-active-bg:#aaa;--bs-btn-active-border-color:#aaa;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#aaa;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#aaa;--bs-gradient:none}.btn-outline-success{--bs-btn-color:#22b24c;--bs-btn-border-color:#22b24c;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#22b24c;--bs-btn-hover-border-color:#22b24c;--bs-btn-focus-shadow-rgb:34,178,76;--bs-btn-active-color:#fff;--bs-btn-active-bg:#22b24c;--bs-btn-active-border-color:#22b24c;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#22b24c;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#22b24c;--bs-gradient:none}.btn-outline-info{--bs-btn-color:#369;--bs-btn-border-color:#369;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#369;--bs-btn-hover-border-color:#369;--bs-btn-focus-shadow-rgb:51,102,153;--bs-btn-active-color:#fff;--bs-btn-active-bg:#369;--bs-btn-active-border-color:#369;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#369;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#369;--bs-gradient:none}.btn-outline-warning{--bs-btn-color:#f5e625;--bs-btn-border-color:#f5e625;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#f5e625;--bs-btn-hover-border-color:#f5e625;--bs-btn-focus-shadow-rgb:245,230,37;--bs-btn-active-color:#fff;--bs-btn-active-bg:#f5e625;--bs-btn-active-border-color:#f5e625;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#f5e625;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#f5e625;--bs-gradient:none}.btn-outline-danger{--bs-btn-color:#f57a00;--bs-btn-border-color:#f57a00;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#f57a00;--bs-btn-hover-border-color:#f57a00;--bs-btn-focus-shadow-rgb:245,122,0;--bs-btn-active-color:#fff;--bs-btn-active-bg:#f57a00;--bs-btn-active-border-color:#f57a00;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#f57a00;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#f57a00;--bs-gradient:none}.btn-outline-light{--bs-btn-color:#f8f9fa;--bs-btn-border-color:#f8f9fa;--bs-btn-hover-color:#000;--bs-btn-hover-bg:#f8f9fa;--bs-btn-hover-border-color:#f8f9fa;--bs-btn-focus-shadow-rgb:248,249,250;--bs-btn-active-color:#000;--bs-btn-active-bg:#f8f9fa;--bs-btn-active-border-color:#f8f9fa;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#f8f9fa;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#f8f9fa;--bs-gradient:none}.btn-outline-dark{--bs-btn-color:#222;--bs-btn-border-color:#222;--bs-btn-hover-color:#fff;--bs-btn-hover-bg:#222;--bs-btn-hover-border-color:#222;--bs-btn-focus-shadow-rgb:34,34,34;--bs-btn-active-color:#fff;--bs-btn-active-bg:#222;--bs-btn-active-border-color:#222;--bs-btn-active-shadow:inset 0 3px 5px rgba(0, 0, 0, 0.125);--bs-btn-disabled-color:#222;--bs-btn-disabled-bg:transparent;--bs-btn-disabled-border-color:#222;--bs-gradient:none}.btn-link{--bs-btn-font-weight:400;--bs-btn-color:var(--bs-link-color);--bs-btn-bg:transparent;--bs-btn-border-color:transparent;--bs-btn-hover-color:var(--bs-link-hover-color);--bs-btn-hover-border-color:transparent;--bs-btn-active-color:var(--bs-link-hover-color);--bs-btn-active-border-color:transparent;--bs-btn-disabled-color:#777;--bs-btn-disabled-border-color:transparent;--bs-btn-box-shadow:0 0 0 #000;--bs-btn-focus-shadow-rgb:238,127,123;text-decoration:underline}.btn-link:focus-visible{color:var(--bs-btn-color)}.btn-link:hover{color:var(--bs-btn-hover-color)}.btn-group-lg>.btn,.btn-lg{--bs-btn-padding-y:0.5rem;--bs-btn-padding-x:1rem;--bs-btn-font-size:1.25rem;--bs-btn-border-radius:var(--bs-border-radius-lg)}.btn-group-sm>.btn,.btn-sm{--bs-btn-padding-y:0.25rem;--bs-btn-padding-x:0.5rem;--bs-btn-font-size:0.875rem;--bs-btn-border-radius:var(--bs-border-radius-sm)}.fade{transition:opacity .15s linear}@media (prefers-reduced-motion:reduce){.fade{transition:none}}.fade:not(.show){opacity:0}.collapse:not(.show){display:none}.collapsing{height:0;overflow:hidden;transition:height .35s ease}@media (prefers-reduced-motion:reduce){.collapsing{transition:none}}.collapsing.collapse-horizontal{width:0;height:auto;transition:width .35s ease}@media (prefers-reduced-motion:reduce){.collapsing.collapse-horizontal{transition:none}}.dropdown,.dropdown-center,.dropend,.dropstart,.dropup,.dropup-center{position:relative}.dropdown-toggle{white-space:nowrap}.dropdown-toggle::after{display:inline-block;margin-left:.255em;vertical-align:.255em;content:"";border-top:.3em solid;border-right:.3em solid transparent;border-bottom:0;border-left:.3em solid transparent}.dropdown-toggle:empty::after{margin-left:0}.dropdown-menu{--bs-dropdown-zindex:1000;--bs-dropdown-min-width:10rem;--bs-dropdown-padding-x:0;--bs-dropdown-padding-y:0.5rem;--bs-dropdown-spacer:0.125rem;--bs-dropdown-font-size:1rem;--bs-dropdown-color:var(--bs-body-color);--bs-dropdown-bg:var(--bs-body-bg);--bs-dropdown-border-color:var(--bs-border-color-translucent);--bs-dropdown-border-radius:var(--bs-border-radius);--bs-dropdown-border-width:var(--bs-border-width);--bs-dropdown-inner-border-radius:calc(var(--bs-border-radius) - var(--bs-border-width));--bs-dropdown-divider-bg:var(--bs-border-color-translucent);--bs-dropdown-divider-margin-y:0.5rem;--bs-dropdown-box-shadow:var(--bs-box-shadow);--bs-dropdown-link-color:var(--bs-body-color);--bs-dropdown-link-hover-color:var(--bs-body-color);--bs-dropdown-link-hover-bg:var(--bs-tertiary-bg);--bs-dropdown-link-active-color:#fff;--bs-dropdown-link-active-bg:#eb6864;--bs-dropdown-link-disabled-color:var(--bs-tertiary-color);--bs-dropdown-item-padding-x:1rem;--bs-dropdown-item-padding-y:0.25rem;--bs-dropdown-header-color:#777;--bs-dropdown-header-padding-x:1rem;--bs-dropdown-header-padding-y:0.5rem;position:absolute;z-index:var(--bs-dropdown-zindex);display:none;min-width:var(--bs-dropdown-min-width);padding:var(--bs-dropdown-padding-y) var(--bs-dropdown-padding-x);margin:0;font-size:var(--bs-dropdown-font-size);color:var(--bs-dropdown-color);text-align:left;list-style:none;background-color:var(--bs-dropdown-bg);background-clip:padding-box;border:var(--bs-dropdown-border-width) solid var(--bs-dropdown-border-color);border-radius:var(--bs-dropdown-border-radius)}.dropdown-menu[data-bs-popper]{top:100%;left:0;margin-top:var(--bs-dropdown-spacer)}.dropdown-menu-start{--bs-position:start}.dropdown-menu-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-end{--bs-position:end}.dropdown-menu-end[data-bs-popper]{right:0;left:auto}@media (min-width:576px){.dropdown-menu-sm-start{--bs-position:start}.dropdown-menu-sm-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-sm-end{--bs-position:end}.dropdown-menu-sm-end[data-bs-popper]{right:0;left:auto}}@media (min-width:768px){.dropdown-menu-md-start{--bs-position:start}.dropdown-menu-md-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-md-end{--bs-position:end}.dropdown-menu-md-end[data-bs-popper]{right:0;left:auto}}@media (min-width:992px){.dropdown-menu-lg-start{--bs-position:start}.dropdown-menu-lg-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-lg-end{--bs-position:end}.dropdown-menu-lg-end[data-bs-popper]{right:0;left:auto}}@media (min-width:1200px){.dropdown-menu-xl-start{--bs-position:start}.dropdown-menu-xl-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-xl-end{--bs-position:end}.dropdown-menu-xl-end[data-bs-popper]{right:0;left:auto}}@media (min-width:1400px){.dropdown-menu-xxl-start{--bs-position:start}.dropdown-menu-xxl-start[data-bs-popper]{right:auto;left:0}.dropdown-menu-xxl-end{--bs-position:end}.dropdown-menu-xxl-end[data-bs-popper]{right:0;left:auto}}.dropup .dropdown-menu[data-bs-popper]{top:auto;bottom:100%;margin-top:0;margin-bottom:var(--bs-dropdown-spacer)}.dropup .dropdown-toggle::after{display:inline-block;margin-left:.255em;vertical-align:.255em;content:"";border-top:0;border-right:.3em solid transparent;border-bottom:.3em solid;border-left:.3em solid transparent}.dropup .dropdown-toggle:empty::after{margin-left:0}.dropend .dropdown-menu[data-bs-popper]{top:0;right:auto;left:100%;margin-top:0;margin-left:var(--bs-dropdown-spacer)}.dropend .dropdown-toggle::after{display:inline-block;margin-left:.255em;vertical-align:.255em;content:"";border-top:.3em solid transparent;border-right:0;border-bottom:.3em solid transparent;border-left:.3em solid}.dropend .dropdown-toggle:empty::after{margin-left:0}.dropend .dropdown-toggle::after{vertical-align:0}.dropstart .dropdown-menu[data-bs-popper]{top:0;right:100%;left:auto;margin-top:0;margin-right:var(--bs-dropdown-spacer)}.dropstart .dropdown-toggle::after{display:inline-block;margin-left:.255em;vertical-align:.255em;content:""}.dropstart .dropdown-toggle::after{display:none}.dropstart .dropdown-toggle::before{display:inline-block;margin-right:.255em;vertical-align:.255em;content:"";border-top:.3em solid transparent;border-right:.3em solid;border-bottom:.3em solid transparent}.dropstart .dropdown-toggle:empty::after{margin-left:0}.dropstart .dropdown-toggle::before{vertical-align:0}.dropdown-divider{height:0;margin:var(--bs-dropdown-divider-margin-y) 0;overflow:hidden;border-top:1px solid var(--bs-dropdown-divider-bg);opacity:1}.dropdown-item{display:block;width:100%;padding:var(--bs-dropdown-item-padding-y) var(--bs-dropdown-item-padding-x);clear:both;font-weight:400;color:var(--bs-dropdown-link-color);text-align:inherit;text-decoration:none;white-space:nowrap;background-color:transparent;border:0;border-radius:var(--bs-dropdown-item-border-radius,0)}.dropdown-item:focus,.dropdown-item:hover{color:var(--bs-dropdown-link-hover-color);background-color:var(--bs-dropdown-link-hover-bg)}.dropdown-item.active,.dropdown-item:active{color:var(--bs-dropdown-link-active-color);text-decoration:none;background-color:var(--bs-dropdown-link-active-bg)}.dropdown-item.disabled,.dropdown-item:disabled{color:var(--bs-dropdown-link-disabled-color);pointer-events:none;background-color:transparent}.dropdown-menu.show{display:block}.dropdown-header{display:block;padding:var(--bs-dropdown-header-padding-y) var(--bs-dropdown-header-padding-x);margin-bottom:0;font-size:.875rem;color:var(--bs-dropdown-header-color);white-space:nowrap}.dropdown-item-text{display:block;padding:var(--bs-dropdown-item-padding-y) var(--bs-dropdown-item-padding-x);color:var(--bs-dropdown-link-color)}.dropdown-menu-dark{--bs-dropdown-color:#dee2e6;--bs-dropdown-bg:#333;--bs-dropdown-border-color:var(--bs-border-color-translucent);--bs-dropdown-box-shadow: ;--bs-dropdown-link-color:#dee2e6;--bs-dropdown-link-hover-color:#fff;--bs-dropdown-divider-bg:var(--bs-border-color-translucent);--bs-dropdown-link-hover-bg:rgba(255, 255, 255, 0.15);--bs-dropdown-link-active-color:#fff;--bs-dropdown-link-active-bg:#eb6864;--bs-dropdown-link-disabled-color:#aaa;--bs-dropdown-header-color:#aaa}.btn-group,.btn-group-vertical{position:relative;display:inline-flex;vertical-align:middle}.btn-group-vertical>.btn,.btn-group>.btn{position:relative;flex:1 1 auto}.btn-group-vertical>.btn-check:checked+.btn,.btn-group-vertical>.btn-check:focus+.btn,.btn-group-vertical>.btn.active,.btn-group-vertical>.btn:active,.btn-group-vertical>.btn:focus,.btn-group-vertical>.btn:hover,.btn-group>.btn-check:checked+.btn,.btn-group>.btn-check:focus+.btn,.btn-group>.btn.active,.btn-group>.btn:active,.btn-group>.btn:focus,.btn-group>.btn:hover{z-index:1}.btn-toolbar{display:flex;flex-wrap:wrap;justify-content:flex-start}.btn-toolbar .input-group{width:auto}.btn-group{border-radius:var(--bs-border-radius)}.btn-group>.btn-group:not(:first-child),.btn-group>:not(.btn-check:first-child)+.btn{margin-left:calc(-1 * var(--bs-border-width))}.btn-group>.btn-group:not(:last-child)>.btn,.btn-group>.btn.dropdown-toggle-split:first-child,.btn-group>.btn:not(:last-child):not(.dropdown-toggle){border-top-right-radius:0;border-bottom-right-radius:0}.btn-group>.btn-group:not(:first-child)>.btn,.btn-group>.btn:nth-child(n+3),.btn-group>:not(.btn-check)+.btn{border-top-left-radius:0;border-bottom-left-radius:0}.dropdown-toggle-split{padding-right:.75rem;padding-left:.75rem}.dropdown-toggle-split::after,.dropend .dropdown-toggle-split::after,.dropup .dropdown-toggle-split::after{margin-left:0}.dropstart .dropdown-toggle-split::before{margin-right:0}.btn-group-sm>.btn+.dropdown-toggle-split,.btn-sm+.dropdown-toggle-split{padding-right:.375rem;padding-left:.375rem}.btn-group-lg>.btn+.dropdown-toggle-split,.btn-lg+.dropdown-toggle-split{padding-right:.75rem;padding-left:.75rem}.btn-group-vertical{flex-direction:column;align-items:flex-start;justify-content:center}.btn-group-vertical>.btn,.btn-group-vertical>.btn-group{width:100%}.btn-group-vertical>.btn-group:not(:first-child),.btn-group-vertical>.btn:not(:first-child){margin-top:calc(-1 * var(--bs-border-width))}.btn-group-vertical>.btn-group:not(:last-child)>.btn,.btn-group-vertical>.btn:not(:last-child):not(.dropdown-toggle){border-bottom-right-radius:0;border-bottom-left-radius:0}.btn-group-vertical>.btn-group:not(:first-child)>.btn,.btn-group-vertical>.btn:nth-child(n+3),.btn-group-vertical>:not(.btn-check)+.btn{border-top-left-radius:0;border-top-right-radius:0}.nav{--bs-nav-link-padding-x:1rem;--bs-nav-link-padding-y:0.5rem;--bs-nav-link-font-weight: ;--bs-nav-link-color:var(--bs-link-color);--bs-nav-link-hover-color:var(--bs-link-hover-color);--bs-nav-link-disabled-color:var(--bs-secondary-color);display:flex;flex-wrap:wrap;padding-left:0;margin-bottom:0;list-style:none}.nav-link{display:block;padding:var(--bs-nav-link-padding-y) var(--bs-nav-link-padding-x);font-size:var(--bs-nav-link-font-size);font-weight:var(--bs-nav-link-font-weight);color:var(--bs-nav-link-color);text-decoration:none;background:0 0;border:0;transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out}@media (prefers-reduced-motion:reduce){.nav-link{transition:none}}.nav-link:focus,.nav-link:hover{color:var(--bs-nav-link-hover-color)}.nav-link:focus-visible{outline:0;box-shadow:0 0 0 .25rem rgba(235,104,100,.25)}.nav-link.disabled,.nav-link:disabled{color:var(--bs-nav-link-disabled-color);pointer-events:none;cursor:default}.nav-tabs{--bs-nav-tabs-border-width:var(--bs-border-width);--bs-nav-tabs-border-color:var(--bs-border-color);--bs-nav-tabs-border-radius:var(--bs-border-radius);--bs-nav-tabs-link-hover-border-color:var(--bs-secondary-bg) var(--bs-secondary-bg) var(--bs-border-color);--bs-nav-tabs-link-active-color:var(--bs-emphasis-color);--bs-nav-tabs-link-active-bg:var(--bs-body-bg);--bs-nav-tabs-link-active-border-color:var(--bs-border-color) var(--bs-border-color) var(--bs-body-bg);border-bottom:var(--bs-nav-tabs-border-width) solid var(--bs-nav-tabs-border-color)}.nav-tabs .nav-link{margin-bottom:calc(-1 * var(--bs-nav-tabs-border-width));border:var(--bs-nav-tabs-border-width) solid transparent;border-top-left-radius:var(--bs-nav-tabs-border-radius);border-top-right-radius:var(--bs-nav-tabs-border-radius)}.nav-tabs .nav-link:focus,.nav-tabs .nav-link:hover{isolation:isolate;border-color:var(--bs-nav-tabs-link-hover-border-color)}.nav-tabs .nav-item.show .nav-link,.nav-tabs .nav-link.active{color:var(--bs-nav-tabs-link-active-color);background-color:var(--bs-nav-tabs-link-active-bg);border-color:var(--bs-nav-tabs-link-active-border-color)}.nav-tabs .dropdown-menu{margin-top:calc(-1 * var(--bs-nav-tabs-border-width));border-top-left-radius:0;border-top-right-radius:0}.nav-pills{--bs-nav-pills-border-radius:var(--bs-border-radius);--bs-nav-pills-link-active-color:#fff;--bs-nav-pills-link-active-bg:#eb6864}.nav-pills .nav-link{border-radius:var(--bs-nav-pills-border-radius)}.nav-pills .nav-link.active,.nav-pills .show>.nav-link{color:var(--bs-nav-pills-link-active-color);background-color:var(--bs-nav-pills-link-active-bg)}.nav-underline{--bs-nav-underline-gap:1rem;--bs-nav-underline-border-width:0.125rem;--bs-nav-underline-link-active-color:var(--bs-emphasis-color);gap:var(--bs-nav-underline-gap)}.nav-underline .nav-link{padding-right:0;padding-left:0;border-bottom:var(--bs-nav-underline-border-width) solid transparent}.nav-underline .nav-link:focus,.nav-underline .nav-link:hover{border-bottom-color:currentcolor}.nav-underline .nav-link.active,.nav-underline .show>.nav-link{font-weight:700;color:var(--bs-nav-underline-link-active-color);border-bottom-color:currentcolor}.nav-fill .nav-item,.nav-fill>.nav-link{flex:1 1 auto;text-align:center}.nav-justified .nav-item,.nav-justified>.nav-link{flex-grow:1;flex-basis:0;text-align:center}.nav-fill .nav-item .nav-link,.nav-justified .nav-item .nav-link{width:100%}.tab-content>.tab-pane{display:none}.tab-content>.active{display:block}.navbar{--bs-navbar-padding-x:0;--bs-navbar-padding-y:0.5rem;--bs-navbar-color:rgba(var(--bs-emphasis-color-rgb), 0.65);--bs-navbar-hover-color:rgba(var(--bs-emphasis-color-rgb), 0.8);--bs-navbar-disabled-color:rgba(var(--bs-emphasis-color-rgb), 0.3);--bs-navbar-active-color:rgba(var(--bs-emphasis-color-rgb), 1);--bs-navbar-brand-padding-y:0.3125rem;--bs-navbar-brand-margin-end:1rem;--bs-navbar-brand-font-size:1.25rem;--bs-navbar-brand-color:rgba(var(--bs-emphasis-color-rgb), 1);--bs-navbar-brand-hover-color:rgba(var(--bs-emphasis-color-rgb), 1);--bs-navbar-nav-link-padding-x:0.5rem;--bs-navbar-toggler-padding-y:0.25rem;--bs-navbar-toggler-padding-x:0.75rem;--bs-navbar-toggler-font-size:1.25rem;--bs-navbar-toggler-icon-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%2834, 34, 34, 0.75%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");--bs-navbar-toggler-border-color:rgba(var(--bs-emphasis-color-rgb), 0.15);--bs-navbar-toggler-border-radius:var(--bs-border-radius);--bs-navbar-toggler-focus-width:0.25rem;--bs-navbar-toggler-transition:box-shadow 0.15s ease-in-out;position:relative;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;padding:var(--bs-navbar-padding-y) var(--bs-navbar-padding-x)}.navbar>.container,.navbar>.container-fluid,.navbar>.container-lg,.navbar>.container-md,.navbar>.container-sm,.navbar>.container-xl,.navbar>.container-xxl{display:flex;flex-wrap:inherit;align-items:center;justify-content:space-between}.navbar-brand{padding-top:var(--bs-navbar-brand-padding-y);padding-bottom:var(--bs-navbar-brand-padding-y);margin-right:var(--bs-navbar-brand-margin-end);font-size:var(--bs-navbar-brand-font-size);color:var(--bs-navbar-brand-color);text-decoration:none;white-space:nowrap}.navbar-brand:focus,.navbar-brand:hover{color:var(--bs-navbar-brand-hover-color)}.navbar-nav{--bs-nav-link-padding-x:0;--bs-nav-link-padding-y:0.5rem;--bs-nav-link-font-weight: ;--bs-nav-link-color:var(--bs-navbar-color);--bs-nav-link-hover-color:var(--bs-navbar-hover-color);--bs-nav-link-disabled-color:var(--bs-navbar-disabled-color);display:flex;flex-direction:column;padding-left:0;margin-bottom:0;list-style:none}.navbar-nav .nav-link.active,.navbar-nav .nav-link.show{color:var(--bs-navbar-active-color)}.navbar-nav .dropdown-menu{position:static}.navbar-text{padding-top:.5rem;padding-bottom:.5rem;color:var(--bs-navbar-color)}.navbar-text a,.navbar-text a:focus,.navbar-text a:hover{color:var(--bs-navbar-active-color)}.navbar-collapse{flex-grow:1;flex-basis:100%;align-items:center}.navbar-toggler{padding:var(--bs-navbar-toggler-padding-y) var(--bs-navbar-toggler-padding-x);font-size:var(--bs-navbar-toggler-font-size);line-height:1;color:var(--bs-navbar-color);background-color:transparent;border:var(--bs-border-width) solid var(--bs-navbar-toggler-border-color);border-radius:var(--bs-navbar-toggler-border-radius);transition:var(--bs-navbar-toggler-transition)}@media (prefers-reduced-motion:reduce){.navbar-toggler{transition:none}}.navbar-toggler:hover{text-decoration:none}.navbar-toggler:focus{text-decoration:none;outline:0;box-shadow:0 0 0 var(--bs-navbar-toggler-focus-width)}.navbar-toggler-icon{display:inline-block;width:1.5em;height:1.5em;vertical-align:middle;background-image:var(--bs-navbar-toggler-icon-bg);background-repeat:no-repeat;background-position:center;background-size:100%}.navbar-nav-scroll{max-height:var(--bs-scroll-height,75vh);overflow-y:auto}@media (min-width:576px){.navbar-expand-sm{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand-sm .navbar-nav{flex-direction:row}.navbar-expand-sm .navbar-nav .dropdown-menu{position:absolute}.navbar-expand-sm .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand-sm .navbar-nav-scroll{overflow:visible}.navbar-expand-sm .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand-sm .navbar-toggler{display:none}.navbar-expand-sm .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand-sm .offcanvas .offcanvas-header{display:none}.navbar-expand-sm .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}}@media (min-width:768px){.navbar-expand-md{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand-md .navbar-nav{flex-direction:row}.navbar-expand-md .navbar-nav .dropdown-menu{position:absolute}.navbar-expand-md .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand-md .navbar-nav-scroll{overflow:visible}.navbar-expand-md .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand-md .navbar-toggler{display:none}.navbar-expand-md .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand-md .offcanvas .offcanvas-header{display:none}.navbar-expand-md .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}}@media (min-width:992px){.navbar-expand-lg{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand-lg .navbar-nav{flex-direction:row}.navbar-expand-lg .navbar-nav .dropdown-menu{position:absolute}.navbar-expand-lg .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand-lg .navbar-nav-scroll{overflow:visible}.navbar-expand-lg .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand-lg .navbar-toggler{display:none}.navbar-expand-lg .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand-lg .offcanvas .offcanvas-header{display:none}.navbar-expand-lg .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}}@media (min-width:1200px){.navbar-expand-xl{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand-xl .navbar-nav{flex-direction:row}.navbar-expand-xl .navbar-nav .dropdown-menu{position:absolute}.navbar-expand-xl .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand-xl .navbar-nav-scroll{overflow:visible}.navbar-expand-xl .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand-xl .navbar-toggler{display:none}.navbar-expand-xl .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand-xl .offcanvas .offcanvas-header{display:none}.navbar-expand-xl .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}}@media (min-width:1400px){.navbar-expand-xxl{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand-xxl .navbar-nav{flex-direction:row}.navbar-expand-xxl .navbar-nav .dropdown-menu{position:absolute}.navbar-expand-xxl .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand-xxl .navbar-nav-scroll{overflow:visible}.navbar-expand-xxl .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand-xxl .navbar-toggler{display:none}.navbar-expand-xxl .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand-xxl .offcanvas .offcanvas-header{display:none}.navbar-expand-xxl .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}}.navbar-expand{flex-wrap:nowrap;justify-content:flex-start}.navbar-expand .navbar-nav{flex-direction:row}.navbar-expand .navbar-nav .dropdown-menu{position:absolute}.navbar-expand .navbar-nav .nav-link{padding-right:var(--bs-navbar-nav-link-padding-x);padding-left:var(--bs-navbar-nav-link-padding-x)}.navbar-expand .navbar-nav-scroll{overflow:visible}.navbar-expand .navbar-collapse{display:flex!important;flex-basis:auto}.navbar-expand .navbar-toggler{display:none}.navbar-expand .offcanvas{position:static;z-index:auto;flex-grow:1;width:auto!important;height:auto!important;visibility:visible!important;background-color:transparent!important;border:0!important;transform:none!important;transition:none}.navbar-expand .offcanvas .offcanvas-header{display:none}.navbar-expand .offcanvas .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible}.navbar-dark,.navbar[data-bs-theme=dark]{--bs-navbar-color:rgba(255, 255, 255, 0.55);--bs-navbar-hover-color:rgba(255, 255, 255, 0.75);--bs-navbar-disabled-color:rgba(255, 255, 255, 0.25);--bs-navbar-active-color:#fff;--bs-navbar-brand-color:#fff;--bs-navbar-brand-hover-color:#fff;--bs-navbar-toggler-border-color:rgba(255, 255, 255, 0.1);--bs-navbar-toggler-icon-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.55%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e")}[data-bs-theme=dark] .navbar-toggler-icon{--bs-navbar-toggler-icon-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.55%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e")}.card{--bs-card-spacer-y:1rem;--bs-card-spacer-x:1rem;--bs-card-title-spacer-y:0.5rem;--bs-card-title-color: ;--bs-card-subtitle-color: ;--bs-card-border-width:var(--bs-border-width);--bs-card-border-color:var(--bs-border-color-translucent);--bs-card-border-radius:var(--bs-border-radius);--bs-card-box-shadow: ;--bs-card-inner-border-radius:calc(var(--bs-border-radius) - (var(--bs-border-width)));--bs-card-cap-padding-y:0.5rem;--bs-card-cap-padding-x:1rem;--bs-card-cap-bg:rgba(var(--bs-body-color-rgb), 0.03);--bs-card-cap-color: ;--bs-card-height: ;--bs-card-color: ;--bs-card-bg:var(--bs-body-bg);--bs-card-img-overlay-padding:1rem;--bs-card-group-margin:0.75rem;position:relative;display:flex;flex-direction:column;min-width:0;height:var(--bs-card-height);color:var(--bs-body-color);word-wrap:break-word;background-color:var(--bs-card-bg);background-clip:border-box;border:var(--bs-card-border-width) solid var(--bs-card-border-color);border-radius:var(--bs-card-border-radius)}.card>hr{margin-right:0;margin-left:0}.card>.list-group{border-top:inherit;border-bottom:inherit}.card>.list-group:first-child{border-top-width:0;border-top-left-radius:var(--bs-card-inner-border-radius);border-top-right-radius:var(--bs-card-inner-border-radius)}.card>.list-group:last-child{border-bottom-width:0;border-bottom-right-radius:var(--bs-card-inner-border-radius);border-bottom-left-radius:var(--bs-card-inner-border-radius)}.card>.card-header+.list-group,.card>.list-group+.card-footer{border-top:0}.card-body{flex:1 1 auto;padding:var(--bs-card-spacer-y) var(--bs-card-spacer-x);color:var(--bs-card-color)}.card-title{margin-bottom:var(--bs-card-title-spacer-y);color:var(--bs-card-title-color)}.card-subtitle{margin-top:calc(-.5 * var(--bs-card-title-spacer-y));margin-bottom:0;color:var(--bs-card-subtitle-color)}.card-text:last-child{margin-bottom:0}.card-link+.card-link{margin-left:var(--bs-card-spacer-x)}.card-header{padding:var(--bs-card-cap-padding-y) var(--bs-card-cap-padding-x);margin-bottom:0;color:var(--bs-card-cap-color);background-color:var(--bs-card-cap-bg);border-bottom:var(--bs-card-border-width) solid var(--bs-card-border-color)}.card-header:first-child{border-radius:var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius) 0 0}.card-footer{padding:var(--bs-card-cap-padding-y) var(--bs-card-cap-padding-x);color:var(--bs-card-cap-color);background-color:var(--bs-card-cap-bg);border-top:var(--bs-card-border-width) solid var(--bs-card-border-color)}.card-footer:last-child{border-radius:0 0 var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius)}.card-header-tabs{margin-right:calc(-.5 * var(--bs-card-cap-padding-x));margin-bottom:calc(-1 * var(--bs-card-cap-padding-y));margin-left:calc(-.5 * var(--bs-card-cap-padding-x));border-bottom:0}.card-header-tabs .nav-link.active{background-color:var(--bs-card-bg);border-bottom-color:var(--bs-card-bg)}.card-header-pills{margin-right:calc(-.5 * var(--bs-card-cap-padding-x));margin-left:calc(-.5 * var(--bs-card-cap-padding-x))}.card-img-overlay{position:absolute;top:0;right:0;bottom:0;left:0;padding:var(--bs-card-img-overlay-padding);border-radius:var(--bs-card-inner-border-radius)}.card-img,.card-img-bottom,.card-img-top{width:100%}.card-img,.card-img-top{border-top-left-radius:var(--bs-card-inner-border-radius);border-top-right-radius:var(--bs-card-inner-border-radius)}.card-img,.card-img-bottom{border-bottom-right-radius:var(--bs-card-inner-border-radius);border-bottom-left-radius:var(--bs-card-inner-border-radius)}.card-group>.card{margin-bottom:var(--bs-card-group-margin)}@media (min-width:576px){.card-group{display:flex;flex-flow:row wrap}.card-group>.card{flex:1 0 0;margin-bottom:0}.card-group>.card+.card{margin-left:0;border-left:0}.card-group>.card:not(:last-child){border-top-right-radius:0;border-bottom-right-radius:0}.card-group>.card:not(:last-child) .card-header,.card-group>.card:not(:last-child) .card-img-top{border-top-right-radius:0}.card-group>.card:not(:last-child) .card-footer,.card-group>.card:not(:last-child) .card-img-bottom{border-bottom-right-radius:0}.card-group>.card:not(:first-child){border-top-left-radius:0;border-bottom-left-radius:0}.card-group>.card:not(:first-child) .card-header,.card-group>.card:not(:first-child) .card-img-top{border-top-left-radius:0}.card-group>.card:not(:first-child) .card-footer,.card-group>.card:not(:first-child) .card-img-bottom{border-bottom-left-radius:0}}.accordion{--bs-accordion-color:var(--bs-body-color);--bs-accordion-bg:var(--bs-body-bg);--bs-accordion-transition:color 0.15s ease-in-out,background-color 0.15s ease-in-out,border-color 0.15s ease-in-out,box-shadow 0.15s ease-in-out,border-radius 0.15s ease;--bs-accordion-border-color:var(--bs-border-color);--bs-accordion-border-width:var(--bs-border-width);--bs-accordion-border-radius:var(--bs-border-radius);--bs-accordion-inner-border-radius:calc(var(--bs-border-radius) - (var(--bs-border-width)));--bs-accordion-btn-padding-x:1.25rem;--bs-accordion-btn-padding-y:1rem;--bs-accordion-btn-color:var(--bs-body-color);--bs-accordion-btn-bg:var(--bs-accordion-bg);--bs-accordion-btn-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='%23222' stroke-linecap='round' stroke-linejoin='round'%3e%3cpath d='m2 5 6 6 6-6'/%3e%3c/svg%3e");--bs-accordion-btn-icon-width:1.25rem;--bs-accordion-btn-icon-transform:rotate(-180deg);--bs-accordion-btn-icon-transition:transform 0.2s ease-in-out;--bs-accordion-btn-active-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='%235e2a28' stroke-linecap='round' stroke-linejoin='round'%3e%3cpath d='m2 5 6 6 6-6'/%3e%3c/svg%3e");--bs-accordion-btn-focus-box-shadow:0 0 0 0.25rem rgba(235, 104, 100, 0.25);--bs-accordion-body-padding-x:1.25rem;--bs-accordion-body-padding-y:1rem;--bs-accordion-active-color:var(--bs-primary-text-emphasis);--bs-accordion-active-bg:var(--bs-primary-bg-subtle)}.accordion-button{position:relative;display:flex;align-items:center;width:100%;padding:var(--bs-accordion-btn-padding-y) var(--bs-accordion-btn-padding-x);font-size:1rem;color:var(--bs-accordion-btn-color);text-align:left;background-color:var(--bs-accordion-btn-bg);border:0;border-radius:0;overflow-anchor:none;transition:var(--bs-accordion-transition)}@media (prefers-reduced-motion:reduce){.accordion-button{transition:none}}.accordion-button:not(.collapsed){color:var(--bs-accordion-active-color);background-color:var(--bs-accordion-active-bg);box-shadow:inset 0 calc(-1 * var(--bs-accordion-border-width)) 0 var(--bs-accordion-border-color)}.accordion-button:not(.collapsed)::after{background-image:var(--bs-accordion-btn-active-icon);transform:var(--bs-accordion-btn-icon-transform)}.accordion-button::after{flex-shrink:0;width:var(--bs-accordion-btn-icon-width);height:var(--bs-accordion-btn-icon-width);margin-left:auto;content:"";background-image:var(--bs-accordion-btn-icon);background-repeat:no-repeat;background-size:var(--bs-accordion-btn-icon-width);transition:var(--bs-accordion-btn-icon-transition)}@media (prefers-reduced-motion:reduce){.accordion-button::after{transition:none}}.accordion-button:hover{z-index:2}.accordion-button:focus{z-index:3;outline:0;box-shadow:var(--bs-accordion-btn-focus-box-shadow)}.accordion-header{margin-bottom:0}.accordion-item{color:var(--bs-accordion-color);background-color:var(--bs-accordion-bg);border:var(--bs-accordion-border-width) solid var(--bs-accordion-border-color)}.accordion-item:first-of-type{border-top-left-radius:var(--bs-accordion-border-radius);border-top-right-radius:var(--bs-accordion-border-radius)}.accordion-item:first-of-type>.accordion-header .accordion-button{border-top-left-radius:var(--bs-accordion-inner-border-radius);border-top-right-radius:var(--bs-accordion-inner-border-radius)}.accordion-item:not(:first-of-type){border-top:0}.accordion-item:last-of-type{border-bottom-right-radius:var(--bs-accordion-border-radius);border-bottom-left-radius:var(--bs-accordion-border-radius)}.accordion-item:last-of-type>.accordion-header .accordion-button.collapsed{border-bottom-right-radius:var(--bs-accordion-inner-border-radius);border-bottom-left-radius:var(--bs-accordion-inner-border-radius)}.accordion-item:last-of-type>.accordion-collapse{border-bottom-right-radius:var(--bs-accordion-border-radius);border-bottom-left-radius:var(--bs-accordion-border-radius)}.accordion-body{padding:var(--bs-accordion-body-padding-y) var(--bs-accordion-body-padding-x)}.accordion-flush>.accordion-item{border-right:0;border-left:0;border-radius:0}.accordion-flush>.accordion-item:first-child{border-top:0}.accordion-flush>.accordion-item:last-child{border-bottom:0}.accordion-flush>.accordion-item>.accordion-collapse,.accordion-flush>.accordion-item>.accordion-header .accordion-button,.accordion-flush>.accordion-item>.accordion-header .accordion-button.collapsed{border-radius:0}[data-bs-theme=dark] .accordion-button::after{--bs-accordion-btn-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23f3a4a2'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708'/%3e%3c/svg%3e");--bs-accordion-btn-active-icon:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23f3a4a2'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708'/%3e%3c/svg%3e")}.breadcrumb{--bs-breadcrumb-padding-x:0;--bs-breadcrumb-padding-y:0;--bs-breadcrumb-margin-bottom:1rem;--bs-breadcrumb-bg: ;--bs-breadcrumb-border-radius: ;--bs-breadcrumb-divider-color:var(--bs-secondary-color);--bs-breadcrumb-item-padding-x:0.5rem;--bs-breadcrumb-item-active-color:var(--bs-secondary-color);display:flex;flex-wrap:wrap;padding:var(--bs-breadcrumb-padding-y) var(--bs-breadcrumb-padding-x);margin-bottom:var(--bs-breadcrumb-margin-bottom);font-size:var(--bs-breadcrumb-font-size);list-style:none;background-color:var(--bs-breadcrumb-bg);border-radius:var(--bs-breadcrumb-border-radius)}.breadcrumb-item+.breadcrumb-item{padding-left:var(--bs-breadcrumb-item-padding-x)}.breadcrumb-item+.breadcrumb-item::before{float:left;padding-right:var(--bs-breadcrumb-item-padding-x);color:var(--bs-breadcrumb-divider-color);content:var(--bs-breadcrumb-divider, "/")}.breadcrumb-item.active{color:var(--bs-breadcrumb-item-active-color)}.pagination{--bs-pagination-padding-x:0.75rem;--bs-pagination-padding-y:0.375rem;--bs-pagination-font-size:1rem;--bs-pagination-color:var(--bs-link-color);--bs-pagination-bg:var(--bs-body-bg);--bs-pagination-border-width:var(--bs-border-width);--bs-pagination-border-color:var(--bs-border-color);--bs-pagination-border-radius:var(--bs-border-radius);--bs-pagination-hover-color:#fff;--bs-pagination-hover-bg:#eb6864;--bs-pagination-hover-border-color:#eb6864;--bs-pagination-focus-color:var(--bs-link-hover-color);--bs-pagination-focus-bg:var(--bs-secondary-bg);--bs-pagination-focus-box-shadow:0 0 0 0.25rem rgba(235, 104, 100, 0.25);--bs-pagination-active-color:#fff;--bs-pagination-active-bg:#eb6864;--bs-pagination-active-border-color:#eb6864;--bs-pagination-disabled-color:var(--bs-secondary-color);--bs-pagination-disabled-bg:var(--bs-secondary-bg);--bs-pagination-disabled-border-color:var(--bs-border-color);display:flex;padding-left:0;list-style:none}.page-link{position:relative;display:block;padding:var(--bs-pagination-padding-y) var(--bs-pagination-padding-x);font-size:var(--bs-pagination-font-size);color:var(--bs-pagination-color);text-decoration:none;background-color:var(--bs-pagination-bg);border:var(--bs-pagination-border-width) solid var(--bs-pagination-border-color);transition:color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out}@media (prefers-reduced-motion:reduce){.page-link{transition:none}}.page-link:hover{z-index:2;color:var(--bs-pagination-hover-color);background-color:var(--bs-pagination-hover-bg);border-color:var(--bs-pagination-hover-border-color)}.page-link:focus{z-index:3;color:var(--bs-pagination-focus-color);background-color:var(--bs-pagination-focus-bg);outline:0;box-shadow:var(--bs-pagination-focus-box-shadow)}.active>.page-link,.page-link.active{z-index:3;color:var(--bs-pagination-active-color);background-color:var(--bs-pagination-active-bg);border-color:var(--bs-pagination-active-border-color)}.disabled>.page-link,.page-link.disabled{color:var(--bs-pagination-disabled-color);pointer-events:none;background-color:var(--bs-pagination-disabled-bg);border-color:var(--bs-pagination-disabled-border-color)}.page-item:not(:first-child) .page-link{margin-left:calc(-1 * var(--bs-border-width))}.page-item:first-child .page-link{border-top-left-radius:var(--bs-pagination-border-radius);border-bottom-left-radius:var(--bs-pagination-border-radius)}.page-item:last-child .page-link{border-top-right-radius:var(--bs-pagination-border-radius);border-bottom-right-radius:var(--bs-pagination-border-radius)}.pagination-lg{--bs-pagination-padding-x:1.5rem;--bs-pagination-padding-y:0.75rem;--bs-pagination-font-size:1.25rem;--bs-pagination-border-radius:var(--bs-border-radius-lg)}.pagination-sm{--bs-pagination-padding-x:0.5rem;--bs-pagination-padding-y:0.25rem;--bs-pagination-font-size:0.875rem;--bs-pagination-border-radius:var(--bs-border-radius-sm)}.badge{--bs-badge-padding-x:0.65em;--bs-badge-padding-y:0.35em;--bs-badge-font-size:0.75em;--bs-badge-font-weight:700;--bs-badge-color:#fff;--bs-badge-border-radius:var(--bs-border-radius);display:inline-block;padding:var(--bs-badge-padding-y) var(--bs-badge-padding-x);font-size:var(--bs-badge-font-size);font-weight:var(--bs-badge-font-weight);line-height:1;color:var(--bs-badge-color);text-align:center;white-space:nowrap;vertical-align:baseline;border-radius:var(--bs-badge-border-radius)}.badge:empty{display:none}.btn .badge{position:relative;top:-1px}.alert{--bs-alert-bg:transparent;--bs-alert-padding-x:1rem;--bs-alert-padding-y:1rem;--bs-alert-margin-bottom:1rem;--bs-alert-color:inherit;--bs-alert-border-color:transparent;--bs-alert-border:var(--bs-border-width) solid var(--bs-alert-border-color);--bs-alert-border-radius:var(--bs-border-radius);--bs-alert-link-color:inherit;position:relative;padding:var(--bs-alert-padding-y) var(--bs-alert-padding-x);margin-bottom:var(--bs-alert-margin-bottom);color:var(--bs-alert-color);background-color:var(--bs-alert-bg);border:var(--bs-alert-border);border-radius:var(--bs-alert-border-radius)}.alert-heading{color:inherit}.alert-link{font-weight:700;color:var(--bs-alert-link-color)}.alert-dismissible{padding-right:3rem}.alert-dismissible .btn-close{position:absolute;top:0;right:0;z-index:2;padding:1.25rem 1rem}.alert-primary{--bs-alert-color:var(--bs-primary-text-emphasis);--bs-alert-bg:var(--bs-primary-bg-subtle);--bs-alert-border-color:var(--bs-primary-border-subtle);--bs-alert-link-color:var(--bs-primary-text-emphasis)}.alert-secondary{--bs-alert-color:var(--bs-secondary-text-emphasis);--bs-alert-bg:var(--bs-secondary-bg-subtle);--bs-alert-border-color:var(--bs-secondary-border-subtle);--bs-alert-link-color:var(--bs-secondary-text-emphasis)}.alert-success{--bs-alert-color:var(--bs-success-text-emphasis);--bs-alert-bg:var(--bs-success-bg-subtle);--bs-alert-border-color:var(--bs-success-border-subtle);--bs-alert-link-color:var(--bs-success-text-emphasis)}.alert-info{--bs-alert-color:var(--bs-info-text-emphasis);--bs-alert-bg:var(--bs-info-bg-subtle);--bs-alert-border-color:var(--bs-info-border-subtle);--bs-alert-link-color:var(--bs-info-text-emphasis)}.alert-warning{--bs-alert-color:var(--bs-warning-text-emphasis);--bs-alert-bg:var(--bs-warning-bg-subtle);--bs-alert-border-color:var(--bs-warning-border-subtle);--bs-alert-link-color:var(--bs-warning-text-emphasis)}.alert-danger{--bs-alert-color:var(--bs-danger-text-emphasis);--bs-alert-bg:var(--bs-danger-bg-subtle);--bs-alert-border-color:var(--bs-danger-border-subtle);--bs-alert-link-color:var(--bs-danger-text-emphasis)}.alert-light{--bs-alert-color:var(--bs-light-text-emphasis);--bs-alert-bg:var(--bs-light-bg-subtle);--bs-alert-border-color:var(--bs-light-border-subtle);--bs-alert-link-color:var(--bs-light-text-emphasis)}.alert-dark{--bs-alert-color:var(--bs-dark-text-emphasis);--bs-alert-bg:var(--bs-dark-bg-subtle);--bs-alert-border-color:var(--bs-dark-border-subtle);--bs-alert-link-color:var(--bs-dark-text-emphasis)}@keyframes progress-bar-stripes{0%{background-position-x:var(--bs-progress-height)}}.progress,.progress-stacked{--bs-progress-height:1rem;--bs-progress-font-size:0.75rem;--bs-progress-bg:var(--bs-secondary-bg);--bs-progress-border-radius:var(--bs-border-radius);--bs-progress-box-shadow:var(--bs-box-shadow-inset);--bs-progress-bar-color:#fff;--bs-progress-bar-bg:#eb6864;--bs-progress-bar-transition:width 0.6s ease;display:flex;height:var(--bs-progress-height);overflow:hidden;font-size:var(--bs-progress-font-size);background-color:var(--bs-progress-bg);border-radius:var(--bs-progress-border-radius)}.progress-bar{display:flex;flex-direction:column;justify-content:center;overflow:hidden;color:var(--bs-progress-bar-color);text-align:center;white-space:nowrap;background-color:var(--bs-progress-bar-bg);transition:var(--bs-progress-bar-transition)}@media (prefers-reduced-motion:reduce){.progress-bar{transition:none}}.progress-bar-striped{background-image:linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);background-size:var(--bs-progress-height) var(--bs-progress-height)}.progress-stacked>.progress{overflow:visible}.progress-stacked>.progress>.progress-bar{width:100%}.progress-bar-animated{animation:1s linear infinite progress-bar-stripes}@media (prefers-reduced-motion:reduce){.progress-bar-animated{animation:none}}.list-group{--bs-list-group-color:var(--bs-body-color);--bs-list-group-bg:var(--bs-body-bg);--bs-list-group-border-color:var(--bs-border-color);--bs-list-group-border-width:var(--bs-border-width);--bs-list-group-border-radius:var(--bs-border-radius);--bs-list-group-item-padding-x:1rem;--bs-list-group-item-padding-y:0.5rem;--bs-list-group-action-color:var(--bs-secondary-color);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-tertiary-bg);--bs-list-group-action-active-color:var(--bs-body-color);--bs-list-group-action-active-bg:var(--bs-secondary-bg);--bs-list-group-disabled-color:var(--bs-secondary-color);--bs-list-group-disabled-bg:var(--bs-body-bg);--bs-list-group-active-color:#fff;--bs-list-group-active-bg:#eb6864;--bs-list-group-active-border-color:#eb6864;display:flex;flex-direction:column;padding-left:0;margin-bottom:0;border-radius:var(--bs-list-group-border-radius)}.list-group-numbered{list-style-type:none;counter-reset:section}.list-group-numbered>.list-group-item::before{content:counters(section, ".") ". ";counter-increment:section}.list-group-item{position:relative;display:block;padding:var(--bs-list-group-item-padding-y) var(--bs-list-group-item-padding-x);color:var(--bs-list-group-color);text-decoration:none;background-color:var(--bs-list-group-bg);border:var(--bs-list-group-border-width) solid var(--bs-list-group-border-color)}.list-group-item:first-child{border-top-left-radius:inherit;border-top-right-radius:inherit}.list-group-item:last-child{border-bottom-right-radius:inherit;border-bottom-left-radius:inherit}.list-group-item.disabled,.list-group-item:disabled{color:var(--bs-list-group-disabled-color);pointer-events:none;background-color:var(--bs-list-group-disabled-bg)}.list-group-item.active{z-index:2;color:var(--bs-list-group-active-color);background-color:var(--bs-list-group-active-bg);border-color:var(--bs-list-group-active-border-color)}.list-group-item+.list-group-item{border-top-width:0}.list-group-item+.list-group-item.active{margin-top:calc(-1 * var(--bs-list-group-border-width));border-top-width:var(--bs-list-group-border-width)}.list-group-item-action{width:100%;color:var(--bs-list-group-action-color);text-align:inherit}.list-group-item-action:not(.active):focus,.list-group-item-action:not(.active):hover{z-index:1;color:var(--bs-list-group-action-hover-color);text-decoration:none;background-color:var(--bs-list-group-action-hover-bg)}.list-group-item-action:not(.active):active{color:var(--bs-list-group-action-active-color);background-color:var(--bs-list-group-action-active-bg)}.list-group-horizontal{flex-direction:row}.list-group-horizontal>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal>.list-group-item.active{margin-top:0}.list-group-horizontal>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}@media (min-width:576px){.list-group-horizontal-sm{flex-direction:row}.list-group-horizontal-sm>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal-sm>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal-sm>.list-group-item.active{margin-top:0}.list-group-horizontal-sm>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal-sm>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}}@media (min-width:768px){.list-group-horizontal-md{flex-direction:row}.list-group-horizontal-md>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal-md>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal-md>.list-group-item.active{margin-top:0}.list-group-horizontal-md>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal-md>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}}@media (min-width:992px){.list-group-horizontal-lg{flex-direction:row}.list-group-horizontal-lg>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal-lg>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal-lg>.list-group-item.active{margin-top:0}.list-group-horizontal-lg>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal-lg>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}}@media (min-width:1200px){.list-group-horizontal-xl{flex-direction:row}.list-group-horizontal-xl>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal-xl>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal-xl>.list-group-item.active{margin-top:0}.list-group-horizontal-xl>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal-xl>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}}@media (min-width:1400px){.list-group-horizontal-xxl{flex-direction:row}.list-group-horizontal-xxl>.list-group-item:first-child:not(:last-child){border-bottom-left-radius:var(--bs-list-group-border-radius);border-top-right-radius:0}.list-group-horizontal-xxl>.list-group-item:last-child:not(:first-child){border-top-right-radius:var(--bs-list-group-border-radius);border-bottom-left-radius:0}.list-group-horizontal-xxl>.list-group-item.active{margin-top:0}.list-group-horizontal-xxl>.list-group-item+.list-group-item{border-top-width:var(--bs-list-group-border-width);border-left-width:0}.list-group-horizontal-xxl>.list-group-item+.list-group-item.active{margin-left:calc(-1 * var(--bs-list-group-border-width));border-left-width:var(--bs-list-group-border-width)}}.list-group-flush{border-radius:0}.list-group-flush>.list-group-item{border-width:0 0 var(--bs-list-group-border-width)}.list-group-flush>.list-group-item:last-child{border-bottom-width:0}.list-group-item-primary{--bs-list-group-color:var(--bs-primary-text-emphasis);--bs-list-group-bg:var(--bs-primary-bg-subtle);--bs-list-group-border-color:var(--bs-primary-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-primary-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-primary-border-subtle);--bs-list-group-active-color:var(--bs-primary-bg-subtle);--bs-list-group-active-bg:var(--bs-primary-text-emphasis);--bs-list-group-active-border-color:var(--bs-primary-text-emphasis)}.list-group-item-secondary{--bs-list-group-color:var(--bs-secondary-text-emphasis);--bs-list-group-bg:var(--bs-secondary-bg-subtle);--bs-list-group-border-color:var(--bs-secondary-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-secondary-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-secondary-border-subtle);--bs-list-group-active-color:var(--bs-secondary-bg-subtle);--bs-list-group-active-bg:var(--bs-secondary-text-emphasis);--bs-list-group-active-border-color:var(--bs-secondary-text-emphasis)}.list-group-item-success{--bs-list-group-color:var(--bs-success-text-emphasis);--bs-list-group-bg:var(--bs-success-bg-subtle);--bs-list-group-border-color:var(--bs-success-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-success-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-success-border-subtle);--bs-list-group-active-color:var(--bs-success-bg-subtle);--bs-list-group-active-bg:var(--bs-success-text-emphasis);--bs-list-group-active-border-color:var(--bs-success-text-emphasis)}.list-group-item-info{--bs-list-group-color:var(--bs-info-text-emphasis);--bs-list-group-bg:var(--bs-info-bg-subtle);--bs-list-group-border-color:var(--bs-info-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-info-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-info-border-subtle);--bs-list-group-active-color:var(--bs-info-bg-subtle);--bs-list-group-active-bg:var(--bs-info-text-emphasis);--bs-list-group-active-border-color:var(--bs-info-text-emphasis)}.list-group-item-warning{--bs-list-group-color:var(--bs-warning-text-emphasis);--bs-list-group-bg:var(--bs-warning-bg-subtle);--bs-list-group-border-color:var(--bs-warning-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-warning-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-warning-border-subtle);--bs-list-group-active-color:var(--bs-warning-bg-subtle);--bs-list-group-active-bg:var(--bs-warning-text-emphasis);--bs-list-group-active-border-color:var(--bs-warning-text-emphasis)}.list-group-item-danger{--bs-list-group-color:var(--bs-danger-text-emphasis);--bs-list-group-bg:var(--bs-danger-bg-subtle);--bs-list-group-border-color:var(--bs-danger-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-danger-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-danger-border-subtle);--bs-list-group-active-color:var(--bs-danger-bg-subtle);--bs-list-group-active-bg:var(--bs-danger-text-emphasis);--bs-list-group-active-border-color:var(--bs-danger-text-emphasis)}.list-group-item-light{--bs-list-group-color:var(--bs-light-text-emphasis);--bs-list-group-bg:var(--bs-light-bg-subtle);--bs-list-group-border-color:var(--bs-light-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-light-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-light-border-subtle);--bs-list-group-active-color:var(--bs-light-bg-subtle);--bs-list-group-active-bg:var(--bs-light-text-emphasis);--bs-list-group-active-border-color:var(--bs-light-text-emphasis)}.list-group-item-dark{--bs-list-group-color:var(--bs-dark-text-emphasis);--bs-list-group-bg:var(--bs-dark-bg-subtle);--bs-list-group-border-color:var(--bs-dark-border-subtle);--bs-list-group-action-hover-color:var(--bs-emphasis-color);--bs-list-group-action-hover-bg:var(--bs-dark-border-subtle);--bs-list-group-action-active-color:var(--bs-emphasis-color);--bs-list-group-action-active-bg:var(--bs-dark-border-subtle);--bs-list-group-active-color:var(--bs-dark-bg-subtle);--bs-list-group-active-bg:var(--bs-dark-text-emphasis);--bs-list-group-active-border-color:var(--bs-dark-text-emphasis)}.btn-close{--bs-btn-close-color:#000;--bs-btn-close-bg:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23000'%3e%3cpath d='M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414'/%3e%3c/svg%3e");--bs-btn-close-opacity:0.5;--bs-btn-close-hover-opacity:0.75;--bs-btn-close-focus-shadow:0 0 0 0.25rem rgba(235, 104, 100, 0.25);--bs-btn-close-focus-opacity:1;--bs-btn-close-disabled-opacity:0.25;box-sizing:content-box;width:1em;height:1em;padding:.25em .25em;color:var(--bs-btn-close-color);background:transparent var(--bs-btn-close-bg) center/1em auto no-repeat;filter:var(--bs-btn-close-filter);border:0;border-radius:.375rem;opacity:var(--bs-btn-close-opacity)}.btn-close:hover{color:var(--bs-btn-close-color);text-decoration:none;opacity:var(--bs-btn-close-hover-opacity)}.btn-close:focus{outline:0;box-shadow:var(--bs-btn-close-focus-shadow);opacity:var(--bs-btn-close-focus-opacity)}.btn-close.disabled,.btn-close:disabled{pointer-events:none;-webkit-user-select:none;-moz-user-select:none;user-select:none;opacity:var(--bs-btn-close-disabled-opacity)}.btn-close-white{--bs-btn-close-filter:invert(1) grayscale(100%) brightness(200%)}:root,[data-bs-theme=light]{--bs-btn-close-filter: }[data-bs-theme=dark]{--bs-btn-close-filter:invert(1) grayscale(100%) brightness(200%)}.toast{--bs-toast-zindex:1090;--bs-toast-padding-x:0.75rem;--bs-toast-padding-y:0.5rem;--bs-toast-spacing:1.5rem;--bs-toast-max-width:350px;--bs-toast-font-size:0.875rem;--bs-toast-color: ;--bs-toast-bg:rgba(var(--bs-body-bg-rgb), 0.85);--bs-toast-border-width:var(--bs-border-width);--bs-toast-border-color:var(--bs-border-color-translucent);--bs-toast-border-radius:var(--bs-border-radius);--bs-toast-box-shadow:var(--bs-box-shadow);--bs-toast-header-color:var(--bs-secondary-color);--bs-toast-header-bg:rgba(var(--bs-body-bg-rgb), 0.85);--bs-toast-header-border-color:var(--bs-border-color-translucent);width:var(--bs-toast-max-width);max-width:100%;font-size:var(--bs-toast-font-size);color:var(--bs-toast-color);pointer-events:auto;background-color:var(--bs-toast-bg);background-clip:padding-box;border:var(--bs-toast-border-width) solid var(--bs-toast-border-color);box-shadow:var(--bs-toast-box-shadow);border-radius:var(--bs-toast-border-radius)}.toast.showing{opacity:0}.toast:not(.show){display:none}.toast-container{--bs-toast-zindex:1090;position:absolute;z-index:var(--bs-toast-zindex);width:-webkit-max-content;width:-moz-max-content;width:max-content;max-width:100%;pointer-events:none}.toast-container>:not(:last-child){margin-bottom:var(--bs-toast-spacing)}.toast-header{display:flex;align-items:center;padding:var(--bs-toast-padding-y) var(--bs-toast-padding-x);color:var(--bs-toast-header-color);background-color:var(--bs-toast-header-bg);background-clip:padding-box;border-bottom:var(--bs-toast-border-width) solid var(--bs-toast-header-border-color);border-top-left-radius:calc(var(--bs-toast-border-radius) - var(--bs-toast-border-width));border-top-right-radius:calc(var(--bs-toast-border-radius) - var(--bs-toast-border-width))}.toast-header .btn-close{margin-right:calc(-.5 * var(--bs-toast-padding-x));margin-left:var(--bs-toast-padding-x)}.toast-body{padding:var(--bs-toast-padding-x);word-wrap:break-word}.modal{--bs-modal-zindex:1055;--bs-modal-width:500px;--bs-modal-padding:1rem;--bs-modal-margin:0.5rem;--bs-modal-color:var(--bs-body-color);--bs-modal-bg:var(--bs-body-bg);--bs-modal-border-color:var(--bs-border-color-translucent);--bs-modal-border-width:var(--bs-border-width);--bs-modal-border-radius:var(--bs-border-radius-lg);--bs-modal-box-shadow:var(--bs-box-shadow-sm);--bs-modal-inner-border-radius:calc(var(--bs-border-radius-lg) - (var(--bs-border-width)));--bs-modal-header-padding-x:1rem;--bs-modal-header-padding-y:1rem;--bs-modal-header-padding:1rem 1rem;--bs-modal-header-border-color:var(--bs-border-color);--bs-modal-header-border-width:var(--bs-border-width);--bs-modal-title-line-height:1.5;--bs-modal-footer-gap:0.5rem;--bs-modal-footer-bg: ;--bs-modal-footer-border-color:var(--bs-border-color);--bs-modal-footer-border-width:var(--bs-border-width);position:fixed;top:0;left:0;z-index:var(--bs-modal-zindex);display:none;width:100%;height:100%;overflow-x:hidden;overflow-y:auto;outline:0}.modal-dialog{position:relative;width:auto;margin:var(--bs-modal-margin);pointer-events:none}.modal.fade .modal-dialog{transform:translate(0,-50px);transition:transform .3s ease-out}@media (prefers-reduced-motion:reduce){.modal.fade .modal-dialog{transition:none}}.modal.show .modal-dialog{transform:none}.modal.modal-static .modal-dialog{transform:scale(1.02)}.modal-dialog-scrollable{height:calc(100% - var(--bs-modal-margin) * 2)}.modal-dialog-scrollable .modal-content{max-height:100%;overflow:hidden}.modal-dialog-scrollable .modal-body{overflow-y:auto}.modal-dialog-centered{display:flex;align-items:center;min-height:calc(100% - var(--bs-modal-margin) * 2)}.modal-content{position:relative;display:flex;flex-direction:column;width:100%;color:var(--bs-modal-color);pointer-events:auto;background-color:var(--bs-modal-bg);background-clip:padding-box;border:var(--bs-modal-border-width) solid var(--bs-modal-border-color);border-radius:var(--bs-modal-border-radius);outline:0}.modal-backdrop{--bs-backdrop-zindex:1050;--bs-backdrop-bg:#000;--bs-backdrop-opacity:0.5;position:fixed;top:0;left:0;z-index:var(--bs-backdrop-zindex);width:100vw;height:100vh;background-color:var(--bs-backdrop-bg)}.modal-backdrop.fade{opacity:0}.modal-backdrop.show{opacity:var(--bs-backdrop-opacity)}.modal-header{display:flex;flex-shrink:0;align-items:center;padding:var(--bs-modal-header-padding);border-bottom:var(--bs-modal-header-border-width) solid var(--bs-modal-header-border-color);border-top-left-radius:var(--bs-modal-inner-border-radius);border-top-right-radius:var(--bs-modal-inner-border-radius)}.modal-header .btn-close{padding:calc(var(--bs-modal-header-padding-y) * .5) calc(var(--bs-modal-header-padding-x) * .5);margin-top:calc(-.5 * var(--bs-modal-header-padding-y));margin-right:calc(-.5 * var(--bs-modal-header-padding-x));margin-bottom:calc(-.5 * var(--bs-modal-header-padding-y));margin-left:auto}.modal-title{margin-bottom:0;line-height:var(--bs-modal-title-line-height)}.modal-body{position:relative;flex:1 1 auto;padding:var(--bs-modal-padding)}.modal-footer{display:flex;flex-shrink:0;flex-wrap:wrap;align-items:center;justify-content:flex-end;padding:calc(var(--bs-modal-padding) - var(--bs-modal-footer-gap) * .5);background-color:var(--bs-modal-footer-bg);border-top:var(--bs-modal-footer-border-width) solid var(--bs-modal-footer-border-color);border-bottom-right-radius:var(--bs-modal-inner-border-radius);border-bottom-left-radius:var(--bs-modal-inner-border-radius)}.modal-footer>*{margin:calc(var(--bs-modal-footer-gap) * .5)}@media (min-width:576px){.modal{--bs-modal-margin:1.75rem;--bs-modal-box-shadow:var(--bs-box-shadow)}.modal-dialog{max-width:var(--bs-modal-width);margin-right:auto;margin-left:auto}.modal-sm{--bs-modal-width:300px}}@media (min-width:992px){.modal-lg,.modal-xl{--bs-modal-width:800px}}@media (min-width:1200px){.modal-xl{--bs-modal-width:1140px}}.modal-fullscreen{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen .modal-footer,.modal-fullscreen .modal-header{border-radius:0}.modal-fullscreen .modal-body{overflow-y:auto}@media (max-width:575.98px){.modal-fullscreen-sm-down{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen-sm-down .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen-sm-down .modal-footer,.modal-fullscreen-sm-down .modal-header{border-radius:0}.modal-fullscreen-sm-down .modal-body{overflow-y:auto}}@media (max-width:767.98px){.modal-fullscreen-md-down{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen-md-down .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen-md-down .modal-footer,.modal-fullscreen-md-down .modal-header{border-radius:0}.modal-fullscreen-md-down .modal-body{overflow-y:auto}}@media (max-width:991.98px){.modal-fullscreen-lg-down{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen-lg-down .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen-lg-down .modal-footer,.modal-fullscreen-lg-down .modal-header{border-radius:0}.modal-fullscreen-lg-down .modal-body{overflow-y:auto}}@media (max-width:1199.98px){.modal-fullscreen-xl-down{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen-xl-down .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen-xl-down .modal-footer,.modal-fullscreen-xl-down .modal-header{border-radius:0}.modal-fullscreen-xl-down .modal-body{overflow-y:auto}}@media (max-width:1399.98px){.modal-fullscreen-xxl-down{width:100vw;max-width:none;height:100%;margin:0}.modal-fullscreen-xxl-down .modal-content{height:100%;border:0;border-radius:0}.modal-fullscreen-xxl-down .modal-footer,.modal-fullscreen-xxl-down .modal-header{border-radius:0}.modal-fullscreen-xxl-down .modal-body{overflow-y:auto}}.tooltip{--bs-tooltip-zindex:1080;--bs-tooltip-max-width:200px;--bs-tooltip-padding-x:0.5rem;--bs-tooltip-padding-y:0.25rem;--bs-tooltip-margin: ;--bs-tooltip-font-size:0.875rem;--bs-tooltip-color:var(--bs-body-bg);--bs-tooltip-bg:var(--bs-emphasis-color);--bs-tooltip-border-radius:var(--bs-border-radius);--bs-tooltip-opacity:0.9;--bs-tooltip-arrow-width:0.8rem;--bs-tooltip-arrow-height:0.4rem;z-index:var(--bs-tooltip-zindex);display:block;margin:var(--bs-tooltip-margin);font-family:var(--bs-font-sans-serif);font-style:normal;font-weight:400;line-height:1.5;text-align:left;text-align:start;text-decoration:none;text-shadow:none;text-transform:none;letter-spacing:normal;word-break:normal;white-space:normal;word-spacing:normal;line-break:auto;font-size:var(--bs-tooltip-font-size);word-wrap:break-word;opacity:0}.tooltip.show{opacity:var(--bs-tooltip-opacity)}.tooltip .tooltip-arrow{display:block;width:var(--bs-tooltip-arrow-width);height:var(--bs-tooltip-arrow-height)}.tooltip .tooltip-arrow::before{position:absolute;content:"";border-color:transparent;border-style:solid}.bs-tooltip-auto[data-popper-placement^=top] .tooltip-arrow,.bs-tooltip-top .tooltip-arrow{bottom:calc(-1 * var(--bs-tooltip-arrow-height))}.bs-tooltip-auto[data-popper-placement^=top] .tooltip-arrow::before,.bs-tooltip-top .tooltip-arrow::before{top:-1px;border-width:var(--bs-tooltip-arrow-height) calc(var(--bs-tooltip-arrow-width) * .5) 0;border-top-color:var(--bs-tooltip-bg)}.bs-tooltip-auto[data-popper-placement^=right] .tooltip-arrow,.bs-tooltip-end .tooltip-arrow{left:calc(-1 * var(--bs-tooltip-arrow-height));width:var(--bs-tooltip-arrow-height);height:var(--bs-tooltip-arrow-width)}.bs-tooltip-auto[data-popper-placement^=right] .tooltip-arrow::before,.bs-tooltip-end .tooltip-arrow::before{right:-1px;border-width:calc(var(--bs-tooltip-arrow-width) * .5) var(--bs-tooltip-arrow-height) calc(var(--bs-tooltip-arrow-width) * .5) 0;border-right-color:var(--bs-tooltip-bg)}.bs-tooltip-auto[data-popper-placement^=bottom] .tooltip-arrow,.bs-tooltip-bottom .tooltip-arrow{top:calc(-1 * var(--bs-tooltip-arrow-height))}.bs-tooltip-auto[data-popper-placement^=bottom] .tooltip-arrow::before,.bs-tooltip-bottom .tooltip-arrow::before{bottom:-1px;border-width:0 calc(var(--bs-tooltip-arrow-width) * .5) var(--bs-tooltip-arrow-height);border-bottom-color:var(--bs-tooltip-bg)}.bs-tooltip-auto[data-popper-placement^=left] .tooltip-arrow,.bs-tooltip-start .tooltip-arrow{right:calc(-1 * var(--bs-tooltip-arrow-height));width:var(--bs-tooltip-arrow-height);height:var(--bs-tooltip-arrow-width)}.bs-tooltip-auto[data-popper-placement^=left] .tooltip-arrow::before,.bs-tooltip-start .tooltip-arrow::before{left:-1px;border-width:calc(var(--bs-tooltip-arrow-width) * .5) 0 calc(var(--bs-tooltip-arrow-width) * .5) var(--bs-tooltip-arrow-height);border-left-color:var(--bs-tooltip-bg)}.tooltip-inner{max-width:var(--bs-tooltip-max-width);padding:var(--bs-tooltip-padding-y) var(--bs-tooltip-padding-x);color:var(--bs-tooltip-color);text-align:center;background-color:var(--bs-tooltip-bg);border-radius:var(--bs-tooltip-border-radius)}.popover{--bs-popover-zindex:1070;--bs-popover-max-width:276px;--bs-popover-font-size:0.875rem;--bs-popover-bg:var(--bs-body-bg);--bs-popover-border-width:var(--bs-border-width);--bs-popover-border-color:var(--bs-border-color-translucent);--bs-popover-border-radius:var(--bs-border-radius-lg);--bs-popover-inner-border-radius:calc(var(--bs-border-radius-lg) - var(--bs-border-width));--bs-popover-box-shadow:var(--bs-box-shadow);--bs-popover-header-padding-x:1rem;--bs-popover-header-padding-y:0.5rem;--bs-popover-header-font-size:1rem;--bs-popover-header-color:inherit;--bs-popover-header-bg:var(--bs-secondary-bg);--bs-popover-body-padding-x:1rem;--bs-popover-body-padding-y:1rem;--bs-popover-body-color:var(--bs-body-color);--bs-popover-arrow-width:1rem;--bs-popover-arrow-height:0.5rem;--bs-popover-arrow-border:var(--bs-popover-border-color);z-index:var(--bs-popover-zindex);display:block;max-width:var(--bs-popover-max-width);font-family:var(--bs-font-sans-serif);font-style:normal;font-weight:400;line-height:1.5;text-align:left;text-align:start;text-decoration:none;text-shadow:none;text-transform:none;letter-spacing:normal;word-break:normal;white-space:normal;word-spacing:normal;line-break:auto;font-size:var(--bs-popover-font-size);word-wrap:break-word;background-color:var(--bs-popover-bg);background-clip:padding-box;border:var(--bs-popover-border-width) solid var(--bs-popover-border-color);border-radius:var(--bs-popover-border-radius)}.popover .popover-arrow{display:block;width:var(--bs-popover-arrow-width);height:var(--bs-popover-arrow-height)}.popover .popover-arrow::after,.popover .popover-arrow::before{position:absolute;display:block;content:"";border-color:transparent;border-style:solid;border-width:0}.bs-popover-auto[data-popper-placement^=top]>.popover-arrow,.bs-popover-top>.popover-arrow{bottom:calc(-1 * (var(--bs-popover-arrow-height)) - var(--bs-popover-border-width))}.bs-popover-auto[data-popper-placement^=top]>.popover-arrow::after,.bs-popover-auto[data-popper-placement^=top]>.popover-arrow::before,.bs-popover-top>.popover-arrow::after,.bs-popover-top>.popover-arrow::before{border-width:var(--bs-popover-arrow-height) calc(var(--bs-popover-arrow-width) * .5) 0}.bs-popover-auto[data-popper-placement^=top]>.popover-arrow::before,.bs-popover-top>.popover-arrow::before{bottom:0;border-top-color:var(--bs-popover-arrow-border)}.bs-popover-auto[data-popper-placement^=top]>.popover-arrow::after,.bs-popover-top>.popover-arrow::after{bottom:var(--bs-popover-border-width);border-top-color:var(--bs-popover-bg)}.bs-popover-auto[data-popper-placement^=right]>.popover-arrow,.bs-popover-end>.popover-arrow{left:calc(-1 * (var(--bs-popover-arrow-height)) - var(--bs-popover-border-width));width:var(--bs-popover-arrow-height);height:var(--bs-popover-arrow-width)}.bs-popover-auto[data-popper-placement^=right]>.popover-arrow::after,.bs-popover-auto[data-popper-placement^=right]>.popover-arrow::before,.bs-popover-end>.popover-arrow::after,.bs-popover-end>.popover-arrow::before{border-width:calc(var(--bs-popover-arrow-width) * .5) var(--bs-popover-arrow-height) calc(var(--bs-popover-arrow-width) * .5) 0}.bs-popover-auto[data-popper-placement^=right]>.popover-arrow::before,.bs-popover-end>.popover-arrow::before{left:0;border-right-color:var(--bs-popover-arrow-border)}.bs-popover-auto[data-popper-placement^=right]>.popover-arrow::after,.bs-popover-end>.popover-arrow::after{left:var(--bs-popover-border-width);border-right-color:var(--bs-popover-bg)}.bs-popover-auto[data-popper-placement^=bottom]>.popover-arrow,.bs-popover-bottom>.popover-arrow{top:calc(-1 * (var(--bs-popover-arrow-height)) - var(--bs-popover-border-width))}.bs-popover-auto[data-popper-placement^=bottom]>.popover-arrow::after,.bs-popover-auto[data-popper-placement^=bottom]>.popover-arrow::before,.bs-popover-bottom>.popover-arrow::after,.bs-popover-bottom>.popover-arrow::before{border-width:0 calc(var(--bs-popover-arrow-width) * .5) var(--bs-popover-arrow-height)}.bs-popover-auto[data-popper-placement^=bottom]>.popover-arrow::before,.bs-popover-bottom>.popover-arrow::before{top:0;border-bottom-color:var(--bs-popover-arrow-border)}.bs-popover-auto[data-popper-placement^=bottom]>.popover-arrow::after,.bs-popover-bottom>.popover-arrow::after{top:var(--bs-popover-border-width);border-bottom-color:var(--bs-popover-bg)}.bs-popover-auto[data-popper-placement^=bottom] .popover-header::before,.bs-popover-bottom .popover-header::before{position:absolute;top:0;left:50%;display:block;width:var(--bs-popover-arrow-width);margin-left:calc(-.5 * var(--bs-popover-arrow-width));content:"";border-bottom:var(--bs-popover-border-width) solid var(--bs-popover-header-bg)}.bs-popover-auto[data-popper-placement^=left]>.popover-arrow,.bs-popover-start>.popover-arrow{right:calc(-1 * (var(--bs-popover-arrow-height)) - var(--bs-popover-border-width));width:var(--bs-popover-arrow-height);height:var(--bs-popover-arrow-width)}.bs-popover-auto[data-popper-placement^=left]>.popover-arrow::after,.bs-popover-auto[data-popper-placement^=left]>.popover-arrow::before,.bs-popover-start>.popover-arrow::after,.bs-popover-start>.popover-arrow::before{border-width:calc(var(--bs-popover-arrow-width) * .5) 0 calc(var(--bs-popover-arrow-width) * .5) var(--bs-popover-arrow-height)}.bs-popover-auto[data-popper-placement^=left]>.popover-arrow::before,.bs-popover-start>.popover-arrow::before{right:0;border-left-color:var(--bs-popover-arrow-border)}.bs-popover-auto[data-popper-placement^=left]>.popover-arrow::after,.bs-popover-start>.popover-arrow::after{right:var(--bs-popover-border-width);border-left-color:var(--bs-popover-bg)}.popover-header{padding:var(--bs-popover-header-padding-y) var(--bs-popover-header-padding-x);margin-bottom:0;font-size:var(--bs-popover-header-font-size);color:var(--bs-popover-header-color);background-color:var(--bs-popover-header-bg);border-bottom:var(--bs-popover-border-width) solid var(--bs-popover-border-color);border-top-left-radius:var(--bs-popover-inner-border-radius);border-top-right-radius:var(--bs-popover-inner-border-radius)}.popover-header:empty{display:none}.popover-body{padding:var(--bs-popover-body-padding-y) var(--bs-popover-body-padding-x);color:var(--bs-popover-body-color)}.carousel{position:relative}.carousel.pointer-event{touch-action:pan-y}.carousel-inner{position:relative;width:100%;overflow:hidden}.carousel-inner::after{display:block;clear:both;content:""}.carousel-item{position:relative;display:none;float:left;width:100%;margin-right:-100%;-webkit-backface-visibility:hidden;backface-visibility:hidden;transition:transform .6s ease-in-out}@media (prefers-reduced-motion:reduce){.carousel-item{transition:none}}.carousel-item-next,.carousel-item-prev,.carousel-item.active{display:block}.active.carousel-item-end,.carousel-item-next:not(.carousel-item-start){transform:translateX(100%)}.active.carousel-item-start,.carousel-item-prev:not(.carousel-item-end){transform:translateX(-100%)}.carousel-fade .carousel-item{opacity:0;transition-property:opacity;transform:none}.carousel-fade .carousel-item-next.carousel-item-start,.carousel-fade .carousel-item-prev.carousel-item-end,.carousel-fade .carousel-item.active{z-index:1;opacity:1}.carousel-fade .active.carousel-item-end,.carousel-fade .active.carousel-item-start{z-index:0;opacity:0;transition:opacity 0s .6s}@media (prefers-reduced-motion:reduce){.carousel-fade .active.carousel-item-end,.carousel-fade .active.carousel-item-start{transition:none}}.carousel-control-next,.carousel-control-prev{position:absolute;top:0;bottom:0;z-index:1;display:flex;align-items:center;justify-content:center;width:15%;padding:0;color:#fff;text-align:center;background:0 0;filter:var(--bs-carousel-control-icon-filter);border:0;opacity:.5;transition:opacity .15s ease}@media (prefers-reduced-motion:reduce){.carousel-control-next,.carousel-control-prev{transition:none}}.carousel-control-next:focus,.carousel-control-next:hover,.carousel-control-prev:focus,.carousel-control-prev:hover{color:#fff;text-decoration:none;outline:0;opacity:.9}.carousel-control-prev{left:0}.carousel-control-next{right:0}.carousel-control-next-icon,.carousel-control-prev-icon{display:inline-block;width:2rem;height:2rem;background-repeat:no-repeat;background-position:50%;background-size:100% 100%}.carousel-control-prev-icon{background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0'/%3e%3c/svg%3e")}.carousel-control-next-icon{background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708'/%3e%3c/svg%3e")}.carousel-indicators{position:absolute;right:0;bottom:0;left:0;z-index:2;display:flex;justify-content:center;padding:0;margin-right:15%;margin-bottom:1rem;margin-left:15%}.carousel-indicators [data-bs-target]{box-sizing:content-box;flex:0 1 auto;width:30px;height:3px;padding:0;margin-right:3px;margin-left:3px;text-indent:-999px;cursor:pointer;background-color:var(--bs-carousel-indicator-active-bg);background-clip:padding-box;border:0;border-top:10px solid transparent;border-bottom:10px solid transparent;opacity:.5;transition:opacity .6s ease}@media (prefers-reduced-motion:reduce){.carousel-indicators [data-bs-target]{transition:none}}.carousel-indicators .active{opacity:1}.carousel-caption{position:absolute;right:15%;bottom:1.25rem;left:15%;padding-top:1.25rem;padding-bottom:1.25rem;color:var(--bs-carousel-caption-color);text-align:center}.carousel-dark{--bs-carousel-indicator-active-bg:#000;--bs-carousel-caption-color:#000;--bs-carousel-control-icon-filter:invert(1) grayscale(100)}:root,[data-bs-theme=light]{--bs-carousel-indicator-active-bg:#fff;--bs-carousel-caption-color:#fff;--bs-carousel-control-icon-filter: }[data-bs-theme=dark]{--bs-carousel-indicator-active-bg:#000;--bs-carousel-caption-color:#000;--bs-carousel-control-icon-filter:invert(1) grayscale(100)}.spinner-border,.spinner-grow{display:inline-block;width:var(--bs-spinner-width);height:var(--bs-spinner-height);vertical-align:var(--bs-spinner-vertical-align);border-radius:50%;animation:var(--bs-spinner-animation-speed) linear infinite var(--bs-spinner-animation-name)}@keyframes spinner-border{to{transform:rotate(360deg)}}.spinner-border{--bs-spinner-width:2rem;--bs-spinner-height:2rem;--bs-spinner-vertical-align:-0.125em;--bs-spinner-border-width:0.25em;--bs-spinner-animation-speed:0.75s;--bs-spinner-animation-name:spinner-border;border:var(--bs-spinner-border-width) solid currentcolor;border-right-color:transparent}.spinner-border-sm{--bs-spinner-width:1rem;--bs-spinner-height:1rem;--bs-spinner-border-width:0.2em}@keyframes spinner-grow{0%{transform:scale(0)}50%{opacity:1;transform:none}}.spinner-grow{--bs-spinner-width:2rem;--bs-spinner-height:2rem;--bs-spinner-vertical-align:-0.125em;--bs-spinner-animation-speed:0.75s;--bs-spinner-animation-name:spinner-grow;background-color:currentcolor;opacity:0}.spinner-grow-sm{--bs-spinner-width:1rem;--bs-spinner-height:1rem}@media (prefers-reduced-motion:reduce){.spinner-border,.spinner-grow{--bs-spinner-animation-speed:1.5s}}.offcanvas,.offcanvas-lg,.offcanvas-md,.offcanvas-sm,.offcanvas-xl,.offcanvas-xxl{--bs-offcanvas-zindex:1045;--bs-offcanvas-width:400px;--bs-offcanvas-height:30vh;--bs-offcanvas-padding-x:1rem;--bs-offcanvas-padding-y:1rem;--bs-offcanvas-color:var(--bs-body-color);--bs-offcanvas-bg:var(--bs-body-bg);--bs-offcanvas-border-width:var(--bs-border-width);--bs-offcanvas-border-color:var(--bs-border-color-translucent);--bs-offcanvas-box-shadow:var(--bs-box-shadow-sm);--bs-offcanvas-transition:transform 0.3s ease-in-out;--bs-offcanvas-title-line-height:1.5}@media (max-width:575.98px){.offcanvas-sm{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}}@media (max-width:575.98px) and (prefers-reduced-motion:reduce){.offcanvas-sm{transition:none}}@media (max-width:575.98px){.offcanvas-sm.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas-sm.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas-sm.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas-sm.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas-sm.show:not(.hiding),.offcanvas-sm.showing{transform:none}.offcanvas-sm.hiding,.offcanvas-sm.show,.offcanvas-sm.showing{visibility:visible}}@media (min-width:576px){.offcanvas-sm{--bs-offcanvas-height:auto;--bs-offcanvas-border-width:0;background-color:transparent!important}.offcanvas-sm .offcanvas-header{display:none}.offcanvas-sm .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible;background-color:transparent!important}}@media (max-width:767.98px){.offcanvas-md{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}}@media (max-width:767.98px) and (prefers-reduced-motion:reduce){.offcanvas-md{transition:none}}@media (max-width:767.98px){.offcanvas-md.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas-md.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas-md.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas-md.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas-md.show:not(.hiding),.offcanvas-md.showing{transform:none}.offcanvas-md.hiding,.offcanvas-md.show,.offcanvas-md.showing{visibility:visible}}@media (min-width:768px){.offcanvas-md{--bs-offcanvas-height:auto;--bs-offcanvas-border-width:0;background-color:transparent!important}.offcanvas-md .offcanvas-header{display:none}.offcanvas-md .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible;background-color:transparent!important}}@media (max-width:991.98px){.offcanvas-lg{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}}@media (max-width:991.98px) and (prefers-reduced-motion:reduce){.offcanvas-lg{transition:none}}@media (max-width:991.98px){.offcanvas-lg.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas-lg.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas-lg.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas-lg.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas-lg.show:not(.hiding),.offcanvas-lg.showing{transform:none}.offcanvas-lg.hiding,.offcanvas-lg.show,.offcanvas-lg.showing{visibility:visible}}@media (min-width:992px){.offcanvas-lg{--bs-offcanvas-height:auto;--bs-offcanvas-border-width:0;background-color:transparent!important}.offcanvas-lg .offcanvas-header{display:none}.offcanvas-lg .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible;background-color:transparent!important}}@media (max-width:1199.98px){.offcanvas-xl{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}}@media (max-width:1199.98px) and (prefers-reduced-motion:reduce){.offcanvas-xl{transition:none}}@media (max-width:1199.98px){.offcanvas-xl.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas-xl.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas-xl.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas-xl.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas-xl.show:not(.hiding),.offcanvas-xl.showing{transform:none}.offcanvas-xl.hiding,.offcanvas-xl.show,.offcanvas-xl.showing{visibility:visible}}@media (min-width:1200px){.offcanvas-xl{--bs-offcanvas-height:auto;--bs-offcanvas-border-width:0;background-color:transparent!important}.offcanvas-xl .offcanvas-header{display:none}.offcanvas-xl .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible;background-color:transparent!important}}@media (max-width:1399.98px){.offcanvas-xxl{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}}@media (max-width:1399.98px) and (prefers-reduced-motion:reduce){.offcanvas-xxl{transition:none}}@media (max-width:1399.98px){.offcanvas-xxl.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas-xxl.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas-xxl.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas-xxl.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas-xxl.show:not(.hiding),.offcanvas-xxl.showing{transform:none}.offcanvas-xxl.hiding,.offcanvas-xxl.show,.offcanvas-xxl.showing{visibility:visible}}@media (min-width:1400px){.offcanvas-xxl{--bs-offcanvas-height:auto;--bs-offcanvas-border-width:0;background-color:transparent!important}.offcanvas-xxl .offcanvas-header{display:none}.offcanvas-xxl .offcanvas-body{display:flex;flex-grow:0;padding:0;overflow-y:visible;background-color:transparent!important}}.offcanvas{position:fixed;bottom:0;z-index:var(--bs-offcanvas-zindex);display:flex;flex-direction:column;max-width:100%;color:var(--bs-offcanvas-color);visibility:hidden;background-color:var(--bs-offcanvas-bg);background-clip:padding-box;outline:0;transition:var(--bs-offcanvas-transition)}@media (prefers-reduced-motion:reduce){.offcanvas{transition:none}}.offcanvas.offcanvas-start{top:0;left:0;width:var(--bs-offcanvas-width);border-right:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(-100%)}.offcanvas.offcanvas-end{top:0;right:0;width:var(--bs-offcanvas-width);border-left:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateX(100%)}.offcanvas.offcanvas-top{top:0;right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-bottom:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(-100%)}.offcanvas.offcanvas-bottom{right:0;left:0;height:var(--bs-offcanvas-height);max-height:100%;border-top:var(--bs-offcanvas-border-width) solid var(--bs-offcanvas-border-color);transform:translateY(100%)}.offcanvas.show:not(.hiding),.offcanvas.showing{transform:none}.offcanvas.hiding,.offcanvas.show,.offcanvas.showing{visibility:visible}.offcanvas-backdrop{position:fixed;top:0;left:0;z-index:1040;width:100vw;height:100vh;background-color:#000}.offcanvas-backdrop.fade{opacity:0}.offcanvas-backdrop.show{opacity:.5}.offcanvas-header{display:flex;align-items:center;padding:var(--bs-offcanvas-padding-y) var(--bs-offcanvas-padding-x)}.offcanvas-header .btn-close{padding:calc(var(--bs-offcanvas-padding-y) * .5) calc(var(--bs-offcanvas-padding-x) * .5);margin-top:calc(-.5 * var(--bs-offcanvas-padding-y));margin-right:calc(-.5 * var(--bs-offcanvas-padding-x));margin-bottom:calc(-.5 * var(--bs-offcanvas-padding-y));margin-left:auto}.offcanvas-title{margin-bottom:0;line-height:var(--bs-offcanvas-title-line-height)}.offcanvas-body{flex-grow:1;padding:var(--bs-offcanvas-padding-y) var(--bs-offcanvas-padding-x);overflow-y:auto}.placeholder{display:inline-block;min-height:1em;vertical-align:middle;cursor:wait;background-color:currentcolor;opacity:.5}.placeholder.btn::before{display:inline-block;content:""}.placeholder-xs{min-height:.6em}.placeholder-sm{min-height:.8em}.placeholder-lg{min-height:1.2em}.placeholder-glow .placeholder{animation:placeholder-glow 2s ease-in-out infinite}@keyframes placeholder-glow{50%{opacity:.2}}.placeholder-wave{-webkit-mask-image:linear-gradient(130deg,#000 55%,rgba(0,0,0,0.8) 75%,#000 95%);mask-image:linear-gradient(130deg,#000 55%,rgba(0,0,0,0.8) 75%,#000 95%);-webkit-mask-size:200% 100%;mask-size:200% 100%;animation:placeholder-wave 2s linear infinite}@keyframes placeholder-wave{100%{-webkit-mask-position:-200% 0%;mask-position:-200% 0%}}.clearfix::after{display:block;clear:both;content:""}.text-bg-primary{color:#fff!important;background-color:RGBA(var(--bs-primary-rgb),var(--bs-bg-opacity,1))!important}.text-bg-secondary{color:#fff!important;background-color:RGBA(var(--bs-secondary-rgb),var(--bs-bg-opacity,1))!important}.text-bg-success{color:#fff!important;background-color:RGBA(var(--bs-success-rgb),var(--bs-bg-opacity,1))!important}.text-bg-info{color:#fff!important;background-color:RGBA(var(--bs-info-rgb),var(--bs-bg-opacity,1))!important}.text-bg-warning{color:#fff!important;background-color:RGBA(var(--bs-warning-rgb),var(--bs-bg-opacity,1))!important}.text-bg-danger{color:#fff!important;background-color:RGBA(var(--bs-danger-rgb),var(--bs-bg-opacity,1))!important}.text-bg-light{color:#000!important;background-color:RGBA(var(--bs-light-rgb),var(--bs-bg-opacity,1))!important}.text-bg-dark{color:#fff!important;background-color:RGBA(var(--bs-dark-rgb),var(--bs-bg-opacity,1))!important}.link-primary{color:RGBA(var(--bs-primary-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-primary-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-primary-rgb),var(--bs-link-underline-opacity,1))!important}.link-primary:focus,.link-primary:hover{color:RGBA(188,83,80,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(188,83,80,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(188,83,80,var(--bs-link-underline-opacity,1))!important}.link-secondary{color:RGBA(var(--bs-secondary-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-secondary-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-secondary-rgb),var(--bs-link-underline-opacity,1))!important}.link-secondary:focus,.link-secondary:hover{color:RGBA(136,136,136,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(136,136,136,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(136,136,136,var(--bs-link-underline-opacity,1))!important}.link-success{color:RGBA(var(--bs-success-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-success-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-success-rgb),var(--bs-link-underline-opacity,1))!important}.link-success:focus,.link-success:hover{color:RGBA(27,142,61,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(27,142,61,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(27,142,61,var(--bs-link-underline-opacity,1))!important}.link-info{color:RGBA(var(--bs-info-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-info-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-info-rgb),var(--bs-link-underline-opacity,1))!important}.link-info:focus,.link-info:hover{color:RGBA(41,82,122,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(41,82,122,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(41,82,122,var(--bs-link-underline-opacity,1))!important}.link-warning{color:RGBA(var(--bs-warning-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-warning-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-warning-rgb),var(--bs-link-underline-opacity,1))!important}.link-warning:focus,.link-warning:hover{color:RGBA(196,184,30,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(196,184,30,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(196,184,30,var(--bs-link-underline-opacity,1))!important}.link-danger{color:RGBA(var(--bs-danger-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-danger-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-danger-rgb),var(--bs-link-underline-opacity,1))!important}.link-danger:focus,.link-danger:hover{color:RGBA(196,98,0,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(196,98,0,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(196,98,0,var(--bs-link-underline-opacity,1))!important}.link-light{color:RGBA(var(--bs-light-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-light-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-light-rgb),var(--bs-link-underline-opacity,1))!important}.link-light:focus,.link-light:hover{color:RGBA(249,250,251,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(249,250,251,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(249,250,251,var(--bs-link-underline-opacity,1))!important}.link-dark{color:RGBA(var(--bs-dark-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-dark-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-dark-rgb),var(--bs-link-underline-opacity,1))!important}.link-dark:focus,.link-dark:hover{color:RGBA(27,27,27,var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(27,27,27,var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(27,27,27,var(--bs-link-underline-opacity,1))!important}.link-body-emphasis{color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-opacity,1))!important;-webkit-text-decoration-color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-underline-opacity,1))!important}.link-body-emphasis:focus,.link-body-emphasis:hover{color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-opacity,.75))!important;-webkit-text-decoration-color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-underline-opacity,0.75))!important;text-decoration-color:RGBA(var(--bs-emphasis-color-rgb),var(--bs-link-underline-opacity,0.75))!important}.focus-ring:focus{outline:0;box-shadow:var(--bs-focus-ring-x,0) var(--bs-focus-ring-y,0) var(--bs-focus-ring-blur,0) var(--bs-focus-ring-width) var(--bs-focus-ring-color)}.icon-link{display:inline-flex;gap:.375rem;align-items:center;-webkit-text-decoration-color:rgba(var(--bs-link-color-rgb),var(--bs-link-opacity,0.5));text-decoration-color:rgba(var(--bs-link-color-rgb),var(--bs-link-opacity,0.5));text-underline-offset:0.25em;-webkit-backface-visibility:hidden;backface-visibility:hidden}.icon-link>.bi{flex-shrink:0;width:1em;height:1em;fill:currentcolor;transition:.2s ease-in-out transform}@media (prefers-reduced-motion:reduce){.icon-link>.bi{transition:none}}.icon-link-hover:focus-visible>.bi,.icon-link-hover:hover>.bi{transform:var(--bs-icon-link-transform,translate3d(.25em,0,0))}.ratio{position:relative;width:100%}.ratio::before{display:block;padding-top:var(--bs-aspect-ratio);content:""}.ratio>*{position:absolute;top:0;left:0;width:100%;height:100%}.ratio-1x1{--bs-aspect-ratio:100%}.ratio-4x3{--bs-aspect-ratio:75%}.ratio-16x9{--bs-aspect-ratio:56.25%}.ratio-21x9{--bs-aspect-ratio:42.8571428571%}.fixed-top{position:fixed;top:0;right:0;left:0;z-index:1030}.fixed-bottom{position:fixed;right:0;bottom:0;left:0;z-index:1030}.sticky-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}@media (min-width:576px){.sticky-sm-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-sm-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}}@media (min-width:768px){.sticky-md-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-md-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}}@media (min-width:992px){.sticky-lg-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-lg-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}}@media (min-width:1200px){.sticky-xl-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-xl-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}}@media (min-width:1400px){.sticky-xxl-top{position:-webkit-sticky;position:sticky;top:0;z-index:1020}.sticky-xxl-bottom{position:-webkit-sticky;position:sticky;bottom:0;z-index:1020}}.hstack{display:flex;flex-direction:row;align-items:center;align-self:stretch}.vstack{display:flex;flex:1 1 auto;flex-direction:column;align-self:stretch}.visually-hidden,.visually-hidden-focusable:not(:focus):not(:focus-within){width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}.visually-hidden-focusable:not(:focus):not(:focus-within):not(caption),.visually-hidden:not(caption){position:absolute!important}.stretched-link::after{position:absolute;top:0;right:0;bottom:0;left:0;z-index:1;content:""}.text-truncate{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.vr{display:inline-block;align-self:stretch;width:var(--bs-border-width);min-height:1em;background-color:currentcolor;opacity:.25}.align-baseline{vertical-align:baseline!important}.align-top{vertical-align:top!important}.align-middle{vertical-align:middle!important}.align-bottom{vertical-align:bottom!important}.align-text-bottom{vertical-align:text-bottom!important}.align-text-top{vertical-align:text-top!important}.float-start{float:left!important}.float-end{float:right!important}.float-none{float:none!important}.object-fit-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-none{-o-object-fit:none!important;object-fit:none!important}.opacity-0{opacity:0!important}.opacity-25{opacity:.25!important}.opacity-50{opacity:.5!important}.opacity-75{opacity:.75!important}.opacity-100{opacity:1!important}.overflow-auto{overflow:auto!important}.overflow-hidden{overflow:hidden!important}.overflow-visible{overflow:visible!important}.overflow-scroll{overflow:scroll!important}.overflow-x-auto{overflow-x:auto!important}.overflow-x-hidden{overflow-x:hidden!important}.overflow-x-visible{overflow-x:visible!important}.overflow-x-scroll{overflow-x:scroll!important}.overflow-y-auto{overflow-y:auto!important}.overflow-y-hidden{overflow-y:hidden!important}.overflow-y-visible{overflow-y:visible!important}.overflow-y-scroll{overflow-y:scroll!important}.d-inline{display:inline!important}.d-inline-block{display:inline-block!important}.d-block{display:block!important}.d-grid{display:grid!important}.d-inline-grid{display:inline-grid!important}.d-table{display:table!important}.d-table-row{display:table-row!important}.d-table-cell{display:table-cell!important}.d-flex{display:flex!important}.d-inline-flex{display:inline-flex!important}.d-none{display:none!important}.shadow{box-shadow:var(--bs-box-shadow)!important}.shadow-sm{box-shadow:var(--bs-box-shadow-sm)!important}.shadow-lg{box-shadow:var(--bs-box-shadow-lg)!important}.shadow-none{box-shadow:none!important}.focus-ring-primary{--bs-focus-ring-color:rgba(var(--bs-primary-rgb), var(--bs-focus-ring-opacity))}.focus-ring-secondary{--bs-focus-ring-color:rgba(var(--bs-secondary-rgb), var(--bs-focus-ring-opacity))}.focus-ring-success{--bs-focus-ring-color:rgba(var(--bs-success-rgb), var(--bs-focus-ring-opacity))}.focus-ring-info{--bs-focus-ring-color:rgba(var(--bs-info-rgb), var(--bs-focus-ring-opacity))}.focus-ring-warning{--bs-focus-ring-color:rgba(var(--bs-warning-rgb), var(--bs-focus-ring-opacity))}.focus-ring-danger{--bs-focus-ring-color:rgba(var(--bs-danger-rgb), var(--bs-focus-ring-opacity))}.focus-ring-light{--bs-focus-ring-color:rgba(var(--bs-light-rgb), var(--bs-focus-ring-opacity))}.focus-ring-dark{--bs-focus-ring-color:rgba(var(--bs-dark-rgb), var(--bs-focus-ring-opacity))}.position-static{position:static!important}.position-relative{position:relative!important}.position-absolute{position:absolute!important}.position-fixed{position:fixed!important}.position-sticky{position:-webkit-sticky!important;position:sticky!important}.top-0{top:0!important}.top-50{top:50%!important}.top-100{top:100%!important}.bottom-0{bottom:0!important}.bottom-50{bottom:50%!important}.bottom-100{bottom:100%!important}.start-0{left:0!important}.start-50{left:50%!important}.start-100{left:100%!important}.end-0{right:0!important}.end-50{right:50%!important}.end-100{right:100%!important}.translate-middle{transform:translate(-50%,-50%)!important}.translate-middle-x{transform:translateX(-50%)!important}.translate-middle-y{transform:translateY(-50%)!important}.border{border:var(--bs-border-width) var(--bs-border-style) var(--bs-border-color)!important}.border-0{border:0!important}.border-top{border-top:var(--bs-border-width) var(--bs-border-style) var(--bs-border-color)!important}.border-top-0{border-top:0!important}.border-end{border-right:var(--bs-border-width) var(--bs-border-style) var(--bs-border-color)!important}.border-end-0{border-right:0!important}.border-bottom{border-bottom:var(--bs-border-width) var(--bs-border-style) var(--bs-border-color)!important}.border-bottom-0{border-bottom:0!important}.border-start{border-left:var(--bs-border-width) var(--bs-border-style) var(--bs-border-color)!important}.border-start-0{border-left:0!important}.border-primary{--bs-border-opacity:1;border-color:rgba(var(--bs-primary-rgb),var(--bs-border-opacity))!important}.border-secondary{--bs-border-opacity:1;border-color:rgba(var(--bs-secondary-rgb),var(--bs-border-opacity))!important}.border-success{--bs-border-opacity:1;border-color:rgba(var(--bs-success-rgb),var(--bs-border-opacity))!important}.border-info{--bs-border-opacity:1;border-color:rgba(var(--bs-info-rgb),var(--bs-border-opacity))!important}.border-warning{--bs-border-opacity:1;border-color:rgba(var(--bs-warning-rgb),var(--bs-border-opacity))!important}.border-danger{--bs-border-opacity:1;border-color:rgba(var(--bs-danger-rgb),var(--bs-border-opacity))!important}.border-light{--bs-border-opacity:1;border-color:rgba(var(--bs-light-rgb),var(--bs-border-opacity))!important}.border-dark{--bs-border-opacity:1;border-color:rgba(var(--bs-dark-rgb),var(--bs-border-opacity))!important}.border-black{--bs-border-opacity:1;border-color:rgba(var(--bs-black-rgb),var(--bs-border-opacity))!important}.border-white{--bs-border-opacity:1;border-color:rgba(var(--bs-white-rgb),var(--bs-border-opacity))!important}.border-primary-subtle{border-color:var(--bs-primary-border-subtle)!important}.border-secondary-subtle{border-color:var(--bs-secondary-border-subtle)!important}.border-success-subtle{border-color:var(--bs-success-border-subtle)!important}.border-info-subtle{border-color:var(--bs-info-border-subtle)!important}.border-warning-subtle{border-color:var(--bs-warning-border-subtle)!important}.border-danger-subtle{border-color:var(--bs-danger-border-subtle)!important}.border-light-subtle{border-color:var(--bs-light-border-subtle)!important}.border-dark-subtle{border-color:var(--bs-dark-border-subtle)!important}.border-1{border-width:1px!important}.border-2{border-width:2px!important}.border-3{border-width:3px!important}.border-4{border-width:4px!important}.border-5{border-width:5px!important}.border-opacity-10{--bs-border-opacity:0.1}.border-opacity-25{--bs-border-opacity:0.25}.border-opacity-50{--bs-border-opacity:0.5}.border-opacity-75{--bs-border-opacity:0.75}.border-opacity-100{--bs-border-opacity:1}.w-25{width:25%!important}.w-50{width:50%!important}.w-75{width:75%!important}.w-100{width:100%!important}.w-auto{width:auto!important}.mw-100{max-width:100%!important}.vw-100{width:100vw!important}.min-vw-100{min-width:100vw!important}.h-25{height:25%!important}.h-50{height:50%!important}.h-75{height:75%!important}.h-100{height:100%!important}.h-auto{height:auto!important}.mh-100{max-height:100%!important}.vh-100{height:100vh!important}.min-vh-100{min-height:100vh!important}.flex-fill{flex:1 1 auto!important}.flex-row{flex-direction:row!important}.flex-column{flex-direction:column!important}.flex-row-reverse{flex-direction:row-reverse!important}.flex-column-reverse{flex-direction:column-reverse!important}.flex-grow-0{flex-grow:0!important}.flex-grow-1{flex-grow:1!important}.flex-shrink-0{flex-shrink:0!important}.flex-shrink-1{flex-shrink:1!important}.flex-wrap{flex-wrap:wrap!important}.flex-nowrap{flex-wrap:nowrap!important}.flex-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-start{justify-content:flex-start!important}.justify-content-end{justify-content:flex-end!important}.justify-content-center{justify-content:center!important}.justify-content-between{justify-content:space-between!important}.justify-content-around{justify-content:space-around!important}.justify-content-evenly{justify-content:space-evenly!important}.align-items-start{align-items:flex-start!important}.align-items-end{align-items:flex-end!important}.align-items-center{align-items:center!important}.align-items-baseline{align-items:baseline!important}.align-items-stretch{align-items:stretch!important}.align-content-start{align-content:flex-start!important}.align-content-end{align-content:flex-end!important}.align-content-center{align-content:center!important}.align-content-between{align-content:space-between!important}.align-content-around{align-content:space-around!important}.align-content-stretch{align-content:stretch!important}.align-self-auto{align-self:auto!important}.align-self-start{align-self:flex-start!important}.align-self-end{align-self:flex-end!important}.align-self-center{align-self:center!important}.align-self-baseline{align-self:baseline!important}.align-self-stretch{align-self:stretch!important}.order-first{order:-1!important}.order-0{order:0!important}.order-1{order:1!important}.order-2{order:2!important}.order-3{order:3!important}.order-4{order:4!important}.order-5{order:5!important}.order-last{order:6!important}.m-0{margin:0!important}.m-1{margin:.25rem!important}.m-2{margin:.5rem!important}.m-3{margin:1rem!important}.m-4{margin:1.5rem!important}.m-5{margin:3rem!important}.m-auto{margin:auto!important}.mx-0{margin-right:0!important;margin-left:0!important}.mx-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-3{margin-right:1rem!important;margin-left:1rem!important}.mx-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-5{margin-right:3rem!important;margin-left:3rem!important}.mx-auto{margin-right:auto!important;margin-left:auto!important}.my-0{margin-top:0!important;margin-bottom:0!important}.my-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-0{margin-top:0!important}.mt-1{margin-top:.25rem!important}.mt-2{margin-top:.5rem!important}.mt-3{margin-top:1rem!important}.mt-4{margin-top:1.5rem!important}.mt-5{margin-top:3rem!important}.mt-auto{margin-top:auto!important}.me-0{margin-right:0!important}.me-1{margin-right:.25rem!important}.me-2{margin-right:.5rem!important}.me-3{margin-right:1rem!important}.me-4{margin-right:1.5rem!important}.me-5{margin-right:3rem!important}.me-auto{margin-right:auto!important}.mb-0{margin-bottom:0!important}.mb-1{margin-bottom:.25rem!important}.mb-2{margin-bottom:.5rem!important}.mb-3{margin-bottom:1rem!important}.mb-4{margin-bottom:1.5rem!important}.mb-5{margin-bottom:3rem!important}.mb-auto{margin-bottom:auto!important}.ms-0{margin-left:0!important}.ms-1{margin-left:.25rem!important}.ms-2{margin-left:.5rem!important}.ms-3{margin-left:1rem!important}.ms-4{margin-left:1.5rem!important}.ms-5{margin-left:3rem!important}.ms-auto{margin-left:auto!important}.p-0{padding:0!important}.p-1{padding:.25rem!important}.p-2{padding:.5rem!important}.p-3{padding:1rem!important}.p-4{padding:1.5rem!important}.p-5{padding:3rem!important}.px-0{padding-right:0!important;padding-left:0!important}.px-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-3{padding-right:1rem!important;padding-left:1rem!important}.px-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-5{padding-right:3rem!important;padding-left:3rem!important}.py-0{padding-top:0!important;padding-bottom:0!important}.py-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-0{padding-top:0!important}.pt-1{padding-top:.25rem!important}.pt-2{padding-top:.5rem!important}.pt-3{padding-top:1rem!important}.pt-4{padding-top:1.5rem!important}.pt-5{padding-top:3rem!important}.pe-0{padding-right:0!important}.pe-1{padding-right:.25rem!important}.pe-2{padding-right:.5rem!important}.pe-3{padding-right:1rem!important}.pe-4{padding-right:1.5rem!important}.pe-5{padding-right:3rem!important}.pb-0{padding-bottom:0!important}.pb-1{padding-bottom:.25rem!important}.pb-2{padding-bottom:.5rem!important}.pb-3{padding-bottom:1rem!important}.pb-4{padding-bottom:1.5rem!important}.pb-5{padding-bottom:3rem!important}.ps-0{padding-left:0!important}.ps-1{padding-left:.25rem!important}.ps-2{padding-left:.5rem!important}.ps-3{padding-left:1rem!important}.ps-4{padding-left:1.5rem!important}.ps-5{padding-left:3rem!important}.gap-0{gap:0!important}.gap-1{gap:.25rem!important}.gap-2{gap:.5rem!important}.gap-3{gap:1rem!important}.gap-4{gap:1.5rem!important}.gap-5{gap:3rem!important}.row-gap-0{row-gap:0!important}.row-gap-1{row-gap:.25rem!important}.row-gap-2{row-gap:.5rem!important}.row-gap-3{row-gap:1rem!important}.row-gap-4{row-gap:1.5rem!important}.row-gap-5{row-gap:3rem!important}.column-gap-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.font-monospace{font-family:var(--bs-font-monospace)!important}.fs-1{font-size:calc(1.375rem + 1.5vw)!important}.fs-2{font-size:calc(1.325rem + .9vw)!important}.fs-3{font-size:calc(1.3rem + .6vw)!important}.fs-4{font-size:calc(1.275rem + .3vw)!important}.fs-5{font-size:1.25rem!important}.fs-6{font-size:1rem!important}.fst-italic{font-style:italic!important}.fst-normal{font-style:normal!important}.fw-lighter{font-weight:lighter!important}.fw-light{font-weight:300!important}.fw-normal{font-weight:400!important}.fw-medium{font-weight:500!important}.fw-semibold{font-weight:600!important}.fw-bold{font-weight:700!important}.fw-bolder{font-weight:bolder!important}.lh-1{line-height:1!important}.lh-sm{line-height:1.25!important}.lh-base{line-height:1.5!important}.lh-lg{line-height:2!important}.text-start{text-align:left!important}.text-end{text-align:right!important}.text-center{text-align:center!important}.text-decoration-none{text-decoration:none!important}.text-decoration-underline{text-decoration:underline!important}.text-decoration-line-through{text-decoration:line-through!important}.text-lowercase{text-transform:lowercase!important}.text-uppercase{text-transform:uppercase!important}.text-capitalize{text-transform:capitalize!important}.text-wrap{white-space:normal!important}.text-nowrap{white-space:nowrap!important}.text-break{word-wrap:break-word!important;word-break:break-word!important}.text-primary{--bs-text-opacity:1;color:rgba(var(--bs-primary-rgb),var(--bs-text-opacity))!important}.text-secondary{--bs-text-opacity:1;color:rgba(var(--bs-secondary-rgb),var(--bs-text-opacity))!important}.text-success{--bs-text-opacity:1;color:rgba(var(--bs-success-rgb),var(--bs-text-opacity))!important}.text-info{--bs-text-opacity:1;color:rgba(var(--bs-info-rgb),var(--bs-text-opacity))!important}.text-warning{--bs-text-opacity:1;color:rgba(var(--bs-warning-rgb),var(--bs-text-opacity))!important}.text-danger{--bs-text-opacity:1;color:rgba(var(--bs-danger-rgb),var(--bs-text-opacity))!important}.text-light{--bs-text-opacity:1;color:rgba(var(--bs-light-rgb),var(--bs-text-opacity))!important}.text-dark{--bs-text-opacity:1;color:rgba(var(--bs-dark-rgb),var(--bs-text-opacity))!important}.text-black{--bs-text-opacity:1;color:rgba(var(--bs-black-rgb),var(--bs-text-opacity))!important}.text-white{--bs-text-opacity:1;color:rgba(var(--bs-white-rgb),var(--bs-text-opacity))!important}.text-body{--bs-text-opacity:1;color:rgba(var(--bs-body-color-rgb),var(--bs-text-opacity))!important}.text-muted{--bs-text-opacity:1;color:var(--bs-secondary-color)!important}.text-black-50{--bs-text-opacity:1;color:rgba(0,0,0,.5)!important}.text-white-50{--bs-text-opacity:1;color:rgba(255,255,255,.5)!important}.text-body-secondary{--bs-text-opacity:1;color:var(--bs-secondary-color)!important}.text-body-tertiary{--bs-text-opacity:1;color:var(--bs-tertiary-color)!important}.text-body-emphasis{--bs-text-opacity:1;color:var(--bs-emphasis-color)!important}.text-reset{--bs-text-opacity:1;color:inherit!important}.text-opacity-25{--bs-text-opacity:0.25}.text-opacity-50{--bs-text-opacity:0.5}.text-opacity-75{--bs-text-opacity:0.75}.text-opacity-100{--bs-text-opacity:1}.text-primary-emphasis{color:var(--bs-primary-text-emphasis)!important}.text-secondary-emphasis{color:var(--bs-secondary-text-emphasis)!important}.text-success-emphasis{color:var(--bs-success-text-emphasis)!important}.text-info-emphasis{color:var(--bs-info-text-emphasis)!important}.text-warning-emphasis{color:var(--bs-warning-text-emphasis)!important}.text-danger-emphasis{color:var(--bs-danger-text-emphasis)!important}.text-light-emphasis{color:var(--bs-light-text-emphasis)!important}.text-dark-emphasis{color:var(--bs-dark-text-emphasis)!important}.link-opacity-10{--bs-link-opacity:0.1}.link-opacity-10-hover:hover{--bs-link-opacity:0.1}.link-opacity-25{--bs-link-opacity:0.25}.link-opacity-25-hover:hover{--bs-link-opacity:0.25}.link-opacity-50{--bs-link-opacity:0.5}.link-opacity-50-hover:hover{--bs-link-opacity:0.5}.link-opacity-75{--bs-link-opacity:0.75}.link-opacity-75-hover:hover{--bs-link-opacity:0.75}.link-opacity-100{--bs-link-opacity:1}.link-opacity-100-hover:hover{--bs-link-opacity:1}.link-offset-1{text-underline-offset:0.125em!important}.link-offset-1-hover:hover{text-underline-offset:0.125em!important}.link-offset-2{text-underline-offset:0.25em!important}.link-offset-2-hover:hover{text-underline-offset:0.25em!important}.link-offset-3{text-underline-offset:0.375em!important}.link-offset-3-hover:hover{text-underline-offset:0.375em!important}.link-underline-primary{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-primary-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-primary-rgb),var(--bs-link-underline-opacity))!important}.link-underline-secondary{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-secondary-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-secondary-rgb),var(--bs-link-underline-opacity))!important}.link-underline-success{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-success-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-success-rgb),var(--bs-link-underline-opacity))!important}.link-underline-info{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-info-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-info-rgb),var(--bs-link-underline-opacity))!important}.link-underline-warning{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-warning-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-warning-rgb),var(--bs-link-underline-opacity))!important}.link-underline-danger{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-danger-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-danger-rgb),var(--bs-link-underline-opacity))!important}.link-underline-light{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-light-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-light-rgb),var(--bs-link-underline-opacity))!important}.link-underline-dark{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-dark-rgb),var(--bs-link-underline-opacity))!important;text-decoration-color:rgba(var(--bs-dark-rgb),var(--bs-link-underline-opacity))!important}.link-underline{--bs-link-underline-opacity:1;-webkit-text-decoration-color:rgba(var(--bs-link-color-rgb),var(--bs-link-underline-opacity,1))!important;text-decoration-color:rgba(var(--bs-link-color-rgb),var(--bs-link-underline-opacity,1))!important}.link-underline-opacity-0{--bs-link-underline-opacity:0}.link-underline-opacity-0-hover:hover{--bs-link-underline-opacity:0}.link-underline-opacity-10{--bs-link-underline-opacity:0.1}.link-underline-opacity-10-hover:hover{--bs-link-underline-opacity:0.1}.link-underline-opacity-25{--bs-link-underline-opacity:0.25}.link-underline-opacity-25-hover:hover{--bs-link-underline-opacity:0.25}.link-underline-opacity-50{--bs-link-underline-opacity:0.5}.link-underline-opacity-50-hover:hover{--bs-link-underline-opacity:0.5}.link-underline-opacity-75{--bs-link-underline-opacity:0.75}.link-underline-opacity-75-hover:hover{--bs-link-underline-opacity:0.75}.link-underline-opacity-100{--bs-link-underline-opacity:1}.link-underline-opacity-100-hover:hover{--bs-link-underline-opacity:1}.bg-primary{--bs-bg-opacity:1;background-color:rgba(var(--bs-primary-rgb),var(--bs-bg-opacity))!important}.bg-secondary{--bs-bg-opacity:1;background-color:rgba(var(--bs-secondary-rgb),var(--bs-bg-opacity))!important}.bg-success{--bs-bg-opacity:1;background-color:rgba(var(--bs-success-rgb),var(--bs-bg-opacity))!important}.bg-info{--bs-bg-opacity:1;background-color:rgba(var(--bs-info-rgb),var(--bs-bg-opacity))!important}.bg-warning{--bs-bg-opacity:1;background-color:rgba(var(--bs-warning-rgb),var(--bs-bg-opacity))!important}.bg-danger{--bs-bg-opacity:1;background-color:rgba(var(--bs-danger-rgb),var(--bs-bg-opacity))!important}.bg-light{--bs-bg-opacity:1;background-color:rgba(var(--bs-light-rgb),var(--bs-bg-opacity))!important}.bg-dark{--bs-bg-opacity:1;background-color:rgba(var(--bs-dark-rgb),var(--bs-bg-opacity))!important}.bg-black{--bs-bg-opacity:1;background-color:rgba(var(--bs-black-rgb),var(--bs-bg-opacity))!important}.bg-white{--bs-bg-opacity:1;background-color:rgba(var(--bs-white-rgb),var(--bs-bg-opacity))!important}.bg-body{--bs-bg-opacity:1;background-color:rgba(var(--bs-body-bg-rgb),var(--bs-bg-opacity))!important}.bg-transparent{--bs-bg-opacity:1;background-color:transparent!important}.bg-body-secondary{--bs-bg-opacity:1;background-color:rgba(var(--bs-secondary-bg-rgb),var(--bs-bg-opacity))!important}.bg-body-tertiary{--bs-bg-opacity:1;background-color:rgba(var(--bs-tertiary-bg-rgb),var(--bs-bg-opacity))!important}.bg-opacity-10{--bs-bg-opacity:0.1}.bg-opacity-25{--bs-bg-opacity:0.25}.bg-opacity-50{--bs-bg-opacity:0.5}.bg-opacity-75{--bs-bg-opacity:0.75}.bg-opacity-100{--bs-bg-opacity:1}.bg-primary-subtle{background-color:var(--bs-primary-bg-subtle)!important}.bg-secondary-subtle{background-color:var(--bs-secondary-bg-subtle)!important}.bg-success-subtle{background-color:var(--bs-success-bg-subtle)!important}.bg-info-subtle{background-color:var(--bs-info-bg-subtle)!important}.bg-warning-subtle{background-color:var(--bs-warning-bg-subtle)!important}.bg-danger-subtle{background-color:var(--bs-danger-bg-subtle)!important}.bg-light-subtle{background-color:var(--bs-light-bg-subtle)!important}.bg-dark-subtle{background-color:var(--bs-dark-bg-subtle)!important}.bg-gradient{background-image:var(--bs-gradient)!important}.user-select-all{-webkit-user-select:all!important;-moz-user-select:all!important;user-select:all!important}.user-select-auto{-webkit-user-select:auto!important;-moz-user-select:auto!important;user-select:auto!important}.user-select-none{-webkit-user-select:none!important;-moz-user-select:none!important;user-select:none!important}.pe-none{pointer-events:none!important}.pe-auto{pointer-events:auto!important}.rounded{border-radius:var(--bs-border-radius)!important}.rounded-0{border-radius:0!important}.rounded-1{border-radius:var(--bs-border-radius-sm)!important}.rounded-2{border-radius:var(--bs-border-radius)!important}.rounded-3{border-radius:var(--bs-border-radius-lg)!important}.rounded-4{border-radius:var(--bs-border-radius-xl)!important}.rounded-5{border-radius:var(--bs-border-radius-xxl)!important}.rounded-circle{border-radius:50%!important}.rounded-pill{border-radius:var(--bs-border-radius-pill)!important}.rounded-top{border-top-left-radius:var(--bs-border-radius)!important;border-top-right-radius:var(--bs-border-radius)!important}.rounded-top-0{border-top-left-radius:0!important;border-top-right-radius:0!important}.rounded-top-1{border-top-left-radius:var(--bs-border-radius-sm)!important;border-top-right-radius:var(--bs-border-radius-sm)!important}.rounded-top-2{border-top-left-radius:var(--bs-border-radius)!important;border-top-right-radius:var(--bs-border-radius)!important}.rounded-top-3{border-top-left-radius:var(--bs-border-radius-lg)!important;border-top-right-radius:var(--bs-border-radius-lg)!important}.rounded-top-4{border-top-left-radius:var(--bs-border-radius-xl)!important;border-top-right-radius:var(--bs-border-radius-xl)!important}.rounded-top-5{border-top-left-radius:var(--bs-border-radius-xxl)!important;border-top-right-radius:var(--bs-border-radius-xxl)!important}.rounded-top-circle{border-top-left-radius:50%!important;border-top-right-radius:50%!important}.rounded-top-pill{border-top-left-radius:var(--bs-border-radius-pill)!important;border-top-right-radius:var(--bs-border-radius-pill)!important}.rounded-end{border-top-right-radius:var(--bs-border-radius)!important;border-bottom-right-radius:var(--bs-border-radius)!important}.rounded-end-0{border-top-right-radius:0!important;border-bottom-right-radius:0!important}.rounded-end-1{border-top-right-radius:var(--bs-border-radius-sm)!important;border-bottom-right-radius:var(--bs-border-radius-sm)!important}.rounded-end-2{border-top-right-radius:var(--bs-border-radius)!important;border-bottom-right-radius:var(--bs-border-radius)!important}.rounded-end-3{border-top-right-radius:var(--bs-border-radius-lg)!important;border-bottom-right-radius:var(--bs-border-radius-lg)!important}.rounded-end-4{border-top-right-radius:var(--bs-border-radius-xl)!important;border-bottom-right-radius:var(--bs-border-radius-xl)!important}.rounded-end-5{border-top-right-radius:var(--bs-border-radius-xxl)!important;border-bottom-right-radius:var(--bs-border-radius-xxl)!important}.rounded-end-circle{border-top-right-radius:50%!important;border-bottom-right-radius:50%!important}.rounded-end-pill{border-top-right-radius:var(--bs-border-radius-pill)!important;border-bottom-right-radius:var(--bs-border-radius-pill)!important}.rounded-bottom{border-bottom-right-radius:var(--bs-border-radius)!important;border-bottom-left-radius:var(--bs-border-radius)!important}.rounded-bottom-0{border-bottom-right-radius:0!important;border-bottom-left-radius:0!important}.rounded-bottom-1{border-bottom-right-radius:var(--bs-border-radius-sm)!important;border-bottom-left-radius:var(--bs-border-radius-sm)!important}.rounded-bottom-2{border-bottom-right-radius:var(--bs-border-radius)!important;border-bottom-left-radius:var(--bs-border-radius)!important}.rounded-bottom-3{border-bottom-right-radius:var(--bs-border-radius-lg)!important;border-bottom-left-radius:var(--bs-border-radius-lg)!important}.rounded-bottom-4{border-bottom-right-radius:var(--bs-border-radius-xl)!important;border-bottom-left-radius:var(--bs-border-radius-xl)!important}.rounded-bottom-5{border-bottom-right-radius:var(--bs-border-radius-xxl)!important;border-bottom-left-radius:var(--bs-border-radius-xxl)!important}.rounded-bottom-circle{border-bottom-right-radius:50%!important;border-bottom-left-radius:50%!important}.rounded-bottom-pill{border-bottom-right-radius:var(--bs-border-radius-pill)!important;border-bottom-left-radius:var(--bs-border-radius-pill)!important}.rounded-start{border-bottom-left-radius:var(--bs-border-radius)!important;border-top-left-radius:var(--bs-border-radius)!important}.rounded-start-0{border-bottom-left-radius:0!important;border-top-left-radius:0!important}.rounded-start-1{border-bottom-left-radius:var(--bs-border-radius-sm)!important;border-top-left-radius:var(--bs-border-radius-sm)!important}.rounded-start-2{border-bottom-left-radius:var(--bs-border-radius)!important;border-top-left-radius:var(--bs-border-radius)!important}.rounded-start-3{border-bottom-left-radius:var(--bs-border-radius-lg)!important;border-top-left-radius:var(--bs-border-radius-lg)!important}.rounded-start-4{border-bottom-left-radius:var(--bs-border-radius-xl)!important;border-top-left-radius:var(--bs-border-radius-xl)!important}.rounded-start-5{border-bottom-left-radius:var(--bs-border-radius-xxl)!important;border-top-left-radius:var(--bs-border-radius-xxl)!important}.rounded-start-circle{border-bottom-left-radius:50%!important;border-top-left-radius:50%!important}.rounded-start-pill{border-bottom-left-radius:var(--bs-border-radius-pill)!important;border-top-left-radius:var(--bs-border-radius-pill)!important}.visible{visibility:visible!important}.invisible{visibility:hidden!important}.z-n1{z-index:-1!important}.z-0{z-index:0!important}.z-1{z-index:1!important}.z-2{z-index:2!important}.z-3{z-index:3!important}@media (min-width:576px){.float-sm-start{float:left!important}.float-sm-end{float:right!important}.float-sm-none{float:none!important}.object-fit-sm-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-sm-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-sm-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-sm-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-sm-none{-o-object-fit:none!important;object-fit:none!important}.d-sm-inline{display:inline!important}.d-sm-inline-block{display:inline-block!important}.d-sm-block{display:block!important}.d-sm-grid{display:grid!important}.d-sm-inline-grid{display:inline-grid!important}.d-sm-table{display:table!important}.d-sm-table-row{display:table-row!important}.d-sm-table-cell{display:table-cell!important}.d-sm-flex{display:flex!important}.d-sm-inline-flex{display:inline-flex!important}.d-sm-none{display:none!important}.flex-sm-fill{flex:1 1 auto!important}.flex-sm-row{flex-direction:row!important}.flex-sm-column{flex-direction:column!important}.flex-sm-row-reverse{flex-direction:row-reverse!important}.flex-sm-column-reverse{flex-direction:column-reverse!important}.flex-sm-grow-0{flex-grow:0!important}.flex-sm-grow-1{flex-grow:1!important}.flex-sm-shrink-0{flex-shrink:0!important}.flex-sm-shrink-1{flex-shrink:1!important}.flex-sm-wrap{flex-wrap:wrap!important}.flex-sm-nowrap{flex-wrap:nowrap!important}.flex-sm-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-sm-start{justify-content:flex-start!important}.justify-content-sm-end{justify-content:flex-end!important}.justify-content-sm-center{justify-content:center!important}.justify-content-sm-between{justify-content:space-between!important}.justify-content-sm-around{justify-content:space-around!important}.justify-content-sm-evenly{justify-content:space-evenly!important}.align-items-sm-start{align-items:flex-start!important}.align-items-sm-end{align-items:flex-end!important}.align-items-sm-center{align-items:center!important}.align-items-sm-baseline{align-items:baseline!important}.align-items-sm-stretch{align-items:stretch!important}.align-content-sm-start{align-content:flex-start!important}.align-content-sm-end{align-content:flex-end!important}.align-content-sm-center{align-content:center!important}.align-content-sm-between{align-content:space-between!important}.align-content-sm-around{align-content:space-around!important}.align-content-sm-stretch{align-content:stretch!important}.align-self-sm-auto{align-self:auto!important}.align-self-sm-start{align-self:flex-start!important}.align-self-sm-end{align-self:flex-end!important}.align-self-sm-center{align-self:center!important}.align-self-sm-baseline{align-self:baseline!important}.align-self-sm-stretch{align-self:stretch!important}.order-sm-first{order:-1!important}.order-sm-0{order:0!important}.order-sm-1{order:1!important}.order-sm-2{order:2!important}.order-sm-3{order:3!important}.order-sm-4{order:4!important}.order-sm-5{order:5!important}.order-sm-last{order:6!important}.m-sm-0{margin:0!important}.m-sm-1{margin:.25rem!important}.m-sm-2{margin:.5rem!important}.m-sm-3{margin:1rem!important}.m-sm-4{margin:1.5rem!important}.m-sm-5{margin:3rem!important}.m-sm-auto{margin:auto!important}.mx-sm-0{margin-right:0!important;margin-left:0!important}.mx-sm-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-sm-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-sm-3{margin-right:1rem!important;margin-left:1rem!important}.mx-sm-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-sm-5{margin-right:3rem!important;margin-left:3rem!important}.mx-sm-auto{margin-right:auto!important;margin-left:auto!important}.my-sm-0{margin-top:0!important;margin-bottom:0!important}.my-sm-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-sm-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-sm-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-sm-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-sm-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-sm-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-sm-0{margin-top:0!important}.mt-sm-1{margin-top:.25rem!important}.mt-sm-2{margin-top:.5rem!important}.mt-sm-3{margin-top:1rem!important}.mt-sm-4{margin-top:1.5rem!important}.mt-sm-5{margin-top:3rem!important}.mt-sm-auto{margin-top:auto!important}.me-sm-0{margin-right:0!important}.me-sm-1{margin-right:.25rem!important}.me-sm-2{margin-right:.5rem!important}.me-sm-3{margin-right:1rem!important}.me-sm-4{margin-right:1.5rem!important}.me-sm-5{margin-right:3rem!important}.me-sm-auto{margin-right:auto!important}.mb-sm-0{margin-bottom:0!important}.mb-sm-1{margin-bottom:.25rem!important}.mb-sm-2{margin-bottom:.5rem!important}.mb-sm-3{margin-bottom:1rem!important}.mb-sm-4{margin-bottom:1.5rem!important}.mb-sm-5{margin-bottom:3rem!important}.mb-sm-auto{margin-bottom:auto!important}.ms-sm-0{margin-left:0!important}.ms-sm-1{margin-left:.25rem!important}.ms-sm-2{margin-left:.5rem!important}.ms-sm-3{margin-left:1rem!important}.ms-sm-4{margin-left:1.5rem!important}.ms-sm-5{margin-left:3rem!important}.ms-sm-auto{margin-left:auto!important}.p-sm-0{padding:0!important}.p-sm-1{padding:.25rem!important}.p-sm-2{padding:.5rem!important}.p-sm-3{padding:1rem!important}.p-sm-4{padding:1.5rem!important}.p-sm-5{padding:3rem!important}.px-sm-0{padding-right:0!important;padding-left:0!important}.px-sm-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-sm-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-sm-3{padding-right:1rem!important;padding-left:1rem!important}.px-sm-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-sm-5{padding-right:3rem!important;padding-left:3rem!important}.py-sm-0{padding-top:0!important;padding-bottom:0!important}.py-sm-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-sm-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-sm-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-sm-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-sm-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-sm-0{padding-top:0!important}.pt-sm-1{padding-top:.25rem!important}.pt-sm-2{padding-top:.5rem!important}.pt-sm-3{padding-top:1rem!important}.pt-sm-4{padding-top:1.5rem!important}.pt-sm-5{padding-top:3rem!important}.pe-sm-0{padding-right:0!important}.pe-sm-1{padding-right:.25rem!important}.pe-sm-2{padding-right:.5rem!important}.pe-sm-3{padding-right:1rem!important}.pe-sm-4{padding-right:1.5rem!important}.pe-sm-5{padding-right:3rem!important}.pb-sm-0{padding-bottom:0!important}.pb-sm-1{padding-bottom:.25rem!important}.pb-sm-2{padding-bottom:.5rem!important}.pb-sm-3{padding-bottom:1rem!important}.pb-sm-4{padding-bottom:1.5rem!important}.pb-sm-5{padding-bottom:3rem!important}.ps-sm-0{padding-left:0!important}.ps-sm-1{padding-left:.25rem!important}.ps-sm-2{padding-left:.5rem!important}.ps-sm-3{padding-left:1rem!important}.ps-sm-4{padding-left:1.5rem!important}.ps-sm-5{padding-left:3rem!important}.gap-sm-0{gap:0!important}.gap-sm-1{gap:.25rem!important}.gap-sm-2{gap:.5rem!important}.gap-sm-3{gap:1rem!important}.gap-sm-4{gap:1.5rem!important}.gap-sm-5{gap:3rem!important}.row-gap-sm-0{row-gap:0!important}.row-gap-sm-1{row-gap:.25rem!important}.row-gap-sm-2{row-gap:.5rem!important}.row-gap-sm-3{row-gap:1rem!important}.row-gap-sm-4{row-gap:1.5rem!important}.row-gap-sm-5{row-gap:3rem!important}.column-gap-sm-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-sm-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-sm-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-sm-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-sm-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-sm-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.text-sm-start{text-align:left!important}.text-sm-end{text-align:right!important}.text-sm-center{text-align:center!important}}@media (min-width:768px){.float-md-start{float:left!important}.float-md-end{float:right!important}.float-md-none{float:none!important}.object-fit-md-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-md-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-md-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-md-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-md-none{-o-object-fit:none!important;object-fit:none!important}.d-md-inline{display:inline!important}.d-md-inline-block{display:inline-block!important}.d-md-block{display:block!important}.d-md-grid{display:grid!important}.d-md-inline-grid{display:inline-grid!important}.d-md-table{display:table!important}.d-md-table-row{display:table-row!important}.d-md-table-cell{display:table-cell!important}.d-md-flex{display:flex!important}.d-md-inline-flex{display:inline-flex!important}.d-md-none{display:none!important}.flex-md-fill{flex:1 1 auto!important}.flex-md-row{flex-direction:row!important}.flex-md-column{flex-direction:column!important}.flex-md-row-reverse{flex-direction:row-reverse!important}.flex-md-column-reverse{flex-direction:column-reverse!important}.flex-md-grow-0{flex-grow:0!important}.flex-md-grow-1{flex-grow:1!important}.flex-md-shrink-0{flex-shrink:0!important}.flex-md-shrink-1{flex-shrink:1!important}.flex-md-wrap{flex-wrap:wrap!important}.flex-md-nowrap{flex-wrap:nowrap!important}.flex-md-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-md-start{justify-content:flex-start!important}.justify-content-md-end{justify-content:flex-end!important}.justify-content-md-center{justify-content:center!important}.justify-content-md-between{justify-content:space-between!important}.justify-content-md-around{justify-content:space-around!important}.justify-content-md-evenly{justify-content:space-evenly!important}.align-items-md-start{align-items:flex-start!important}.align-items-md-end{align-items:flex-end!important}.align-items-md-center{align-items:center!important}.align-items-md-baseline{align-items:baseline!important}.align-items-md-stretch{align-items:stretch!important}.align-content-md-start{align-content:flex-start!important}.align-content-md-end{align-content:flex-end!important}.align-content-md-center{align-content:center!important}.align-content-md-between{align-content:space-between!important}.align-content-md-around{align-content:space-around!important}.align-content-md-stretch{align-content:stretch!important}.align-self-md-auto{align-self:auto!important}.align-self-md-start{align-self:flex-start!important}.align-self-md-end{align-self:flex-end!important}.align-self-md-center{align-self:center!important}.align-self-md-baseline{align-self:baseline!important}.align-self-md-stretch{align-self:stretch!important}.order-md-first{order:-1!important}.order-md-0{order:0!important}.order-md-1{order:1!important}.order-md-2{order:2!important}.order-md-3{order:3!important}.order-md-4{order:4!important}.order-md-5{order:5!important}.order-md-last{order:6!important}.m-md-0{margin:0!important}.m-md-1{margin:.25rem!important}.m-md-2{margin:.5rem!important}.m-md-3{margin:1rem!important}.m-md-4{margin:1.5rem!important}.m-md-5{margin:3rem!important}.m-md-auto{margin:auto!important}.mx-md-0{margin-right:0!important;margin-left:0!important}.mx-md-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-md-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-md-3{margin-right:1rem!important;margin-left:1rem!important}.mx-md-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-md-5{margin-right:3rem!important;margin-left:3rem!important}.mx-md-auto{margin-right:auto!important;margin-left:auto!important}.my-md-0{margin-top:0!important;margin-bottom:0!important}.my-md-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-md-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-md-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-md-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-md-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-md-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-md-0{margin-top:0!important}.mt-md-1{margin-top:.25rem!important}.mt-md-2{margin-top:.5rem!important}.mt-md-3{margin-top:1rem!important}.mt-md-4{margin-top:1.5rem!important}.mt-md-5{margin-top:3rem!important}.mt-md-auto{margin-top:auto!important}.me-md-0{margin-right:0!important}.me-md-1{margin-right:.25rem!important}.me-md-2{margin-right:.5rem!important}.me-md-3{margin-right:1rem!important}.me-md-4{margin-right:1.5rem!important}.me-md-5{margin-right:3rem!important}.me-md-auto{margin-right:auto!important}.mb-md-0{margin-bottom:0!important}.mb-md-1{margin-bottom:.25rem!important}.mb-md-2{margin-bottom:.5rem!important}.mb-md-3{margin-bottom:1rem!important}.mb-md-4{margin-bottom:1.5rem!important}.mb-md-5{margin-bottom:3rem!important}.mb-md-auto{margin-bottom:auto!important}.ms-md-0{margin-left:0!important}.ms-md-1{margin-left:.25rem!important}.ms-md-2{margin-left:.5rem!important}.ms-md-3{margin-left:1rem!important}.ms-md-4{margin-left:1.5rem!important}.ms-md-5{margin-left:3rem!important}.ms-md-auto{margin-left:auto!important}.p-md-0{padding:0!important}.p-md-1{padding:.25rem!important}.p-md-2{padding:.5rem!important}.p-md-3{padding:1rem!important}.p-md-4{padding:1.5rem!important}.p-md-5{padding:3rem!important}.px-md-0{padding-right:0!important;padding-left:0!important}.px-md-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-md-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-md-3{padding-right:1rem!important;padding-left:1rem!important}.px-md-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-md-5{padding-right:3rem!important;padding-left:3rem!important}.py-md-0{padding-top:0!important;padding-bottom:0!important}.py-md-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-md-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-md-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-md-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-md-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-md-0{padding-top:0!important}.pt-md-1{padding-top:.25rem!important}.pt-md-2{padding-top:.5rem!important}.pt-md-3{padding-top:1rem!important}.pt-md-4{padding-top:1.5rem!important}.pt-md-5{padding-top:3rem!important}.pe-md-0{padding-right:0!important}.pe-md-1{padding-right:.25rem!important}.pe-md-2{padding-right:.5rem!important}.pe-md-3{padding-right:1rem!important}.pe-md-4{padding-right:1.5rem!important}.pe-md-5{padding-right:3rem!important}.pb-md-0{padding-bottom:0!important}.pb-md-1{padding-bottom:.25rem!important}.pb-md-2{padding-bottom:.5rem!important}.pb-md-3{padding-bottom:1rem!important}.pb-md-4{padding-bottom:1.5rem!important}.pb-md-5{padding-bottom:3rem!important}.ps-md-0{padding-left:0!important}.ps-md-1{padding-left:.25rem!important}.ps-md-2{padding-left:.5rem!important}.ps-md-3{padding-left:1rem!important}.ps-md-4{padding-left:1.5rem!important}.ps-md-5{padding-left:3rem!important}.gap-md-0{gap:0!important}.gap-md-1{gap:.25rem!important}.gap-md-2{gap:.5rem!important}.gap-md-3{gap:1rem!important}.gap-md-4{gap:1.5rem!important}.gap-md-5{gap:3rem!important}.row-gap-md-0{row-gap:0!important}.row-gap-md-1{row-gap:.25rem!important}.row-gap-md-2{row-gap:.5rem!important}.row-gap-md-3{row-gap:1rem!important}.row-gap-md-4{row-gap:1.5rem!important}.row-gap-md-5{row-gap:3rem!important}.column-gap-md-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-md-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-md-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-md-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-md-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-md-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.text-md-start{text-align:left!important}.text-md-end{text-align:right!important}.text-md-center{text-align:center!important}}@media (min-width:992px){.float-lg-start{float:left!important}.float-lg-end{float:right!important}.float-lg-none{float:none!important}.object-fit-lg-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-lg-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-lg-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-lg-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-lg-none{-o-object-fit:none!important;object-fit:none!important}.d-lg-inline{display:inline!important}.d-lg-inline-block{display:inline-block!important}.d-lg-block{display:block!important}.d-lg-grid{display:grid!important}.d-lg-inline-grid{display:inline-grid!important}.d-lg-table{display:table!important}.d-lg-table-row{display:table-row!important}.d-lg-table-cell{display:table-cell!important}.d-lg-flex{display:flex!important}.d-lg-inline-flex{display:inline-flex!important}.d-lg-none{display:none!important}.flex-lg-fill{flex:1 1 auto!important}.flex-lg-row{flex-direction:row!important}.flex-lg-column{flex-direction:column!important}.flex-lg-row-reverse{flex-direction:row-reverse!important}.flex-lg-column-reverse{flex-direction:column-reverse!important}.flex-lg-grow-0{flex-grow:0!important}.flex-lg-grow-1{flex-grow:1!important}.flex-lg-shrink-0{flex-shrink:0!important}.flex-lg-shrink-1{flex-shrink:1!important}.flex-lg-wrap{flex-wrap:wrap!important}.flex-lg-nowrap{flex-wrap:nowrap!important}.flex-lg-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-lg-start{justify-content:flex-start!important}.justify-content-lg-end{justify-content:flex-end!important}.justify-content-lg-center{justify-content:center!important}.justify-content-lg-between{justify-content:space-between!important}.justify-content-lg-around{justify-content:space-around!important}.justify-content-lg-evenly{justify-content:space-evenly!important}.align-items-lg-start{align-items:flex-start!important}.align-items-lg-end{align-items:flex-end!important}.align-items-lg-center{align-items:center!important}.align-items-lg-baseline{align-items:baseline!important}.align-items-lg-stretch{align-items:stretch!important}.align-content-lg-start{align-content:flex-start!important}.align-content-lg-end{align-content:flex-end!important}.align-content-lg-center{align-content:center!important}.align-content-lg-between{align-content:space-between!important}.align-content-lg-around{align-content:space-around!important}.align-content-lg-stretch{align-content:stretch!important}.align-self-lg-auto{align-self:auto!important}.align-self-lg-start{align-self:flex-start!important}.align-self-lg-end{align-self:flex-end!important}.align-self-lg-center{align-self:center!important}.align-self-lg-baseline{align-self:baseline!important}.align-self-lg-stretch{align-self:stretch!important}.order-lg-first{order:-1!important}.order-lg-0{order:0!important}.order-lg-1{order:1!important}.order-lg-2{order:2!important}.order-lg-3{order:3!important}.order-lg-4{order:4!important}.order-lg-5{order:5!important}.order-lg-last{order:6!important}.m-lg-0{margin:0!important}.m-lg-1{margin:.25rem!important}.m-lg-2{margin:.5rem!important}.m-lg-3{margin:1rem!important}.m-lg-4{margin:1.5rem!important}.m-lg-5{margin:3rem!important}.m-lg-auto{margin:auto!important}.mx-lg-0{margin-right:0!important;margin-left:0!important}.mx-lg-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-lg-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-lg-3{margin-right:1rem!important;margin-left:1rem!important}.mx-lg-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-lg-5{margin-right:3rem!important;margin-left:3rem!important}.mx-lg-auto{margin-right:auto!important;margin-left:auto!important}.my-lg-0{margin-top:0!important;margin-bottom:0!important}.my-lg-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-lg-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-lg-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-lg-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-lg-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-lg-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-lg-0{margin-top:0!important}.mt-lg-1{margin-top:.25rem!important}.mt-lg-2{margin-top:.5rem!important}.mt-lg-3{margin-top:1rem!important}.mt-lg-4{margin-top:1.5rem!important}.mt-lg-5{margin-top:3rem!important}.mt-lg-auto{margin-top:auto!important}.me-lg-0{margin-right:0!important}.me-lg-1{margin-right:.25rem!important}.me-lg-2{margin-right:.5rem!important}.me-lg-3{margin-right:1rem!important}.me-lg-4{margin-right:1.5rem!important}.me-lg-5{margin-right:3rem!important}.me-lg-auto{margin-right:auto!important}.mb-lg-0{margin-bottom:0!important}.mb-lg-1{margin-bottom:.25rem!important}.mb-lg-2{margin-bottom:.5rem!important}.mb-lg-3{margin-bottom:1rem!important}.mb-lg-4{margin-bottom:1.5rem!important}.mb-lg-5{margin-bottom:3rem!important}.mb-lg-auto{margin-bottom:auto!important}.ms-lg-0{margin-left:0!important}.ms-lg-1{margin-left:.25rem!important}.ms-lg-2{margin-left:.5rem!important}.ms-lg-3{margin-left:1rem!important}.ms-lg-4{margin-left:1.5rem!important}.ms-lg-5{margin-left:3rem!important}.ms-lg-auto{margin-left:auto!important}.p-lg-0{padding:0!important}.p-lg-1{padding:.25rem!important}.p-lg-2{padding:.5rem!important}.p-lg-3{padding:1rem!important}.p-lg-4{padding:1.5rem!important}.p-lg-5{padding:3rem!important}.px-lg-0{padding-right:0!important;padding-left:0!important}.px-lg-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-lg-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-lg-3{padding-right:1rem!important;padding-left:1rem!important}.px-lg-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-lg-5{padding-right:3rem!important;padding-left:3rem!important}.py-lg-0{padding-top:0!important;padding-bottom:0!important}.py-lg-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-lg-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-lg-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-lg-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-lg-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-lg-0{padding-top:0!important}.pt-lg-1{padding-top:.25rem!important}.pt-lg-2{padding-top:.5rem!important}.pt-lg-3{padding-top:1rem!important}.pt-lg-4{padding-top:1.5rem!important}.pt-lg-5{padding-top:3rem!important}.pe-lg-0{padding-right:0!important}.pe-lg-1{padding-right:.25rem!important}.pe-lg-2{padding-right:.5rem!important}.pe-lg-3{padding-right:1rem!important}.pe-lg-4{padding-right:1.5rem!important}.pe-lg-5{padding-right:3rem!important}.pb-lg-0{padding-bottom:0!important}.pb-lg-1{padding-bottom:.25rem!important}.pb-lg-2{padding-bottom:.5rem!important}.pb-lg-3{padding-bottom:1rem!important}.pb-lg-4{padding-bottom:1.5rem!important}.pb-lg-5{padding-bottom:3rem!important}.ps-lg-0{padding-left:0!important}.ps-lg-1{padding-left:.25rem!important}.ps-lg-2{padding-left:.5rem!important}.ps-lg-3{padding-left:1rem!important}.ps-lg-4{padding-left:1.5rem!important}.ps-lg-5{padding-left:3rem!important}.gap-lg-0{gap:0!important}.gap-lg-1{gap:.25rem!important}.gap-lg-2{gap:.5rem!important}.gap-lg-3{gap:1rem!important}.gap-lg-4{gap:1.5rem!important}.gap-lg-5{gap:3rem!important}.row-gap-lg-0{row-gap:0!important}.row-gap-lg-1{row-gap:.25rem!important}.row-gap-lg-2{row-gap:.5rem!important}.row-gap-lg-3{row-gap:1rem!important}.row-gap-lg-4{row-gap:1.5rem!important}.row-gap-lg-5{row-gap:3rem!important}.column-gap-lg-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-lg-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-lg-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-lg-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-lg-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-lg-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.text-lg-start{text-align:left!important}.text-lg-end{text-align:right!important}.text-lg-center{text-align:center!important}}@media (min-width:1200px){.float-xl-start{float:left!important}.float-xl-end{float:right!important}.float-xl-none{float:none!important}.object-fit-xl-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-xl-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-xl-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-xl-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-xl-none{-o-object-fit:none!important;object-fit:none!important}.d-xl-inline{display:inline!important}.d-xl-inline-block{display:inline-block!important}.d-xl-block{display:block!important}.d-xl-grid{display:grid!important}.d-xl-inline-grid{display:inline-grid!important}.d-xl-table{display:table!important}.d-xl-table-row{display:table-row!important}.d-xl-table-cell{display:table-cell!important}.d-xl-flex{display:flex!important}.d-xl-inline-flex{display:inline-flex!important}.d-xl-none{display:none!important}.flex-xl-fill{flex:1 1 auto!important}.flex-xl-row{flex-direction:row!important}.flex-xl-column{flex-direction:column!important}.flex-xl-row-reverse{flex-direction:row-reverse!important}.flex-xl-column-reverse{flex-direction:column-reverse!important}.flex-xl-grow-0{flex-grow:0!important}.flex-xl-grow-1{flex-grow:1!important}.flex-xl-shrink-0{flex-shrink:0!important}.flex-xl-shrink-1{flex-shrink:1!important}.flex-xl-wrap{flex-wrap:wrap!important}.flex-xl-nowrap{flex-wrap:nowrap!important}.flex-xl-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-xl-start{justify-content:flex-start!important}.justify-content-xl-end{justify-content:flex-end!important}.justify-content-xl-center{justify-content:center!important}.justify-content-xl-between{justify-content:space-between!important}.justify-content-xl-around{justify-content:space-around!important}.justify-content-xl-evenly{justify-content:space-evenly!important}.align-items-xl-start{align-items:flex-start!important}.align-items-xl-end{align-items:flex-end!important}.align-items-xl-center{align-items:center!important}.align-items-xl-baseline{align-items:baseline!important}.align-items-xl-stretch{align-items:stretch!important}.align-content-xl-start{align-content:flex-start!important}.align-content-xl-end{align-content:flex-end!important}.align-content-xl-center{align-content:center!important}.align-content-xl-between{align-content:space-between!important}.align-content-xl-around{align-content:space-around!important}.align-content-xl-stretch{align-content:stretch!important}.align-self-xl-auto{align-self:auto!important}.align-self-xl-start{align-self:flex-start!important}.align-self-xl-end{align-self:flex-end!important}.align-self-xl-center{align-self:center!important}.align-self-xl-baseline{align-self:baseline!important}.align-self-xl-stretch{align-self:stretch!important}.order-xl-first{order:-1!important}.order-xl-0{order:0!important}.order-xl-1{order:1!important}.order-xl-2{order:2!important}.order-xl-3{order:3!important}.order-xl-4{order:4!important}.order-xl-5{order:5!important}.order-xl-last{order:6!important}.m-xl-0{margin:0!important}.m-xl-1{margin:.25rem!important}.m-xl-2{margin:.5rem!important}.m-xl-3{margin:1rem!important}.m-xl-4{margin:1.5rem!important}.m-xl-5{margin:3rem!important}.m-xl-auto{margin:auto!important}.mx-xl-0{margin-right:0!important;margin-left:0!important}.mx-xl-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-xl-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-xl-3{margin-right:1rem!important;margin-left:1rem!important}.mx-xl-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-xl-5{margin-right:3rem!important;margin-left:3rem!important}.mx-xl-auto{margin-right:auto!important;margin-left:auto!important}.my-xl-0{margin-top:0!important;margin-bottom:0!important}.my-xl-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-xl-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-xl-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-xl-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-xl-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-xl-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-xl-0{margin-top:0!important}.mt-xl-1{margin-top:.25rem!important}.mt-xl-2{margin-top:.5rem!important}.mt-xl-3{margin-top:1rem!important}.mt-xl-4{margin-top:1.5rem!important}.mt-xl-5{margin-top:3rem!important}.mt-xl-auto{margin-top:auto!important}.me-xl-0{margin-right:0!important}.me-xl-1{margin-right:.25rem!important}.me-xl-2{margin-right:.5rem!important}.me-xl-3{margin-right:1rem!important}.me-xl-4{margin-right:1.5rem!important}.me-xl-5{margin-right:3rem!important}.me-xl-auto{margin-right:auto!important}.mb-xl-0{margin-bottom:0!important}.mb-xl-1{margin-bottom:.25rem!important}.mb-xl-2{margin-bottom:.5rem!important}.mb-xl-3{margin-bottom:1rem!important}.mb-xl-4{margin-bottom:1.5rem!important}.mb-xl-5{margin-bottom:3rem!important}.mb-xl-auto{margin-bottom:auto!important}.ms-xl-0{margin-left:0!important}.ms-xl-1{margin-left:.25rem!important}.ms-xl-2{margin-left:.5rem!important}.ms-xl-3{margin-left:1rem!important}.ms-xl-4{margin-left:1.5rem!important}.ms-xl-5{margin-left:3rem!important}.ms-xl-auto{margin-left:auto!important}.p-xl-0{padding:0!important}.p-xl-1{padding:.25rem!important}.p-xl-2{padding:.5rem!important}.p-xl-3{padding:1rem!important}.p-xl-4{padding:1.5rem!important}.p-xl-5{padding:3rem!important}.px-xl-0{padding-right:0!important;padding-left:0!important}.px-xl-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-xl-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-xl-3{padding-right:1rem!important;padding-left:1rem!important}.px-xl-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-xl-5{padding-right:3rem!important;padding-left:3rem!important}.py-xl-0{padding-top:0!important;padding-bottom:0!important}.py-xl-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-xl-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-xl-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-xl-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-xl-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-xl-0{padding-top:0!important}.pt-xl-1{padding-top:.25rem!important}.pt-xl-2{padding-top:.5rem!important}.pt-xl-3{padding-top:1rem!important}.pt-xl-4{padding-top:1.5rem!important}.pt-xl-5{padding-top:3rem!important}.pe-xl-0{padding-right:0!important}.pe-xl-1{padding-right:.25rem!important}.pe-xl-2{padding-right:.5rem!important}.pe-xl-3{padding-right:1rem!important}.pe-xl-4{padding-right:1.5rem!important}.pe-xl-5{padding-right:3rem!important}.pb-xl-0{padding-bottom:0!important}.pb-xl-1{padding-bottom:.25rem!important}.pb-xl-2{padding-bottom:.5rem!important}.pb-xl-3{padding-bottom:1rem!important}.pb-xl-4{padding-bottom:1.5rem!important}.pb-xl-5{padding-bottom:3rem!important}.ps-xl-0{padding-left:0!important}.ps-xl-1{padding-left:.25rem!important}.ps-xl-2{padding-left:.5rem!important}.ps-xl-3{padding-left:1rem!important}.ps-xl-4{padding-left:1.5rem!important}.ps-xl-5{padding-left:3rem!important}.gap-xl-0{gap:0!important}.gap-xl-1{gap:.25rem!important}.gap-xl-2{gap:.5rem!important}.gap-xl-3{gap:1rem!important}.gap-xl-4{gap:1.5rem!important}.gap-xl-5{gap:3rem!important}.row-gap-xl-0{row-gap:0!important}.row-gap-xl-1{row-gap:.25rem!important}.row-gap-xl-2{row-gap:.5rem!important}.row-gap-xl-3{row-gap:1rem!important}.row-gap-xl-4{row-gap:1.5rem!important}.row-gap-xl-5{row-gap:3rem!important}.column-gap-xl-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-xl-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-xl-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-xl-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-xl-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-xl-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.text-xl-start{text-align:left!important}.text-xl-end{text-align:right!important}.text-xl-center{text-align:center!important}}@media (min-width:1400px){.float-xxl-start{float:left!important}.float-xxl-end{float:right!important}.float-xxl-none{float:none!important}.object-fit-xxl-contain{-o-object-fit:contain!important;object-fit:contain!important}.object-fit-xxl-cover{-o-object-fit:cover!important;object-fit:cover!important}.object-fit-xxl-fill{-o-object-fit:fill!important;object-fit:fill!important}.object-fit-xxl-scale{-o-object-fit:scale-down!important;object-fit:scale-down!important}.object-fit-xxl-none{-o-object-fit:none!important;object-fit:none!important}.d-xxl-inline{display:inline!important}.d-xxl-inline-block{display:inline-block!important}.d-xxl-block{display:block!important}.d-xxl-grid{display:grid!important}.d-xxl-inline-grid{display:inline-grid!important}.d-xxl-table{display:table!important}.d-xxl-table-row{display:table-row!important}.d-xxl-table-cell{display:table-cell!important}.d-xxl-flex{display:flex!important}.d-xxl-inline-flex{display:inline-flex!important}.d-xxl-none{display:none!important}.flex-xxl-fill{flex:1 1 auto!important}.flex-xxl-row{flex-direction:row!important}.flex-xxl-column{flex-direction:column!important}.flex-xxl-row-reverse{flex-direction:row-reverse!important}.flex-xxl-column-reverse{flex-direction:column-reverse!important}.flex-xxl-grow-0{flex-grow:0!important}.flex-xxl-grow-1{flex-grow:1!important}.flex-xxl-shrink-0{flex-shrink:0!important}.flex-xxl-shrink-1{flex-shrink:1!important}.flex-xxl-wrap{flex-wrap:wrap!important}.flex-xxl-nowrap{flex-wrap:nowrap!important}.flex-xxl-wrap-reverse{flex-wrap:wrap-reverse!important}.justify-content-xxl-start{justify-content:flex-start!important}.justify-content-xxl-end{justify-content:flex-end!important}.justify-content-xxl-center{justify-content:center!important}.justify-content-xxl-between{justify-content:space-between!important}.justify-content-xxl-around{justify-content:space-around!important}.justify-content-xxl-evenly{justify-content:space-evenly!important}.align-items-xxl-start{align-items:flex-start!important}.align-items-xxl-end{align-items:flex-end!important}.align-items-xxl-center{align-items:center!important}.align-items-xxl-baseline{align-items:baseline!important}.align-items-xxl-stretch{align-items:stretch!important}.align-content-xxl-start{align-content:flex-start!important}.align-content-xxl-end{align-content:flex-end!important}.align-content-xxl-center{align-content:center!important}.align-content-xxl-between{align-content:space-between!important}.align-content-xxl-around{align-content:space-around!important}.align-content-xxl-stretch{align-content:stretch!important}.align-self-xxl-auto{align-self:auto!important}.align-self-xxl-start{align-self:flex-start!important}.align-self-xxl-end{align-self:flex-end!important}.align-self-xxl-center{align-self:center!important}.align-self-xxl-baseline{align-self:baseline!important}.align-self-xxl-stretch{align-self:stretch!important}.order-xxl-first{order:-1!important}.order-xxl-0{order:0!important}.order-xxl-1{order:1!important}.order-xxl-2{order:2!important}.order-xxl-3{order:3!important}.order-xxl-4{order:4!important}.order-xxl-5{order:5!important}.order-xxl-last{order:6!important}.m-xxl-0{margin:0!important}.m-xxl-1{margin:.25rem!important}.m-xxl-2{margin:.5rem!important}.m-xxl-3{margin:1rem!important}.m-xxl-4{margin:1.5rem!important}.m-xxl-5{margin:3rem!important}.m-xxl-auto{margin:auto!important}.mx-xxl-0{margin-right:0!important;margin-left:0!important}.mx-xxl-1{margin-right:.25rem!important;margin-left:.25rem!important}.mx-xxl-2{margin-right:.5rem!important;margin-left:.5rem!important}.mx-xxl-3{margin-right:1rem!important;margin-left:1rem!important}.mx-xxl-4{margin-right:1.5rem!important;margin-left:1.5rem!important}.mx-xxl-5{margin-right:3rem!important;margin-left:3rem!important}.mx-xxl-auto{margin-right:auto!important;margin-left:auto!important}.my-xxl-0{margin-top:0!important;margin-bottom:0!important}.my-xxl-1{margin-top:.25rem!important;margin-bottom:.25rem!important}.my-xxl-2{margin-top:.5rem!important;margin-bottom:.5rem!important}.my-xxl-3{margin-top:1rem!important;margin-bottom:1rem!important}.my-xxl-4{margin-top:1.5rem!important;margin-bottom:1.5rem!important}.my-xxl-5{margin-top:3rem!important;margin-bottom:3rem!important}.my-xxl-auto{margin-top:auto!important;margin-bottom:auto!important}.mt-xxl-0{margin-top:0!important}.mt-xxl-1{margin-top:.25rem!important}.mt-xxl-2{margin-top:.5rem!important}.mt-xxl-3{margin-top:1rem!important}.mt-xxl-4{margin-top:1.5rem!important}.mt-xxl-5{margin-top:3rem!important}.mt-xxl-auto{margin-top:auto!important}.me-xxl-0{margin-right:0!important}.me-xxl-1{margin-right:.25rem!important}.me-xxl-2{margin-right:.5rem!important}.me-xxl-3{margin-right:1rem!important}.me-xxl-4{margin-right:1.5rem!important}.me-xxl-5{margin-right:3rem!important}.me-xxl-auto{margin-right:auto!important}.mb-xxl-0{margin-bottom:0!important}.mb-xxl-1{margin-bottom:.25rem!important}.mb-xxl-2{margin-bottom:.5rem!important}.mb-xxl-3{margin-bottom:1rem!important}.mb-xxl-4{margin-bottom:1.5rem!important}.mb-xxl-5{margin-bottom:3rem!important}.mb-xxl-auto{margin-bottom:auto!important}.ms-xxl-0{margin-left:0!important}.ms-xxl-1{margin-left:.25rem!important}.ms-xxl-2{margin-left:.5rem!important}.ms-xxl-3{margin-left:1rem!important}.ms-xxl-4{margin-left:1.5rem!important}.ms-xxl-5{margin-left:3rem!important}.ms-xxl-auto{margin-left:auto!important}.p-xxl-0{padding:0!important}.p-xxl-1{padding:.25rem!important}.p-xxl-2{padding:.5rem!important}.p-xxl-3{padding:1rem!important}.p-xxl-4{padding:1.5rem!important}.p-xxl-5{padding:3rem!important}.px-xxl-0{padding-right:0!important;padding-left:0!important}.px-xxl-1{padding-right:.25rem!important;padding-left:.25rem!important}.px-xxl-2{padding-right:.5rem!important;padding-left:.5rem!important}.px-xxl-3{padding-right:1rem!important;padding-left:1rem!important}.px-xxl-4{padding-right:1.5rem!important;padding-left:1.5rem!important}.px-xxl-5{padding-right:3rem!important;padding-left:3rem!important}.py-xxl-0{padding-top:0!important;padding-bottom:0!important}.py-xxl-1{padding-top:.25rem!important;padding-bottom:.25rem!important}.py-xxl-2{padding-top:.5rem!important;padding-bottom:.5rem!important}.py-xxl-3{padding-top:1rem!important;padding-bottom:1rem!important}.py-xxl-4{padding-top:1.5rem!important;padding-bottom:1.5rem!important}.py-xxl-5{padding-top:3rem!important;padding-bottom:3rem!important}.pt-xxl-0{padding-top:0!important}.pt-xxl-1{padding-top:.25rem!important}.pt-xxl-2{padding-top:.5rem!important}.pt-xxl-3{padding-top:1rem!important}.pt-xxl-4{padding-top:1.5rem!important}.pt-xxl-5{padding-top:3rem!important}.pe-xxl-0{padding-right:0!important}.pe-xxl-1{padding-right:.25rem!important}.pe-xxl-2{padding-right:.5rem!important}.pe-xxl-3{padding-right:1rem!important}.pe-xxl-4{padding-right:1.5rem!important}.pe-xxl-5{padding-right:3rem!important}.pb-xxl-0{padding-bottom:0!important}.pb-xxl-1{padding-bottom:.25rem!important}.pb-xxl-2{padding-bottom:.5rem!important}.pb-xxl-3{padding-bottom:1rem!important}.pb-xxl-4{padding-bottom:1.5rem!important}.pb-xxl-5{padding-bottom:3rem!important}.ps-xxl-0{padding-left:0!important}.ps-xxl-1{padding-left:.25rem!important}.ps-xxl-2{padding-left:.5rem!important}.ps-xxl-3{padding-left:1rem!important}.ps-xxl-4{padding-left:1.5rem!important}.ps-xxl-5{padding-left:3rem!important}.gap-xxl-0{gap:0!important}.gap-xxl-1{gap:.25rem!important}.gap-xxl-2{gap:.5rem!important}.gap-xxl-3{gap:1rem!important}.gap-xxl-4{gap:1.5rem!important}.gap-xxl-5{gap:3rem!important}.row-gap-xxl-0{row-gap:0!important}.row-gap-xxl-1{row-gap:.25rem!important}.row-gap-xxl-2{row-gap:.5rem!important}.row-gap-xxl-3{row-gap:1rem!important}.row-gap-xxl-4{row-gap:1.5rem!important}.row-gap-xxl-5{row-gap:3rem!important}.column-gap-xxl-0{-moz-column-gap:0!important;column-gap:0!important}.column-gap-xxl-1{-moz-column-gap:0.25rem!important;column-gap:.25rem!important}.column-gap-xxl-2{-moz-column-gap:0.5rem!important;column-gap:.5rem!important}.column-gap-xxl-3{-moz-column-gap:1rem!important;column-gap:1rem!important}.column-gap-xxl-4{-moz-column-gap:1.5rem!important;column-gap:1.5rem!important}.column-gap-xxl-5{-moz-column-gap:3rem!important;column-gap:3rem!important}.text-xxl-start{text-align:left!important}.text-xxl-end{text-align:right!important}.text-xxl-center{text-align:center!important}}@media (min-width:1200px){.fs-1{font-size:2.5rem!important}.fs-2{font-size:2rem!important}.fs-3{font-size:1.75rem!important}.fs-4{font-size:1.5rem!important}}@media print{.d-print-inline{display:inline!important}.d-print-inline-block{display:inline-block!important}.d-print-block{display:block!important}.d-print-grid{display:grid!important}.d-print-inline-grid{display:inline-grid!important}.d-print-table{display:table!important}.d-print-table-row{display:table-row!important}.d-print-table-cell{display:table-cell!important}.d-print-flex{display:flex!important}.d-print-inline-flex{display:inline-flex!important}.d-print-none{display:none!important}}.table-danger,.table-info,.table-light,.table-primary,.table-secondary,.table-success,.table-warning{--bs-table-color:#222}.navbar{font-family:"News Cycle","Arial Narrow Bold",sans-serif;font-size:18px;font-weight:700}.navbar-brand{padding-top:.5rem;font-size:inherit;font-weight:700;text-transform:uppercase}.btn{font-family:"News Cycle","Arial Narrow Bold",sans-serif;font-weight:700}.btn-secondary,.btn-warning{color:#fff}.pagination a:hover{text-decoration:none}
/*# sourceMappingURL=bootstrap.min.css.map */
```

# static/css/styles.css

```css
.table th,
.table td {
    vertical-align: middle !important;
}

.table-admin th:first-of-type,
.table-admin td:first-of-type,
.table-admin th:last-of-type,
.table-admin td:last-of-type {
    width: 1%;
    white-space: nowrap;
}

.center-column-1 th:nth-child(1),
.center-column-1 td:nth-child(1),
.center-column-2 th:nth-child(2),
.center-column-2 td:nth-child(2),
.center-column-3 th:nth-child(3),
.center-column-3 td:nth-child(3),
.center-column-4 th:nth-child(4),
.center-column-4 td:nth-child(4),
.center-column-5 th:nth-child(5),
.center-column-5 td:nth-child(5),
.center-column-6 th:nth-child(6),
.center-column-6 td:nth-child(6) {
    text-align: center;
    width: 1%;
    white-space: nowrap;
}
```

# static/img/favicon.png

This is a binary file of the type: Image

# static/img/placeholder.png

This is a binary file of the type: Image

# static/img/products/000002/000002-001.jpg

This is a binary file of the type: Image

# static/img/products/000004/000004-001.jpg

This is a binary file of the type: Image

# static/img/products/000006/000006-001.jpg

This is a binary file of the type: Image

# static/img/products/000007/000007-001.jpg

This is a binary file of the type: Image

# static/img/products/000008/000008-001.jpg

This is a binary file of the type: Image

# static/img/products/000009/000009-001.jpg

This is a binary file of the type: Image

# static/img/products/000011/000011-001.jpg

This is a binary file of the type: Image

# static/img/products/000012/000012-001.jpg

This is a binary file of the type: Image

# static/img/products/000017/000017-001.jpg

This is a binary file of the type: Image

# static/img/products/000018/000018-001.jpg

This is a binary file of the type: Image

# static/img/products/000019/000019-001.jpg

This is a binary file of the type: Image

# static/img/products/000020/000020-001.jpg

This is a binary file of the type: Image

# static/img/products/000022/000022-001.jpg

This is a binary file of the type: Image

# static/img/products/000023/000023-001.jpg

This is a binary file of the type: Image

# static/img/products/000024/000024-001.jpg

This is a binary file of the type: Image

# static/img/products/000024/000024-002.jpg

This is a binary file of the type: Image

# static/img/products/000024/000024-003.jpg

This is a binary file of the type: Image

# static/img/products/000025/000025-001.jpg

This is a binary file of the type: Image

# static/img/products/000026/000026-001.jpg

This is a binary file of the type: Image

# static/img/products/000028/000028-001.jpg

This is a binary file of the type: Image

# static/img/products/000030/000030-001.jpg

This is a binary file of the type: Image

# static/img/user-default.png

This is a binary file of the type: Image

# static/js/scripts.js

```js
function algumaCoisa() {
    console.log("Função de exemplo");
}

document.addEventListener("DOMContentLoaded", function() {
    algumaCoisa();
});
```

# static/uploads/usuarios/5_6b5a130d6bc33fa2.jpg

This is a binary file of the type: Image

# static/uploads/usuarios/5_6717d9e290bff45a.jpeg

This is a binary file of the type: Image

# static/uploads/usuarios/5_ad5cf8ae1512dff2.jpg

This is a binary file of the type: Image

# static/uploads/usuarios/6_fa0710b123012c4d.jpg

This is a binary file of the type: Image

# templates/admin/categorias/alterar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Alteração de Categoria</h2>
        <hr>
        <form action="/admin/categorias/alterar" method="post">
            <input type="hidden" name="id" value="{{ categoria.id }}">
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome da Categoria" required value="{{ categoria.nome }}">
                <label for="nome">Nome da Categoria</label>
            </div>
            <button type="submit" class="btn btn-primary me-2">Alterar Categoria</button>
            <a href="/admin/categorias" class="btn btn-secondary">Cancelar Alteração</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/categorias/cadastrar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Cadastro de Categoria</h2>
        <hr>
        <form action="/admin/categorias/cadastrar" method="post">
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome da Categoria" required>
                <label for="nome">Nome da Categoria</label>
            </div>
            <button type="submit" class="btn btn-primary me-2">Cadastrar Categoria</button>
            <a href="/admin/categorias" class="btn btn-secondary">Cancelar Cadastro</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/categorias/excluir.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Excluir Categoria</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <div class="alert alert-warning" role="alert">
            <h4 class="alert-heading">Confirmar Exclusão</h4>
            <p>Tem certeza que deseja excluir a categoria abaixo?</p>
            <hr>
            <p class="mb-0">
                <strong>Nome:</strong> {{ categoria.nome }}
            </p>
        </div>
        <form action="/admin/categorias/excluir" method="post">
            <input type="hidden" name="id" value="{{ categoria.id }}">
            <button type="submit" class="btn btn-danger me-2">Confirmar Exclusão</button>
            <a href="/admin/categorias" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/categorias/listar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between">
    <h1>Categorias</h1>
    <a href="/admin/categorias/cadastrar" class="btn btn-primary">Nova Categoria</a>
</div>
<hr>
{% if categorias %}
<table class="table table-striped table-admin center-column-1">
    <thead>
        <tr>
            <th>Código</th>
            <th>Nome</th>
            <th class="text-center">Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for categoria in categorias %}
        <tr>
            <td>{{"{:06d}".format(categoria.id)}}</td>
            <td>{{categoria.nome}}</td>
            <td class="text-center">
                <a href="/admin/categorias/alterar/{{categoria.id}}" class="btn btn-success btn-sm" title="Alterar"><i class="bi-pencil"></i></a>
                <a href="/admin/categorias/excluir/{{categoria.id}}" class="btn btn-danger btn-sm"><i class="bi-trash"></i></a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<div class="alert alert-warning" role="alert">
    Nenhuma categoria cadastrada.
</div>
{% endif %}
{% endblock %}
```

# templates/admin/clientes/alterar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Alterar Cliente</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/clientes/alterar" method="post">
            <input type="hidden" name="id" value="{{ cliente.id }}">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome Completo" value="{{ cliente.nome }}" required>
                        <label for="nome">Nome Completo</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="cpf" name="cpf" placeholder="CPF" value="{{ cliente.cpf }}" pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Formato: 000.000.000-00" required>
                        <label for="cpf">CPF</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="email" name="email" placeholder="E-mail" value="{{ cliente.email }}" required>
                        <label for="email">E-mail</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="tel" class="form-control" id="telefone" name="telefone" placeholder="Telefone" value="{{ cliente.telefone }}" pattern="\(\d{2}\) \d{4,5}-\d{4}" title="Formato: (00) 0000-0000 ou (00) 00000-0000" required>
                        <label for="telefone">Telefone</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="alert alert-info">
                        <i class="bi-info-circle"></i> Deixe os campos de senha em branco para manter a senha atual
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="senha" name="senha" placeholder="Nova Senha" minlength="6">
                        <label for="senha">Nova Senha (opcional)</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="confirmar_senha" name="confirmar_senha" placeholder="Confirmar Nova Senha" minlength="6">
                        <label for="confirmar_senha">Confirmar Nova Senha</label>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary me-2">Salvar Alterações</button>
            <a href="/admin/clientes" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>

<script>
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha || confirmarSenha) {
        if (senha !== confirmarSenha) {
            e.preventDefault();
            alert('As senhas não coincidem!');
        }
    }
});

// Máscaras para CPF e Telefone
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

document.getElementById('telefone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
        if (value.length === 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else {
            value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        }
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/(\d{0,2})/, '($1');
    }
    e.target.value = value;
});
</script>
{% endblock %}
```

# templates/admin/clientes/cadastrar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Cadastro de Cliente</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/clientes/cadastrar" method="post">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome Completo" required>
                        <label for="nome">Nome Completo</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="cpf" name="cpf" placeholder="CPF" pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Formato: 000.000.000-00" required>
                        <label for="cpf">CPF</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="email" name="email" placeholder="E-mail" required>
                        <label for="email">E-mail</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="tel" class="form-control" id="telefone" name="telefone" placeholder="Telefone" pattern="\(\d{2}\) \d{4,5}-\d{4}" title="Formato: (00) 0000-0000 ou (00) 00000-0000" required>
                        <label for="telefone">Telefone</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="senha" name="senha" placeholder="Senha" minlength="6" required>
                        <label for="senha">Senha</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="confirmar_senha" name="confirmar_senha" placeholder="Confirmar Senha" minlength="6" required>
                        <label for="confirmar_senha">Confirmar Senha</label>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary me-2">Cadastrar Cliente</button>
            <a href="/admin/clientes" class="btn btn-secondary">Cancelar Cadastro</a>
        </form>
    </div>
</div>

<script>
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha !== confirmarSenha) {
        e.preventDefault();
        alert('As senhas não coincidem!');
    }
});

// Máscaras para CPF e Telefone
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

document.getElementById('telefone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
        if (value.length === 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else {
            value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        }
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/(\d{0,2})/, '($1');
    }
    e.target.value = value;
});
</script>
{% endblock %}
```

# templates/admin/clientes/clientes.html

```html
{% extends "base.html" %}
{% block conteudo %}
<h1>Clientes</h1>
<hr>
<table class="table table-striped">
    <thead>
        <tr>
            <th>Id</th>
            <th>Nome</th>
            <th>CPF</th>
            <th>Email</th>
            <th>Telefone</th>
        </tr>
    </thead>
    <tbody>
        {% for cliente in clientes %}
        <tr>
            <td>{{cliente.id}}</td>
            <td>{{cliente.nome}}</td>
            <td>{{cliente.cpf}}</td>
            <td>{{cliente.email}}</td>
            <td>{{cliente.telefone}}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

# templates/admin/clientes/detalhar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between mb-3">
    <h1>Detalhes do Cliente</h1>
    <div>
        <a href="/admin/clientes/alterar/{{cliente.id}}" class="btn btn-success">
            <i class="bi-pencil"></i> Alterar
        </a>
        <a href="/admin/clientes" class="btn btn-secondary">
            <i class="bi-arrow-left"></i> Voltar
        </a>
    </div>
</div>
<hr>
<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-md-3 text-center">
                <div class="mb-3">
                    <i class="bi-person-circle" style="font-size: 150px; color: #6c757d;"></i>
                </div>
                <h3>{{cliente.nome}}</h3>
                <p class="text-muted">Cliente #{{"{:06d}".format(cliente.id)}}</p>
            </div>
            <div class="col-md-9">
                <h4 class="mb-3">Informações Pessoais</h4>

                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">Nome Completo</h6>
                                <p class="card-text fs-5">{{cliente.nome}}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">CPF</h6>
                                <p class="card-text fs-5">{{cliente.cpf}}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <h4 class="mb-3">Informações de Contato</h4>

                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">E-mail</h6>
                                <p class="card-text fs-5">
                                    <i class="bi-envelope"></i> {{cliente.email}}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">Telefone</h6>
                                <p class="card-text fs-5">
                                    <i class="bi-telephone"></i> {{cliente.telefone}}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="alert alert-info">
                    <h5><i class="bi-shield-lock"></i> Informações de Segurança</h5>
                    <p class="mb-0">A senha do cliente está criptografada e não pode ser visualizada por questões de segurança.</p>
                </div>

                <div class="d-flex gap-2 mt-4">
                    <a href="/admin/clientes/alterar/{{cliente.id}}" class="btn btn-success">
                        <i class="bi-pencil"></i> Alterar Cliente
                    </a>
                    <a href="/admin/clientes/excluir/{{cliente.id}}" class="btn btn-danger">
                        <i class="bi-trash"></i> Excluir Cliente
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/admin/clientes/excluir.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Excluir Cliente</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <div class="alert alert-warning" role="alert">
            <h4 class="alert-heading">Confirmar Exclusão</h4>
            <p>Tem certeza que deseja excluir o cliente abaixo?</p>
            <hr>
            <p class="mb-0">
                <strong>Nome:</strong> {{ cliente.nome }}<br>
                <strong>CPF:</strong> {{ cliente.cpf }}<br>
                <strong>E-mail:</strong> {{ cliente.email }}<br>
                <strong>Telefone:</strong> {{ cliente.telefone }}
            </p>
        </div>
        <form action="/admin/clientes/excluir" method="post">
            <input type="hidden" name="id" value="{{ cliente.id }}">
            <button type="submit" class="btn btn-danger me-2">Confirmar Exclusão</button>
            <a href="/admin/clientes" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/clientes/listar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between">
    <h1>Clientes</h1>
    <a href="/admin/clientes/cadastrar" class="btn btn-primary">Novo Cliente</a>
</div>
<hr>
<table class="table table-striped table-admin center-column-1">
    <thead>
        <tr>
            <th>Código</th>
            <th>Nome</th>
            <th>CPF</th>
            <th>E-mail</th>
            <th>Telefone</th>
            <th class="text-center">Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for cliente in clientes %}
        <tr>
            <td>{{"{:06d}".format(cliente.id)}}</td>
            <td>{{cliente.nome}}</td>
            <td>{{cliente.cpf}}</td>
            <td>{{cliente.email}}</td>
            <td>{{cliente.telefone}}</td>
            <td class="text-center">
                <a href="/admin/clientes/detalhar/{{cliente.id}}" class="btn btn-info btn-sm" title="Ver Detalhes"><i class="bi-eye"></i></a>
                <a href="/admin/clientes/alterar/{{cliente.id}}" class="btn btn-success btn-sm" title="Alterar"><i class="bi-pencil"></i></a>
                <a href="/admin/clientes/excluir/{{cliente.id}}" class="btn btn-danger btn-sm" title="Excluir"><i class="bi-trash"></i></a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

# templates/admin/formas/alterar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Alterar Forma de Pagamento</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/formas/alterar" method="post">
            <input type="hidden" name="id" value="{{ forma.id }}">
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome da Forma de Pagamento" value="{{ forma.nome }}" required>
                <label for="nome">Nome da Forma de Pagamento</label>
            </div>
            <div class="form-floating mb-3">
                <input type="number" step="0.01" min="0" max="100" class="form-control" id="desconto" name="desconto" placeholder="Desconto (%)" value="{{ forma.desconto }}" required>
                <label for="desconto">Desconto (%)</label>
            </div>
            <button type="submit" class="btn btn-primary me-2">Salvar Alterações</button>
            <a href="/admin/formas" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/formas/cadastrar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Cadastro de Forma de Pagamento</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/formas/cadastrar" method="post">
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome da Forma de Pagamento" required>
                <label for="nome">Nome da Forma de Pagamento</label>
            </div>
            <div class="form-floating mb-3">
                <input type="number" step="0.01" min="0" max="100" class="form-control" id="desconto" name="desconto" placeholder="Desconto (%)" required>
                <label for="desconto">Desconto (%)</label>
            </div>
            <button type="submit" class="btn btn-primary me-2">Cadastrar Forma de Pagamento</button>
            <a href="/admin/formas" class="btn btn-secondary">Cancelar Cadastro</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/formas/excluir.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Excluir Forma de Pagamento</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <div class="alert alert-warning" role="alert">
            <h4 class="alert-heading">Confirmar Exclusão</h4>
            <p>Tem certeza que deseja excluir a forma de pagamento abaixo?</p>
            <hr>
            <p class="mb-0">
                <strong>Nome:</strong> {{ forma.nome }}<br>
                <strong>Desconto:</strong> {{ "%.2f"|format(forma.desconto) }}%
            </p>
        </div>
        <form action="/admin/formas/excluir" method="post">
            <input type="hidden" name="id" value="{{ forma.id }}">
            <button type="submit" class="btn btn-danger me-2">Confirmar Exclusão</button>
            <a href="/admin/formas" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/formas/listar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between">
    <h1>Formas de Pagamento</h1>
    <a href="/admin/formas/cadastrar" class="btn btn-primary">Nova Forma de Pagamento</a>
</div>
<hr>
<table class="table table-striped table-admin center-column-3">
    <thead>
        <tr>
            <th>Código</th>
            <th>Nome</th>
            <th>Desconto (%)</th>
            <th class="text-center">Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for forma in formas %}
        <tr>
            <td>{{"{:04d}".format(forma.id)}}</td>
            <td>{{forma.nome}}</td>
            <td>{{"{:.2f}".format(forma.desconto)}}%</td>
            <td class="text-center">
                <a href="/admin/formas/alterar/{{forma.id}}" class="btn btn-success btn-sm" title="Alterar"><i class="bi-pencil"></i></a>
                <a href="/admin/formas/excluir/{{forma.id}}" class="btn btn-danger btn-sm"><i class="bi-trash"></i></a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

# templates/admin/produtos/alterar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Alterar Produto</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/produtos/alterar" method="post" enctype="multipart/form-data">
            <input type="hidden" name="id" value="{{ produto.id }}">
            <div class="form-floating mb-3">
                <select class="form-select" id="categoria_id" name="categoria_id" required>
                    <option value="">Selecione uma categoria</option>
                    {% for categoria in categorias %}
                    <option value="{{ categoria.id }}" {% if categoria.id == produto.categoria_id %}selected{% endif %}>{{ categoria.nome }}</option>
                    {% endfor %}
                </select>
                <label for="categoria_id">Categoria</label>
            </div>
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome do Produto" value="{{ produto.nome }}" required>
                <label for="nome">Nome do Produto</label>
            </div>
            <div class="form-floating mb-3">
                <textarea type="text" class="form-control" id="descricao" name="descricao"
                    placeholder="Descrição do Produto" required style="height: 100px">{{ produto.descricao }}</textarea>
                <label for="descricao">Descrição do Produto</label>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <div class="form-floating mb-3">
                        <input type="number" step="0.01" class="form-control" id="preco" name="preco" placeholder="Preço do Produto"
                            value="{{ produto.preco }}" required>
                        <label for="preco">Preço do Produto</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-floating mb-3">
                        <input type="number" class="form-control" id="quantidade" name="quantidade"
                            placeholder="Quantidade em Estoque" value="{{ produto.quantidade }}" required>
                        <label for="quantidade">Quantidade em Estoque</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="foto" class="form-label">{% if foto_principal %}Substituir Foto Principal{% else %}Adicionar Foto Principal{% endif %}</label>
                        <input type="file" class="form-control" id="foto" name="foto" accept="image/*">
                        <div class="form-text small">Formatos aceitos: JPG, PNG, GIF, WEBP. Será cortada para formato quadrado.</div>
                    </div>
                </div>
            </div>

            {% if foto_principal %}
            <div class="row mb-3">
                <div class="col-12">
                    <label class="form-label">Foto Principal Atual</label>
                    <div class="d-flex align-items-center">
                        <img id="foto-atual" src="{{ foto_principal }}" alt="Foto atual" style="width: 150px; height: 150px; object-fit: cover; border: 2px solid #dee2e6; border-radius: 8px;" class="me-3">
                        <div>
                            <p class="mb-1">Foto principal atual do produto</p>
                            <small class="text-muted">Esta foto será substituída se você selecionar uma nova imagem acima.</small>
                            <br>
                            <a href="/admin/produtos/{{ produto.id }}/galeria" class="btn btn-sm btn-outline-primary mt-2">
                                <i class="bi-images"></i> Gerenciar Galeria de Fotos
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="row mb-3">
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="bi-info-circle"></i> Este produto ainda não possui foto principal.
                        <a href="/admin/produtos/{{ produto.id }}/galeria" class="alert-link">Clique aqui para acessar a galeria de fotos</a>
                        ou selecione uma foto acima.
                    </div>
                </div>
            </div>
            {% endif %}

            <div class="row" id="preview-container" style="display: none;">
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label">Preview da Nova Foto</label>
                        <div class="d-flex align-items-center">
                            <img id="preview-image" src="" alt="Preview" style="width: 150px; height: 150px; object-fit: cover; border: 2px solid #28a745; border-radius: 8px;" class="me-3">
                            <div>
                                <p class="mb-1"><strong>Nova foto selecionada</strong></p>
                                <small class="text-muted">Esta foto substituirá a foto principal atual quando você salvar as alterações.</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary me-2">Salvar Alterações</button>
            <a href="/admin/produtos" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewContainer.style.display = 'block';
                };

                reader.readAsDataURL(file);
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                fotoInput.value = '';
                previewContainer.style.display = 'none';
            }
        } else {
            previewContainer.style.display = 'none';
        }
    });
});
</script>

{% endblock %}
```

# templates/admin/produtos/cadastrar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Cadastro de Produto</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <form action="/admin/produtos/cadastrar" method="post" enctype="multipart/form-data">
            <div class="form-floating mb-3">
                <select class="form-select" id="categoria_id" name="categoria_id" required>
                    <option value="">Selecione uma categoria</option>
                    {% for categoria in categorias %}
                    <option value="{{ categoria.id }}">{{ categoria.nome }}</option>
                    {% endfor %}
                </select>
                <label for="categoria_id">Categoria</label>
            </div>
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome do Produto" required>
                <label for="nome">Nome do Produto</label>
            </div>
            <div class="form-floating mb-3">
                <textarea type="text" class="form-control" id="descricao" name="descricao"
                    placeholder="Descrição do Produto" required style="height: 100px"></textarea>
                <label for="descricao">Descrição do Produto</label>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <div class="form-floating mb-3">
                        <input type="number" step="0.01" class="form-control" id="preco" name="preco" placeholder="Preço do Produto"
                            required>
                        <label for="preco">Preço do Produto</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-floating mb-3">
                        <input type="number" class="form-control" id="quantidade" name="quantidade"
                            placeholder="Quantidade em Estoque" required>
                        <label for="quantidade">Quantidade em Estoque</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="mb-3">
                        <label for="foto" class="form-label">Foto Principal (Opcional)</label>
                        <input type="file" class="form-control" id="foto" name="foto" accept="image/*">
                        <div class="form-text small">Formatos aceitos: JPG, PNG, GIF, WEBP. Será cortada para formato quadrado.</div>
                    </div>
                </div>
            </div>
            <div class="row" id="preview-container" style="display: none;">
                <div class="col-12">
                    <div class="mb-3">
                        <label class="form-label">Preview da Foto</label>
                        <div class="d-flex align-items-center">
                            <img id="preview-image" src="" alt="Preview" style="width: 150px; height: 150px; object-fit: cover; border: 2px solid #dee2e6; border-radius: 8px;" class="me-3">
                            <div>
                                <p class="mb-1">Preview da foto selecionada</p>
                                <small class="text-muted">A imagem será automaticamente cortada para formato quadrado e redimensionada para 800x800 pixels.</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary me-2">Cadastrar Produto</button>
            <a href="/admin/produtos" class="btn btn-secondary">Cancelar Cadastro</a>
        </form>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewContainer.style.display = 'block';
                };

                reader.readAsDataURL(file);
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                fotoInput.value = '';
                previewContainer.style.display = 'none';
            }
        } else {
            previewContainer.style.display = 'none';
        }
    });
});
</script>

{% endblock %}
```

# templates/admin/produtos/detalhar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between mb-3">
    <h1>Detalhes do Produto</h1>
    <div>
        <a href="/admin/produtos/alterar/{{produto.id}}" class="btn btn-success">
            <i class="bi-pencil"></i> Alterar
        </a>
        <a href="/admin/produtos" class="btn btn-secondary">
            <i class="bi-arrow-left"></i> Voltar
        </a>
    </div>
</div>
<hr>
<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-md-4">
                <img class="img-thumbnail w-100" src="https://picsum.photos/600/600?random={{produto.id}}" alt="{{produto.nome}}" />
            </div>
            <div class="col-md-8">
                <h2 class="card-title mb-3">{{produto.nome}}</h2>

                <div class="mb-3">
                    <h5>Descrição:</h5>
                    <p class="card-text lead">{{produto.descricao}}</p>
                </div>

                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="alert alert-info">
                            <strong>Código:</strong> {{"{:06d}".format(produto.id)}}<br>
                            <strong>Categoria:</strong> {{produto.categoria_nome if produto.categoria_nome else 'Não categorizado'}}<br>
                            <strong>Quantidade em Estoque:</strong> {{produto.quantidade}} unidades
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="alert alert-success">
                            <h4 class="text-success">Preço</h4>
                            <h2 class="mb-0">R$ {{"{:.2f}".format(produto.preco)}}</h2>
                        </div>
                    </div>
                </div>

                <div class="d-flex gap-2">
                    <a href="/admin/produtos/alterar/{{produto.id}}" class="btn btn-success">
                        <i class="bi-pencil"></i> Alterar Produto
                    </a>
                    <a href="/admin/produtos/excluir/{{produto.id}}" class="btn btn-danger">
                        <i class="bi-trash"></i> Excluir Produto
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/admin/produtos/excluir.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="card">
    <div class="card-body">
        <h2>Excluir Produto</h2>
        <hr>
        {% if mensagem %}
        <div class="alert alert-danger" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        <div class="alert alert-warning" role="alert">
            <h4 class="alert-heading">Confirmar Exclusão</h4>
            <p>Tem certeza que deseja excluir o produto abaixo?</p>
            <hr>
            <p class="mb-0">
                <strong>Nome:</strong> {{ produto.nome }}<br>
                <strong>Descrição:</strong> {{ produto.descricao }}<br>
                <strong>Preço:</strong> R$ {{ "%.2f"|format(produto.preco) }}<br>
                <strong>Quantidade:</strong> {{ produto.quantidade }}
            </p>
        </div>
        <form action="/admin/produtos/excluir" method="post">
            <input type="hidden" name="id" value="{{ produto.id }}">
            <button type="submit" class="btn btn-danger me-2">Confirmar Exclusão</button>
            <a href="/admin/produtos" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
```

# templates/admin/produtos/galeria.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between">
    <h1>Galeria de Fotos - {{ produto.nome }}</h1>
    <a href="/admin/produtos" class="btn btn-secondary">Voltar</a>
</div>
<hr>

<div class="row">
    <div class="col-md-8">
        <h3>Fotos Existentes</h3>
        {% if fotos %}
        <div class="row g-3" id="galeria-fotos">
            {% for foto in fotos %}
            {% set foto_numero = foto.split('-')[-1].split('.')[0] | int %}
            <div class="col-md-4" data-numero="{{ foto_numero }}" draggable="true">
                <div class="card">
                    {% if loop.index == 1 %}
                    <div class="badge bg-primary position-absolute top-0 start-0 m-2">Principal</div>
                    {% endif %}
                    <img src="{{ foto }}" class="card-img-top" style="width: 100%; aspect-ratio: 1/1; object-fit: cover;" alt="Foto {{ foto_numero }}">
                    <div class="card-body text-center">
                        <p class="card-text small">Foto {{ "{:03d}".format(foto_numero) }}</p>
                        {% if loop.index == 1 %}
                        <button type="button" class="btn btn-danger btn-sm" disabled title="A foto principal não pode ser excluída">
                            <i class="bi-trash"></i> Excluir
                        </button>
                        {% else %}
                        <form method="post" action="/admin/produtos/{{ produto.id }}/galeria/excluir/{{ foto_numero }}"
                              onsubmit="return confirm('Deseja realmente excluir esta foto?')" style="display: inline;">
                            <button type="submit" class="btn btn-danger btn-sm">
                                <i class="bi-trash"></i> Excluir
                            </button>
                        </form>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if fotos|length > 1 %}
        <div class="mt-4">
            <h4>Reordenar Fotos</h4>
            <p class="text-muted">Arraste as fotos para reordená-las. A primeira foto será sempre a principal.</p>
            <form method="post" action="/admin/produtos/{{ produto.id }}/galeria/reordenar" id="form-reordenar">
                <input type="hidden" name="nova_ordem" id="nova_ordem">
                <button type="button" class="btn btn-success" onclick="salvarOrdem()">
                    <i class="bi-check"></i> Salvar Nova Ordem
                </button>
            </form>
        </div>
        {% endif %}
        {% else %}
        <div class="text-center py-5">
            <i class="bi-images" style="font-size: 4rem; color: #dee2e6;"></i>
            <p class="text-muted mt-3">Nenhuma foto cadastrada para este produto.</p>
        </div>
        {% endif %}
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h3>Adicionar Fotos</h3>
                <form method="post" action="/admin/produtos/{{ produto.id }}/galeria/upload" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="fotos" class="form-label">Selecionar Fotos</label>
                        <input type="file" class="form-control" id="fotos" name="fotos" accept="image/*" multiple required>
                        <div class="form-text">
                            Selecione uma ou mais fotos.<br>
                            Formatos aceitos: JPG, PNG, GIF, WEBP.<br>
                            As imagens serão cortadas para formato quadrado.
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="bi-upload"></i> Enviar Fotos
                    </button>
                </form>

                <hr>

                <div class="mt-3">
                    <h5>Informações</h5>
                    <ul class="list-unstyled small text-muted">
                        <li><i class="bi-info-circle"></i> A primeira foto é sempre a principal</li>
                        <li><i class="bi-arrow-up-down"></i> Arraste para reordenar</li>
                        <li><i class="bi-square"></i> Fotos são automaticamente cortadas para formato quadrado</li>
                        <li><i class="bi-file-earmark-image"></i> Todas as fotos são salvas como JPG</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Sistema de Drag and Drop para reordenar fotos
let draggedElement = null;

document.addEventListener('DOMContentLoaded', function() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    const fotoCards = galeriaFotos.querySelectorAll('[draggable="true"]');

    fotoCards.forEach(card => {
        card.addEventListener('dragstart', function(e) {
            draggedElement = this;
            this.style.opacity = '0.5';
        });

        card.addEventListener('dragend', function(e) {
            this.style.opacity = '';
            draggedElement = null;
        });

        card.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        card.addEventListener('drop', function(e) {
            e.preventDefault();
            if (this !== draggedElement) {
                // Trocar posições
                const allCards = Array.from(galeriaFotos.children);
                const draggedIndex = allCards.indexOf(draggedElement);
                const targetIndex = allCards.indexOf(this);

                if (draggedIndex < targetIndex) {
                    this.parentNode.insertBefore(draggedElement, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(draggedElement, this);
                }

                // Atualizar badges de "Principal"
                atualizarBadgePrincipal();
            }
        });
    });
});

function atualizarBadgePrincipal() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    // Remover todos os badges existentes
    galeriaFotos.querySelectorAll('.badge').forEach(badge => badge.remove());

    // Adicionar badge na primeira foto
    const primeiraFoto = galeriaFotos.firstElementChild;
    if (primeiraFoto) {
        const badge = document.createElement('div');
        badge.className = 'badge bg-primary position-absolute top-0 start-0 m-2';
        badge.textContent = 'Principal';
        primeiraFoto.querySelector('.card').appendChild(badge);
    }
}

function salvarOrdem() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    const cards = galeriaFotos.querySelectorAll('[data-numero]');
    const novaOrdem = Array.from(cards).map(card => card.dataset.numero);

    document.getElementById('nova_ordem').value = novaOrdem.join(',');
    document.getElementById('form-reordenar').submit();
}

// Preview de imagens antes do upload
document.getElementById('fotos').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        console.log(`${files.length} arquivo(s) selecionado(s)`);
    }
});
</script>

{% endblock %}
```

# templates/admin/produtos/listar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="d-flex align-items-center justify-content-between">
    <h1>Produtos</h1>
    <a href="/admin/produtos/cadastrar" class="btn btn-primary">Novo Produto</a>
</div>
<hr>
<table class="table table-striped table-admin center-column-1 center-column-2 center-column-7 center-column-8">
    <thead>
        <tr>
            <th>Código</th>
            <th>Foto</th>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Descrição</th>
            <th>Preço</th>
            <th>Quantidade</th>
            <th class="text-center">Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for produto in produtos %}
        <tr>
            <td>{{"{:06d}".format(produto.id)}}</td>
            <td>
                <img src="{{ produto.foto_principal or '/static/img/placeholder.png' }}"
                     alt="Foto do produto"
                     style="width: 50px; height: 50px; object-fit: cover;">
            </td>
            <td>{{produto.nome}}</td>
            <td>{{produto.categoria_nome}}</td>
            <td>{{produto.descricao}}</td>
            <td>R$ {{produto.preco}}</td>
            <td>{{produto.quantidade}}</td>
            <td class="text-center">
                <a href="/admin/produtos/detalhar/{{produto.id}}" class="btn btn-info btn-sm" title="Ver Detalhes"><i class="bi-eye"></i></a>
                <a href="/admin/produtos/{{produto.id}}/galeria" class="btn btn-warning btn-sm" title="Galeria de Fotos"><i class="bi-images"></i></a>
                <a href="/admin/produtos/alterar/{{produto.id}}" class="btn btn-success btn-sm" title="Alterar"><i class="bi-pencil"></i></a>
                <a href="/admin/produtos/excluir/{{produto.id}}" class="btn btn-danger btn-sm" title="Excluir"><i class="bi-trash"></i></a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

# templates/admin/usuarios/alterar.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <h1>Alterar Administrador</h1>
    
    {% if request.query_params.get('erro') == 'email_existe' %}
    <div class="alert alert-danger" role="alert">
        Este e-mail já está cadastrado no sistema!
    </div>
    {% endif %}
    
    <form method="post" action="/admin/usuarios/alterar/{{ usuario.id }}">
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="nome" class="form-label">Nome</label>
                    <input type="text" class="form-control" id="nome" name="nome" 
                           value="{{ usuario.nome }}" required autofocus>
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="email" class="form-label">E-mail</label>
                    <input type="email" class="form-control" id="email" name="email" 
                           value="{{ usuario.email }}" required>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="senha" class="form-label">Nova Senha (opcional)</label>
                    <input type="password" class="form-control" id="senha" name="senha" minlength="6">
                    <div class="form-text">Deixe em branco para manter a senha atual</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="confirmar_senha" class="form-label">Confirmar Nova Senha</label>
                    <input type="password" class="form-control" id="confirmar_senha" minlength="6">
                </div>
            </div>
        </div>
        
        <button type="submit" class="btn btn-success">
            <i class="bi-check-lg"></i> Salvar
        </button>
        <a href="/admin/usuarios/lista" class="btn btn-secondary">
            <i class="bi-x-lg"></i> Cancelar
        </a>
    </form>
</div>

<script>
// Validação de senha
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    // Se uma senha foi digitada, verificar se as duas coincidem
    if (senha && senha !== confirmarSenha) {
        e.preventDefault();
        alert('As senhas não coincidem!');
        document.getElementById('confirmar_senha').focus();
    }
    
    // Se confirmar senha foi digitada mas senha não
    if (confirmarSenha && !senha) {
        e.preventDefault();
        alert('Digite a nova senha primeiro!');
        document.getElementById('senha').focus();
    }
});
</script>
{% endblock %}
```

# templates/admin/usuarios/cadastro.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <h1>Cadastro de Administrador</h1>
    
    {% if request.query_params.get('erro') == 'email_existe' %}
    <div class="alert alert-danger" role="alert">
        Este e-mail já está cadastrado no sistema!
    </div>
    {% endif %}
    
    <form method="post" action="/admin/usuarios/cadastro">
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="nome" class="form-label">Nome</label>
                    <input type="text" class="form-control" id="nome" name="nome" required autofocus>
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="email" class="form-label">E-mail</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="senha" class="form-label">Senha</label>
                    <input type="password" class="form-control" id="senha" name="senha" 
                           minlength="6" required>
                    <div class="form-text">Mínimo 6 caracteres</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="confirmar_senha" class="form-label">Confirmar Senha</label>
                    <input type="password" class="form-control" id="confirmar_senha" 
                           minlength="6" required>
                </div>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">
            <i class="bi-check-lg"></i> Cadastrar
        </button>
        <a href="/admin/usuarios/lista" class="btn btn-secondary">
            <i class="bi-x-lg"></i> Cancelar
        </a>
    </form>
</div>

<script>
// Validação de senha
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha !== confirmarSenha) {
        e.preventDefault();
        alert('As senhas não coincidem!');
        document.getElementById('confirmar_senha').focus();
    }
});
</script>
{% endblock %}
```

# templates/admin/usuarios/excluir.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Confirmar Exclusão</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning">
                        <i class="bi-exclamation-triangle"></i>
                        <strong>Atenção!</strong> Esta ação não pode ser desfeita.
                    </div>
                    
                    <p>Tem certeza que deseja excluir o administrador?</p>
                    
                    <div class="bg-light p-3 rounded mb-3">
                        <strong>Nome:</strong> {{ usuario.nome }}<br>
                        <strong>E-mail:</strong> {{ usuario.email }}<br>
                        <strong>ID:</strong> {{ usuario.id }}
                    </div>
                    
                    <form method="post" action="/admin/usuarios/excluir/{{ usuario.id }}">
                        <button type="submit" class="btn btn-danger">
                            <i class="bi-trash"></i> Confirmar Exclusão
                        </button>
                        <a href="/admin/usuarios/lista" class="btn btn-secondary">
                            <i class="bi-x-lg"></i> Cancelar
                        </a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/admin/usuarios/lista.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <h1>Administradores</h1>
    
    {% if request.query_params.get('erro') == 'auto_exclusao' %}
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        Você não pode excluir seu próprio usuário!
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endif %}
    
    <a href="/admin/usuarios/cadastro" class="btn btn-primary mb-3">
        <i class="bi-plus-circle"></i> Novo Administrador
    </a>
    
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>E-mail</th>
                    <th>Data Cadastro</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for usuario in usuarios %}
                <tr>
                    <td>{{ usuario.id }}</td>
                    <td>{{ usuario.nome }}</td>
                    <td>{{ usuario.email }}</td>
                    <td>{{ usuario.data_cadastro }}</td>
                    <td>
                        <a href="/admin/usuarios/alterar/{{ usuario.id }}" class="btn btn-sm btn-success">
                            <i class="bi-pencil"></i> Alterar
                        </a>
                        {% if usuario.id != request.session.get('usuario').id %}
                        <a href="/admin/usuarios/excluir/{{ usuario.id }}" class="btn btn-sm btn-danger">
                            <i class="bi-trash"></i> Excluir
                        </a>
                        {% else %}
                        <span class="text-muted">
                            <small>(você)</small>
                        </span>
                        {% endif %}
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" class="text-center">Nenhum administrador cadastrado</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

# templates/auth/cadastro.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow">
                <div class="card-body p-5">
                    <h2 class="text-center mb-4">Criar Conta</h2>
                    
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}
                    
                    <form method="post" action="/cadastro">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" id="nome" name="nome" 
                                           placeholder="Nome Completo" value="{{ nome if nome }}" required autofocus>
                                    <label for="nome">Nome Completo</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" id="cpf" name="cpf" 
                                           placeholder="CPF" value="{{ cpf if cpf }}" 
                                           pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Formato: 000.000.000-00" required>
                                    <label for="cpf">CPF</label>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="tel" class="form-control" id="telefone" name="telefone" 
                                           placeholder="Telefone" value="{{ telefone if telefone }}"
                                           pattern="\(\d{2}\) \d{4,5}-\d{4}" title="Formato: (00) 0000-0000 ou (00) 00000-0000" required>
                                    <label for="telefone">Telefone</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-floating mb-3">
                            <input type="email" class="form-control" id="email" name="email" 
                                   placeholder="E-mail" value="{{ email if email }}" required>
                            <label for="email">E-mail</label>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="password" class="form-control" id="senha" name="senha" 
                                           placeholder="Senha" minlength="6" required>
                                    <label for="senha">Senha</label>
                                    <div class="form-text">Mínimo 6 caracteres</div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="password" class="form-control" id="confirmar_senha" name="confirmar_senha" 
                                           placeholder="Confirmar Senha" minlength="6" required>
                                    <label for="confirmar_senha">Confirmar Senha</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-success btn-lg">
                                <i class="bi-person-plus"></i> Criar Conta
                            </button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <p class="mb-0">Já tem uma conta?</p>
                        <a href="/login" class="btn btn-outline-primary mt-2">
                            <i class="bi-box-arrow-in-right"></i> Fazer Login
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Máscaras para CPF e Telefone
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

document.getElementById('telefone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
        if (value.length === 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else {
            value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        }
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/(\d{0,2})/, '($1');
    }
    e.target.value = value;
});

// Validação de senha
document.querySelector('form').addEventListener('submit', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha !== confirmarSenha) {
        e.preventDefault();
        alert('As senhas não coincidem!');
        document.getElementById('confirmar_senha').focus();
    }
});
</script>
{% endblock %}
```

# templates/auth/esqueci_senha.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow">
                <div class="card-body p-5">
                    <h2 class="text-center mb-4">Recuperar Senha</h2>
                    
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}
                    
                    {% if sucesso %}
                    <div class="alert alert-success" role="alert">
                        {{ sucesso }}
                    </div>
                    
                    {% if debug_link %}
                    <!-- REMOVER EM PRODUÇÃO - Apenas para teste -->
                    <div class="alert alert-warning" role="alert">
                        <strong>Link de teste (remover em produção):</strong><br>
                        <a href="{{ debug_link }}" target="_blank">{{ debug_link }}</a>
                    </div>
                    {% endif %}
                    
                    <div class="text-center mt-3">
                        <a href="/login" class="btn btn-primary">
                            <i class="bi-arrow-left"></i> Voltar ao Login
                        </a>
                    </div>
                    {% else %}
                    
                    <p class="text-muted mb-4">
                        Digite seu e-mail cadastrado e enviaremos instruções para redefinir sua senha.
                    </p>
                    
                    <form method="post" action="/esqueci-senha">
                        <div class="form-floating mb-3">
                            <input type="email" class="form-control" id="email" name="email" 
                                   placeholder="E-mail" required autofocus>
                            <label for="email">E-mail cadastrado</label>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="bi-envelope"></i> Enviar Instruções
                            </button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <a href="/login" class="text-decoration-none">
                            <i class="bi-arrow-left"></i> Voltar ao Login
                        </a>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/auth/login.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow">
                <div class="card-body p-5">
                    <h2 class="text-center mb-4">Login</h2>
                    
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}
                    
                    <form method="post" action="/login">
                        {% if redirect %}
                        <input type="hidden" name="redirect" value="{{ redirect }}">
                        {% endif %}
                        
                        <div class="form-floating mb-3">
                            <input type="email" class="form-control" id="email" name="email" 
                                   placeholder="E-mail" value="{{ email if email }}" required autofocus>
                            <label for="email">E-mail</label>
                        </div>
                        
                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" id="senha" name="senha" 
                                   placeholder="Senha" required>
                            <label for="senha">Senha</label>
                        </div>
                        
                        <div class="mb-3">
                            <a href="/esqueci-senha" class="text-decoration-none">Esqueceu sua senha?</a>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="bi-box-arrow-in-right"></i> Entrar
                            </button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <p class="mb-0">Não tem uma conta?</p>
                        <a href="/cadastro" class="btn btn-outline-success mt-2">
                            <i class="bi-person-plus"></i> Criar Conta
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

# templates/auth/redefinir_senha.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow">
                <div class="card-body p-5">
                    <h2 class="text-center mb-4">Redefinir Senha</h2>
                    
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}
                    
                    {% if sucesso %}
                    <div class="alert alert-success" role="alert">
                        {{ sucesso }}
                    </div>
                    <div class="text-center mt-3">
                        <a href="/login" class="btn btn-primary btn-lg">
                            <i class="bi-box-arrow-in-right"></i> Fazer Login
                        </a>
                    </div>
                    {% elif not erro or token %}
                    
                    <p class="text-muted mb-4">
                        Digite sua nova senha abaixo.
                    </p>
                    
                    <form method="post" action="/redefinir-senha/{{ token }}">
                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" id="senha" name="senha" 
                                   placeholder="Nova Senha" minlength="6" required autofocus>
                            <label for="senha">Nova Senha</label>
                            <div class="form-text">Mínimo 6 caracteres</div>
                        </div>
                        
                        <div class="form-floating mb-3">
                            <input type="password" class="form-control" id="confirmar_senha" name="confirmar_senha" 
                                   placeholder="Confirmar Nova Senha" minlength="6" required>
                            <label for="confirmar_senha">Confirmar Nova Senha</label>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-success btn-lg">
                                <i class="bi-key"></i> Redefinir Senha
                            </button>
                        </div>
                    </form>
                    {% else %}
                    <div class="text-center">
                        <a href="/esqueci-senha" class="btn btn-primary">
                            <i class="bi-envelope"></i> Solicitar novo link
                        </a>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Validação de senha
if (document.querySelector('form')) {
    document.querySelector('form').addEventListener('submit', function(e) {
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmar_senha').value;
        
        if (senha !== confirmarSenha) {
            e.preventDefault();
            alert('As senhas não coincidem!');
            document.getElementById('confirmar_senha').focus();
        }
    });
}
</script>
{% endblock %}
```

# templates/base.html

```html
<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="/static/img/favicon.png" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <title>Loja Virtual</title>
</head>

<body class="d-flex flex-column min-vh-100">
    <header class="text-bg-dark p-3">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <h1>Loja Virtual</h1>
                <div class="nav">
                    <a class="nav-link text-white" href="/">Home</a>
                    {% if request.session.get('usuario') and request.session.get('usuario').perfil == 'admin' %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                            Administrar
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="/admin/categorias">Categorias</a></li>
                            <li><a class="dropdown-item" href="/admin/produtos">Produtos</a></li>
                            <li><a class="dropdown-item" href="/admin/clientes">Clientes</a></li>
                            <li><a class="dropdown-item" href="/admin/formas">Formas de Pagamento</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/admin/usuarios/lista">Administradores</a></li>
                        </ul>
                    </li>
                    {% endif %}
                    
                    {% if request.session.get('usuario') %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                            {% if request.session.get('usuario').foto %}
                            <img src="{{ request.session.get('usuario').foto }}" 
                                 class="rounded-circle" 
                                 style="width: 30px; height: 30px; object-fit: cover;">
                            {% else %}
                            <i class="bi-person-circle"></i>
                            {% endif %}
                            {{ request.session.get('usuario').nome }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="/perfil">
                                <i class="bi-person"></i> Meu Perfil
                            </a></li>
                            <li><a class="dropdown-item" href="/perfil/alterar-senha">
                                <i class="bi-key"></i> Alterar Senha
                            </a></li>
                            {% if request.session.get('usuario').perfil == 'cliente' %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/perfil/pedidos">
                                <i class="bi-bag"></i> Meus Pedidos
                            </a></li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/logout">
                                <i class="bi-box-arrow-right"></i> Sair
                            </a></li>
                        </ul>
                    </li>
                    {% else %}
                    <a class="nav-link text-white" href="/login">
                        <i class="bi-box-arrow-in-right"></i> Login
                    </a>
                    <a class="nav-link text-white" href="/cadastro">
                        <i class="bi-person-plus"></i> Cadastre-se
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
        </div>
    </header>
    <main class="container my-3">
        {% if mensagem %}
        <div class="alert alert-success" role="alert">
            {{ mensagem }}
        </div>
        {% endif %}
        {% block conteudo %}
        {% endblock %}
    </main>
    <footer class="text-bg-dark p-3 text-center mt-auto">
        <p class="m-0">Copyright &copy; 2025 Loja Virtual</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
```

# templates/index.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-6 g-3">
    {% for p in produtos %}
    <div class="col">
        <div class="card h-100">
            <img class="card-img-top" src="{{ p.foto_principal or '/static/img/placeholder.png' }}" alt="{{p.nome}}" style="height: 200px; object-fit: cover;" />
            <div class="card-body">
                <h4 class="card-title">{{p.nome}}</h4>
                <p class="card-text">
                    {{p.descricao}}
                </p>
                <p class="card-text">
                    R$ {{p.preco}}
                </p>
            </div>
            <div class="card-footer p-2">
                <a class="btn btn-danger w-100" href="/produtos/{{p.id}}">Ver Detalhes</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}

```

# templates/perfil/alterar_senha.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-3">
            <div class="list-group mb-3">
                <a href="/perfil" class="list-group-item list-group-item-action">
                    <i class="bi-person"></i> Meus Dados
                </a>
                <a href="/perfil/alterar-senha" class="list-group-item list-group-item-action active">
                    <i class="bi-key"></i> Alterar Senha
                </a>
                {% if request.session.get('usuario').perfil == 'cliente' %}
                <a href="/perfil/pedidos" class="list-group-item list-group-item-action">
                    <i class="bi-bag"></i> Meus Pedidos
                </a>
                <a href="/perfil/enderecos" class="list-group-item list-group-item-action">
                    <i class="bi-geo-alt"></i> Endereços
                </a>
                {% endif %}
            </div>

            <div class="card">
                <div class="card-body text-center">
                    <img src="{{ request.session.get('usuario').foto or '/static/img/user-default.png' }}" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;" alt="Foto do perfil">
                    <h5>{{ request.session.get('usuario').nome }}</h5>
                    <p class="text-muted mb-0">{{ request.session.get('usuario').perfil|title }}</p>
                </div>
            </div>
        </div>

        <div class="col-md-9">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Alterar Senha</h4>
                </div>
                <div class="card-body">
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}

                    {% if sucesso %}
                    <div class="alert alert-success" role="alert">
                        {{ sucesso }}
                    </div>
                    {% endif %}

                    <form method="post" action="/perfil/alterar-senha">
                        <div class="mb-3">
                            <label for="senha_atual" class="form-label">Senha Atual</label>
                            <input type="password" class="form-control" id="senha_atual" name="senha_atual" required autofocus>
                        </div>

                        <div class="mb-3">
                            <label for="senha_nova" class="form-label">Nova Senha</label>
                            <input type="password" class="form-control" id="senha_nova" name="senha_nova" minlength="6" required>
                            <div class="form-text">
                                A senha deve ter no mínimo 6 caracteres
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="confirmar_senha" class="form-label">Confirmar Nova Senha</label>
                            <input type="password" class="form-control" id="confirmar_senha" name="confirmar_senha" minlength="6" required>
                        </div>

                        <button type="submit" class="btn btn-success">
                            <i class="bi-check-lg"></i> Alterar Senha
                        </button>
                        <a href="/perfil" class="btn btn-secondary">
                            <i class="bi-x-lg"></i> Cancelar
                        </a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // Validação de senha
    document.querySelector('form').addEventListener('submit', function (e) {
        const senhaNova = document.getElementById('senha_nova').value;
        const confirmarSenha = document.getElementById('confirmar_senha').value;

        if (senhaNova !== confirmarSenha) {
            e.preventDefault();
            alert('As novas senhas não coincidem!');
            document.getElementById('confirmar_senha').focus();
        }
    });
</script>
{% endblock %}
```

# templates/perfil/dados.html

```html
{% extends "base.html" %}
{% block conteudo %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-3">
            <div class="list-group mb-3">
                <a href="/perfil" class="list-group-item list-group-item-action active">
                    <i class="bi-person"></i> Meus Dados
                </a>
                <a href="/perfil/alterar-senha" class="list-group-item list-group-item-action">
                    <i class="bi-key"></i> Alterar Senha
                </a>
                {% if usuario.perfil == 'cliente' %}
                <a href="/perfil/pedidos" class="list-group-item list-group-item-action">
                    <i class="bi-bag"></i> Meus Pedidos
                </a>
                <a href="/perfil/enderecos" class="list-group-item list-group-item-action">
                    <i class="bi-geo-alt"></i> Endereços
                </a>
                {% endif %}
            </div>

            <div class="card">
                <div class="card-body text-center">
                    <div class="d-flex justify-content-center">
                        <img id="foto-atual" src="{{ usuario.foto or '/static/img/user-default.png' }}"
                             class="rounded-circle mb-3"
                             style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #dee2e6;"
                             alt="Foto do perfil">
                    </div>

                    <!-- Preview da nova foto -->
                    <div id="preview-foto-container" style="display: none;">
                        <div class="d-flex justify-content-center">
                            <img id="preview-foto" src=""
                                 class="rounded-circle mb-2"
                                 style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #28a745;"
                                 alt="Preview da nova foto">
                        </div>
                        <div class="small text-success mb-2">
                            <i class="bi-check-circle"></i> Nova foto selecionada
                        </div>
                    </div>

                    <h5>{{ usuario.nome }}</h5>
                    <p class="text-muted">{{ usuario.perfil|title }}</p>

                    <hr>

                    <form action="/perfil/alterar-foto" method="post" enctype="multipart/form-data" id="form-foto">
                        <div class="mb-2">
                            <label for="foto" class="form-label small">Selecionar Nova Foto</label>
                            <input type="file" class="form-control form-control-sm"
                                   id="foto" name="foto" accept="image/*">
                            <div class="form-text small">JPG, JPEG ou PNG</div>
                        </div>
                        <button type="submit" class="btn btn-sm btn-outline-primary" id="btn-alterar" disabled>
                            <i class="bi-camera"></i> Alterar Foto
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-secondary" id="btn-cancelar" onclick="cancelarSelecao()" style="display: none;">
                            <i class="bi-x"></i> Cancelar
                        </button>
                    </form>
                </div>
            </div>            
        </div>
        
        <div class="col-md-9">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Meus Dados</h4>
                </div>
                <div class="card-body">
                    {% if request.query_params.get('sucesso') %}
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        Dados atualizados com sucesso!
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endif %}
                    
                    {% if request.query_params.get('foto_sucesso') %}
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        Foto atualizada com sucesso!
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endif %}
                    
                    {% if request.query_params.get('erro') == 'tipo_invalido' %}
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Tipo de arquivo inválido! Use apenas JPG, JPEG ou PNG.
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endif %}
                    
                    {% if request.query_params.get('erro') == 'upload_falhou' %}
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Erro ao fazer upload da foto. Tente novamente.
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                    {% endif %}
                    
                    {% if erro %}
                    <div class="alert alert-danger" role="alert">
                        {{ erro }}
                    </div>
                    {% endif %}
                    
                    <form method="post" action="/perfil">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="mb-3">
                                    <label for="nome" class="form-label">Nome Completo</label>
                                    <input type="text" class="form-control" id="nome" name="nome" 
                                           value="{{ usuario.nome }}" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-12">
                                <div class="mb-3">
                                    <label for="email" class="form-label">E-mail</label>
                                    <input type="email" class="form-control" id="email" name="email" 
                                           value="{{ usuario.email }}" required>
                                </div>
                            </div>
                        </div>
                        
                        {% if usuario.perfil == 'cliente' and cliente_dados %}
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="cpf" class="form-label">CPF</label>
                                    <input type="text" class="form-control" id="cpf" name="cpf" 
                                           value="{{ cliente_dados.cpf }}" 
                                           pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" 
                                           title="Formato: 000.000.000-00">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="telefone" class="form-label">Telefone</label>
                                    <input type="tel" class="form-control" id="telefone" name="telefone" 
                                           value="{{ cliente_dados.telefone }}"
                                           pattern="\(\d{2}\) \d{4,5}-\d{4}" 
                                           title="Formato: (00) 0000-0000 ou (00) 00000-0000">
                                </div>
                            </div>
                        </div>
                        {% endif %}
                        
                        <div class="row">
                            <div class="col-md-12">
                                <div class="mb-3">
                                    <label class="form-label">Data de Cadastro</label>
                                    <input type="text" class="form-control" value="{{ usuario.data_cadastro }}" readonly disabled>
                                </div>
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-success">
                            <i class="bi-check-lg"></i> Salvar Alterações
                        </button>
                        <a href="/" class="btn btn-secondary">
                            <i class="bi-x-lg"></i> Cancelar
                        </a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Preview de foto de perfil
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Esconder foto atual e mostrar preview
                    fotoAtual.style.display = 'none';
                    previewFoto.src = e.target.result;
                    previewContainer.style.display = 'block';

                    // Habilitar botão e mostrar opções
                    btnAlterar.disabled = false;
                    btnAlterar.textContent = ' Confirmar Alteração';
                    btnAlterar.innerHTML = '<i class="bi-check"></i> Confirmar Alteração';
                    btnCancelar.style.display = 'inline-block';
                };

                reader.readAsDataURL(file);
            } else {
                alert('Por favor, selecione apenas arquivos de imagem (JPG, JPEG ou PNG).');
                cancelarSelecao();
            }
        } else {
            cancelarSelecao();
        }
    });
});

function cancelarSelecao() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Limpar seleção
    fotoInput.value = '';

    // Mostrar foto atual e esconder preview
    fotoAtual.style.display = 'block';
    previewContainer.style.display = 'none';

    // Resetar botões
    btnAlterar.disabled = true;
    btnAlterar.innerHTML = '<i class="bi-camera"></i> Alterar Foto';
    btnCancelar.style.display = 'none';
}
</script>

{% if usuario.perfil == 'cliente' and cliente_dados %}
<script>
// Máscaras para CPF e Telefone
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

document.getElementById('telefone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    if (value.length > 6) {
        if (value.length === 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else {
            value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
        }
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/(\d{0,2})/, '($1');
    }
    e.target.value = value;
});
</script>
{% endif %}
{% endblock %}
```

# util/__init__.py

```py
# Pacote util - Funções utilitárias para o projeto
```

# util/auth_decorator.py

```py
"""
Decorator para proteger rotas com autenticação e autorização
"""
from functools import wraps
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse


def obter_usuario_logado(request: Request) -> Optional[dict]:
    """
    Obtém os dados do usuário logado da sessão
    
    Args:
        request: Objeto Request do FastAPI
    
    Returns:
        Dicionário com dados do usuário ou None se não estiver logado
    """
    if not hasattr(request, 'session'):
        return None
    return request.session.get('usuario')


def esta_logado(request: Request) -> bool:
    """
    Verifica se há um usuário logado
    
    Args:
        request: Objeto Request do FastAPI
    
    Returns:
        True se há usuário logado, False caso contrário
    """
    return obter_usuario_logado(request) is not None


def criar_sessao(request: Request, usuario: dict) -> None:
    """
    Cria uma sessão para o usuário após login
    
    Args:
        request: Objeto Request do FastAPI
        usuario: Dicionário com dados do usuário
    """
    if hasattr(request, 'session'):
        # Remove senha da sessão por segurança
        usuario_sessao = usuario.copy()
        usuario_sessao.pop('senha', None)
        request.session['usuario'] = usuario_sessao


def destruir_sessao(request: Request) -> None:
    """
    Destrói a sessão do usuário (logout)
    
    Args:
        request: Objeto Request do FastAPI
    """
    if hasattr(request, 'session'):
        request.session.clear()


def requer_autenticacao(perfis_autorizados: List[str] = None):
    """
    Decorator para proteger rotas que requerem autenticação
    
    Args:
        perfis_autorizados: Lista de perfis autorizados a acessar a rota.
                           Se None, qualquer usuário logado pode acessar.
    
    Exemplo de uso:
        @router.get("/admin")
        @requer_autenticacao(['admin'])
        async def admin_page(request: Request):
            ...
        
        @router.get("/perfil")
        @requer_autenticacao()  # Qualquer usuário logado
        async def perfil(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontra o objeto Request nos argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            # Verifica se o usuário está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                # Redireciona para login se não estiver autenticado
                return RedirectResponse(
                    url="/login?redirect=" + str(request.url.path),
                    status_code=status.HTTP_303_SEE_OTHER
                )
            
            # Verifica autorização se perfis foram especificados
            if perfis_autorizados:
                perfil_usuario = usuario.get('perfil', 'cliente')
                if perfil_usuario not in perfis_autorizados:
                    # Retorna erro 403 se não autorizado
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Você não tem permissão para acessar este recurso"
                    )
            
            # Adiciona o usuário aos kwargs para fácil acesso na rota
            kwargs['usuario_logado'] = usuario
            
            # Chama a função original
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Importação necessária para funções assíncronas
import asyncio
```

# util/criar_admin.py

```py
from util.security import criar_hash_senha
from repo import usuario_repo
from model.usuario_model import Usuario

def criar_admin_padrao():
    """Cria um usuário administrador padrão se não existir"""
    
    # Verificar se já existe algum admin
    admins = usuario_repo.obter_todos_por_perfil("admin")
    
    if not admins:
        # Criar admin padrão
        senha_hash = criar_hash_senha("admin123")
        admin = Usuario(
            id=0,
            nome="Administrador",
            email="admin@admin.com",
            senha=senha_hash,
            perfil="admin"
        )
        
        usuario_repo.inserir(admin)
        print("Admin padrão criado com sucesso!")
        print("E-mail: admin@admin.com")
        print("Senha: admin123")
        print("IMPORTANTE: Altere a senha após o primeiro login!")
        return True
    
    return False

if __name__ == "__main__":
    criar_admin_padrao()
```

# util/db_util.py

```py
import sqlite3


def get_connection():
    conn = None
    try:
        conn = sqlite3.connect("dados.db")
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(e)
    return conn

```

# util/foto_util.py

```py
import os
from PIL import Image
from typing import List, Optional


def obter_diretorio_produto(produto_id: int) -> str:
    """Retorna o caminho do diretório de fotos de um produto"""
    codigo_produto = f"{produto_id:06d}"
    # Usar caminho relativo ao diretório atual
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", "img", "products", codigo_produto)


def obter_url_diretorio_produto(produto_id: int) -> str:
    """Retorna a URL do diretório de fotos de um produto"""
    codigo_produto = f"{produto_id:06d}"
    return f"/static/img/products/{codigo_produto}"


def criar_diretorio_produto(produto_id: int) -> bool:
    """Cria o diretório de fotos do produto se não existir"""
    try:
        diretorio = obter_diretorio_produto(produto_id)
        os.makedirs(diretorio, exist_ok=True)
        return True
    except:
        return False


def processar_imagem(arquivo, caminho_destino: str) -> bool:
    """
    Processa uma imagem: corta para quadrado, redimensiona e salva como JPG
    """
    try:
        # Abrir a imagem
        img = Image.open(arquivo)

        # Converter para RGB se necessário (para salvar como JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Cortar para quadrado (centro da imagem)
        largura, altura = img.size
        tamanho = min(largura, altura)

        left = (largura - tamanho) // 2
        top = (altura - tamanho) // 2
        right = left + tamanho
        bottom = top + tamanho

        img = img.crop((left, top, right, bottom))

        # Redimensionar para tamanho padrão
        img = img.resize((800, 800), Image.Resampling.LANCZOS)

        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # Salvar como JPG
        img.save(caminho_destino, 'JPEG', quality=85, optimize=True)

        return True
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return False


def obter_foto_principal(produto_id: int) -> Optional[str]:
    """Retorna a URL da foto principal do produto ou None se não existir"""
    codigo_produto = f"{produto_id:06d}"
    caminho_foto = obter_diretorio_produto(produto_id) + f"/{codigo_produto}-001.jpg"

    if os.path.exists(caminho_foto):
        return f"/static/img/products/{codigo_produto}/{codigo_produto}-001.jpg"
    return None


def obter_todas_fotos(produto_id: int) -> List[str]:
    """Retorna lista de URLs de todas as fotos do produto ordenadas"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return []

    fotos = []
    arquivos = os.listdir(diretorio)

    # Filtrar apenas arquivos JPG do produto
    for arquivo in arquivos:
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            fotos.append(f"/static/img/products/{codigo_produto}/{arquivo}")

    # Ordenar por número sequencial
    fotos.sort()
    return fotos


def obter_proximo_numero(produto_id: int) -> int:
    """Retorna o próximo número sequencial disponível para uma nova foto"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return 1

    numeros = []
    arquivos = os.listdir(diretorio)

    for arquivo in arquivos:
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            # Extrair número do arquivo (XXXXXX-NNN.jpg)
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numeros.append(int(numero_str))
            except:
                continue

    if not numeros:
        return 1

    return max(numeros) + 1


def excluir_foto(produto_id: int, numero: int) -> bool:
    """Remove uma foto específica e reordena as restantes"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    # Remover o arquivo específico
    caminho_foto = f"{diretorio}/{codigo_produto}-{numero:03d}.jpg"

    if os.path.exists(caminho_foto):
        try:
            os.remove(caminho_foto)
        except:
            return False

    # Reordenar fotos restantes
    return reordenar_fotos_automatico(produto_id)


def reordenar_fotos_automatico(produto_id: int) -> bool:
    """Reordena automaticamente as fotos para não ter gaps na numeração"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return True

    # Obter todas as fotos ordenadas
    arquivos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            arquivos.append(arquivo)

    arquivos.sort()

    # Renomear temporariamente para evitar conflitos
    temp_files = []
    for i, arquivo in enumerate(arquivos):
        caminho_original = f"{diretorio}/{arquivo}"
        caminho_temp = f"{diretorio}/temp_{i:03d}.jpg"
        try:
            os.rename(caminho_original, caminho_temp)
            temp_files.append(caminho_temp)
        except:
            return False

    # Renomear para a sequência final
    for i, caminho_temp in enumerate(temp_files):
        novo_numero = i + 1
        caminho_final = f"{diretorio}/{codigo_produto}-{novo_numero:03d}.jpg"
        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True


def reordenar_fotos(produto_id: int, nova_ordem: List[int]) -> bool:
    """Reordena as fotos conforme a nova ordem especificada"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return False

    # Mapear arquivos existentes
    arquivos_existentes = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numero = int(numero_str)
                arquivos_existentes[numero] = arquivo
            except:
                continue

    # Validar nova ordem
    if len(nova_ordem) != len(arquivos_existentes):
        return False

    # Renomear temporariamente
    temp_files = {}
    for i, numero_original in enumerate(nova_ordem):
        if numero_original not in arquivos_existentes:
            return False

        arquivo_original = arquivos_existentes[numero_original]
        caminho_original = f"{diretorio}/{arquivo_original}"
        caminho_temp = f"{diretorio}/temp_{i:03d}.jpg"

        try:
            os.rename(caminho_original, caminho_temp)
            temp_files[i] = caminho_temp
        except:
            return False

    # Renomear para a sequência final
    for i in range(len(nova_ordem)):
        novo_numero = i + 1
        caminho_temp = temp_files[i]
        caminho_final = f"{diretorio}/{codigo_produto}-{novo_numero:03d}.jpg"

        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True


def salvar_nova_foto(produto_id: int, arquivo, como_principal: bool = False) -> bool:
    """Salva uma nova foto do produto"""
    criar_diretorio_produto(produto_id)
    codigo_produto = f"{produto_id:06d}"

    if como_principal:
        # Salvar como foto principal (001)
        numero = 1
        # Se já existe foto principal, mover as outras
        if obter_foto_principal(produto_id):
            _mover_fotos_para_frente(produto_id)
    else:
        # Adicionar como próxima foto
        numero = obter_proximo_numero(produto_id)

    caminho_destino = f"{obter_diretorio_produto(produto_id)}/{codigo_produto}-{numero:03d}.jpg"
    return processar_imagem(arquivo, caminho_destino)


def _mover_fotos_para_frente(produto_id: int):
    """Move todas as fotos existentes uma posição para frente"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    arquivos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            arquivos.append(arquivo)

    # Ordenar em ordem reversa para não sobrescrever
    arquivos.sort(reverse=True)

    for arquivo in arquivos:
        try:
            numero_str = arquivo.split('-')[1].split('.')[0]
            numero_atual = int(numero_str)
            novo_numero = numero_atual + 1

            caminho_atual = f"{diretorio}/{arquivo}"
            novo_arquivo = f"{codigo_produto}-{novo_numero:03d}.jpg"
            caminho_novo = f"{diretorio}/{novo_arquivo}"

            os.rename(caminho_atual, caminho_novo)
        except:
            continue
```

# util/security.py

```py
"""
Módulo de segurança para gerenciar senhas e tokens
"""
import secrets
import string
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Contexto para hash de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash seguro da senha usando bcrypt
    
    Args:
        senha: Senha em texto plano
    
    Returns:
        Hash da senha
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash
    
    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenado no banco
    
    Returns:
        True se a senha está correta, False caso contrário
    """
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except:
        return False


def gerar_token_redefinicao(tamanho: int = 32) -> str:
    """
    Gera um token aleatório seguro para redefinição de senha
    
    Args:
        tamanho: Tamanho do token em caracteres
    
    Returns:
        Token aleatório
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Calcula a data de expiração do token
    
    Args:
        horas: Número de horas de validade do token
    
    Returns:
        Data de expiração no formato ISO
    """
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    """
    Valida se a senha atende aos requisitos mínimos de segurança
    
    Args:
        senha: Senha a ser validada
    
    Returns:
        Tupla (válida, mensagem de erro se inválida)
    """
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    
    # Adicione mais validações conforme necessário
    # if not any(c.isupper() for c in senha):
    #     return False, "A senha deve conter pelo menos uma letra maiúscula"
    # if not any(c.islower() for c in senha):
    #     return False, "A senha deve conter pelo menos uma letra minúscula"
    # if not any(c.isdigit() for c in senha):
    #     return False, "A senha deve conter pelo menos um número"
    
    return True, ""


def gerar_senha_aleatoria(tamanho: int = 8) -> str:
    """
    Gera uma senha aleatória segura
    
    Args:
        tamanho: Tamanho da senha
    
    Returns:
        Senha aleatória
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%"
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha
```

# util/template_util.py

```py
from typing import List, Optional, Union
from jinja2 import FileSystemLoader
from fastapi.templating import Jinja2Templates


def criar_templates(diretorio_especifico: Optional[Union[str, List[str]]] = None) -> Jinja2Templates:
    """
    Cria um objeto Jinja2Templates configurado com múltiplos diretórios.
    
    O diretório raiz "templates" é sempre incluído automaticamente para garantir
    acesso aos templates base como base.html.
    
    Args:
        diretorio_especifico: Diretório(s) específico(s) além do raiz.
                             Pode ser uma string única ou lista de strings.
                             Exemplo: "templates/admin/categorias" ou
                                     ["templates/admin", "templates/public"]
    
    Returns:
        Objeto Jinja2Templates configurado com os diretórios especificados
    
    Exemplo de uso:
        # Para um diretório específico
        templates = criar_templates("templates/admin/categorias")
        
        # Para múltiplos diretórios
        templates = criar_templates(["templates/admin", "templates/admin/produtos"])
        
        # Apenas com o diretório raiz
        templates = criar_templates()
    """
    # Sempre incluir o diretório raiz onde estão os templates base
    diretorios = ["templates"]
    
    # Adicionar diretórios específicos se fornecidos
    if diretorio_especifico:
        if isinstance(diretorio_especifico, str):
            # Se for uma string única, adiciona à lista
            diretorios.append(diretorio_especifico)
        elif isinstance(diretorio_especifico, list):
            # Se for uma lista, estende a lista de diretórios
            diretorios.extend(diretorio_especifico)
    
    # Criar o objeto Jinja2Templates com diretório base como "."
    # Isso é necessário para que o FileSystemLoader funcione corretamente
    templates = Jinja2Templates(directory=".")
    
    # Configurar o loader com múltiplos diretórios
    # O FileSystemLoader tentará encontrar templates em ordem nos diretórios listados
    templates.env.loader = FileSystemLoader(diretorios)
    
    return templates
```

