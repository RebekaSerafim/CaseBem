from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.categoria_item_model import CategoriaItem
from model.item_model import TipoItem
from repo import usuario_repo, fornecedor_repo, item_repo, categoria_item_repo, orcamento_repo, demanda_repo
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==================== REDIRECIONAMENTO RAIZ ====================

@router.get("/admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def admin_root(request: Request, usuario_logado: dict = None):
    """Redireciona /admin para /admin/dashboard"""
    return RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)

# ==================== PERFIL ADMIN ====================

@router.get("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def perfil_admin(request: Request, usuario_logado: dict = None):
    """Página de perfil do administrador"""
    try:
        admin = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin
        })
    except Exception as e:
        print(f"Erro ao carregar perfil admin: {e}")
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar perfil"
        })

@router.post("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_perfil_admin(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    cargo: str = Form(""),
    endereco: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    observacoes: str = Form(""),
    usuario_logado: dict = None
):
    """Atualiza o perfil do administrador"""
    try:
        admin = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        if not admin:
            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Atualizar dados do usuário
        admin.nome = nome
        admin.email = email
        admin.telefone = telefone if telefone else None

        # Campos específicos do admin podem ser armazenados como propriedades customizadas
        # ou em uma tabela separada dependendo da implementação do banco

        sucesso = usuario_repo.atualizar_usuario(admin)

        if sucesso:
            # Atualizar a sessão com os novos dados
            usuario_logado['nome'] = nome
            usuario_logado['email'] = email

            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "sucesso": "Perfil atualizado com sucesso!"
            })
        else:
            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "erro": "Erro ao atualizar perfil"
            })

    except Exception as e:
        print(f"Erro ao atualizar perfil admin: {e}")
        admin = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "erro": "Erro ao atualizar perfil"
        })

# ==================== DASHBOARD ====================

@router.get("/admin/dashboard")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def dashboard_admin(request: Request, usuario_logado: dict = None):
    """Dashboard principal do administrador"""
    try:
        # Estatísticas do sistema
        stats = {
            "total_usuarios": usuario_repo.contar_usuarios(),
            "total_fornecedores": fornecedor_repo.contar_fornecedores(),
            "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
            "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
            "fornecedores_nao_verificados": fornecedor_repo.contar_fornecedores_nao_verificados(),
            "total_itens": item_repo.contar_itens(),
            "total_categorias": categoria_item_repo.contar_categorias(),
            "total_orcamentos": orcamento_repo.contar_orcamentos(),
            "total_demandas": demanda_repo.contar_demandas(),
            "estatisticas_itens": {
                "produtos": item_repo.contar_itens_por_tipo(TipoItem.PRODUTO),
                "servicos": item_repo.contar_itens_por_tipo(TipoItem.SERVICO),
                "espacos": item_repo.contar_itens_por_tipo(TipoItem.ESPACO)
            }
        }

        # Buscar fornecedores recentes
        fornecedores_recentes = fornecedor_repo.obter_fornecedores_por_pagina(1, 5)

        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats": stats,
            "fornecedores_recentes": fornecedores_recentes
        })
    except Exception as e:
        print(f"Erro no dashboard admin: {e}")
        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar estatísticas"
        })

# ==================== GESTÃO DE USUÁRIOS ====================

@router.get("/admin/usuarios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_usuarios(request: Request, usuario_logado: dict = None):
    """Lista todos os usuários do sistema com filtros"""
    try:
        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_usuario = request.query_params.get("tipo_usuario", "").strip()
        status = request.query_params.get("status", "").strip()

        # Aplicar filtros se fornecidos, senão listar todos
        if busca or tipo_usuario or status:
            usuarios = usuario_repo.buscar_usuarios(busca, tipo_usuario, status, 1, 100)
        else:
            usuarios = usuario_repo.obter_usuarios_por_pagina(1, 100)

        # Buscar dados de fornecedores para verificar status de verificação
        fornecedores_dados = {}
        for usuario in usuarios:
            if usuario.perfil == TipoUsuario.FORNECEDOR:
                fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario.id)
                if fornecedor:
                    fornecedores_dados[usuario.id] = fornecedor

        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuarios": usuarios,
            "fornecedores_dados": fornecedores_dados
        })
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuários"
        })

# ==================== GESTÃO DE ADMINISTRADORES ====================

@router.get("/admin/usuarios/novo-admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def novo_admin_form(request: Request, usuario_logado: dict = None):
    """Formulário para cadastrar novo administrador"""
    return templates.TemplateResponse("admin/admin_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar"
    })

@router.post("/admin/usuarios/criar-admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def criar_admin(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(""),
    telefone: str = Form(""),
    data_nascimento: str = Form(""),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    """Cria um novo administrador"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Nome é obrigatório"
            })

        # Validar se o email não está vazio
        email = email.strip()
        if not email:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Email é obrigatório"
            })

        # Verificar se já existe usuário com o mesmo email
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": f"Já existe um usuário cadastrado com o email {email}"
            })

        # Validar senha
        if not senha or len(senha) < 6:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Senha deve ter pelo menos 6 caracteres"
            })

        # Limpar campos opcionais
        cpf = cpf.strip() if cpf.strip() else None
        telefone = telefone.strip() if telefone.strip() else None
        data_nascimento = data_nascimento.strip() if data_nascimento.strip() else None

        # Hash da senha
        from util.security import criar_hash_senha
        senha_hash = criar_hash_senha(senha)

        # Criar objeto Usuario
        from model.usuario_model import Usuario
        novo_admin = Usuario(
            id=0,
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            senha=senha_hash,
            perfil=TipoUsuario.ADMIN,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            ativo=True
        )

        # Inserir no banco
        admin_id = usuario_repo.inserir_usuario(novo_admin)
        if admin_id:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Erro ao cadastrar administrador"
            })

    except Exception as e:
        print(f"Erro ao criar administrador: {e}")
        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "criar",
            "erro": "Erro interno do servidor"
        })

@router.get("/admin/usuarios/editar-admin/{id_admin}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def editar_admin_form(request: Request, id_admin: int, usuario_logado: dict = None):
    """Formulário para editar administrador"""
    try:
        admin = usuario_repo.obter_usuario_por_id(id_admin)
        if not admin or admin.perfil != TipoUsuario.ADMIN:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "acao": "editar"
        })
    except Exception as e:
        print(f"Erro ao carregar administrador para edição: {e}")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/atualizar-admin/{id_admin}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_admin(
    request: Request,
    id_admin: int,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(""),
    telefone: str = Form(""),
    data_nascimento: str = Form(""),
    usuario_logado: dict = None
):
    """Atualiza dados do administrador"""
    try:
        # Obter administrador atual
        admin = usuario_repo.obter_usuario_por_id(id_admin)
        if not admin or admin.perfil != TipoUsuario.ADMIN:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

        # Validar campos obrigatórios
        nome = nome.strip()
        email = email.strip()

        if not nome:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Nome é obrigatório"
            })

        if not email:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Email é obrigatório"
            })

        # Verificar se email já existe (exceto para o próprio usuário)
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente and usuario_existente.id != id_admin:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": f"Já existe outro usuário cadastrado com o email {email}"
            })

        # Atualizar dados
        admin.nome = nome
        admin.email = email
        admin.cpf = cpf.strip() if cpf.strip() else None
        admin.telefone = telefone.strip() if telefone.strip() else None
        admin.data_nascimento = data_nascimento.strip() if data_nascimento.strip() else None

        if usuario_repo.atualizar_usuario(admin):
            # Atualizar sessão se o admin editou a si mesmo
            if usuario_logado['id'] == id_admin:
                usuario_logado['nome'] = nome
                usuario_logado['email'] = email

            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Erro ao atualizar administrador"
            })

    except Exception as e:
        print(f"Erro ao atualizar administrador: {e}")
        admin = usuario_repo.obter_usuario_por_id(id_admin)
        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "acao": "editar",
            "erro": "Erro interno do servidor"
        })

@router.get("/admin/usuarios/{id_usuario}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def visualizar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    """Visualiza detalhes de um usuário específico"""
    try:
        usuario = usuario_repo.obter_usuario_por_id(id_usuario)

        if not usuario:
            return templates.TemplateResponse("admin/usuarios.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Se for fornecedor, buscar dados adicionais
        fornecedor = None
        if usuario.perfil == TipoUsuario.FORNECEDOR:
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_usuario)

        return templates.TemplateResponse("admin/usuario_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuario": usuario,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao visualizar usuário: {e}")
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuário"
        })

@router.post("/admin/usuarios/{id_usuario}/bloquear")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def bloquear_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    """Bloqueia um usuário"""
    try:
        sucesso = usuario_repo.bloquear_usuario(id_usuario)
        if sucesso:
            informar_sucesso(request, "Usuário bloqueado com sucesso!")
        else:
            informar_erro(request, "Erro ao bloquear usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao bloquear usuário: {e}")
        informar_erro(request, "Erro ao bloquear usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/{id_usuario}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    """Ativa um usuário"""
    try:
        sucesso = usuario_repo.ativar_usuario(id_usuario)
        if sucesso:
            informar_sucesso(request, "Usuário ativado com sucesso!")
        else:
            informar_erro(request, "Erro ao ativar usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao ativar usuário: {e}")
        informar_erro(request, "Erro ao ativar usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)


# ==================== VERIFICAÇÃO DE FORNECEDORES ====================

@router.get("/admin/verificacao/{id_fornecedor}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def verificacao_fornecedor_especifico(request: Request, id_fornecedor: int, usuario_logado: dict = None):
    """Página de verificação para um fornecedor específico"""
    try:
        # Buscar o usuário e dados do fornecedor
        usuario = usuario_repo.obter_usuario_por_id(id_fornecedor)
        if not usuario or usuario.perfil != TipoUsuario.FORNECEDOR:
            return templates.TemplateResponse("admin/verificacao.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Fornecedor não encontrado"
            })

        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            return templates.TemplateResponse("admin/verificacao.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Dados do fornecedor não encontrados"
            })

        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao carregar verificação: {e}")
        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar dados do fornecedor"
        })

@router.get("/admin/verificacao")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def verificacao_fornecedores(request: Request, usuario_logado: dict = None):
    """Lista fornecedores pendentes de verificação"""
    try:
        fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 100)
        fornecedores_pendentes = [f for f in fornecedores if not f.verificado]

        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedores_pendentes": fornecedores_pendentes
        })
    except Exception as e:
        print(f"Erro ao carregar verificação: {e}")
        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar fornecedores pendentes"
        })

@router.post("/admin/verificacao/{id_fornecedor}/aprovar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def aprovar_fornecedor(request: Request, id_fornecedor: int, usuario_logado: dict = None):
    """Aprova um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        fornecedor.verificado = True
        from datetime import datetime
        fornecedor.data_verificacao = datetime.now().isoformat()
        fornecedor_repo.atualizar_fornecedor(fornecedor)

        informar_sucesso(request, "Fornecedor aprovado com sucesso!")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao aprovar fornecedor: {e}")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/verificacao/{id_fornecedor}/rejeitar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def rejeitar_fornecedor(request: Request, id_fornecedor: int, observacoes: str = Form(""), usuario_logado: dict = None):
    """Rejeita um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        # Rejeitar fornecedor (remover verificação)
        sucesso = fornecedor_repo.rejeitar_fornecedor(id_fornecedor)

        if not sucesso:
            print(f"Falha ao rejeitar fornecedor {id_fornecedor}")

        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao rejeitar fornecedor: {e}")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

# ==================== GESTÃO DE ITENS (VISUALIZAÇÃO E CONTROLE) ====================

@router.get("/admin/itens")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_itens(request: Request, usuario_logado: dict = None):
    """Lista todos os itens do sistema com filtros"""
    try:
        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_item = request.query_params.get("tipo_item", "").strip()
        status_filtro = request.query_params.get("status", "").strip()
        fornecedor_id = request.query_params.get("fornecedor", "").strip()

        # Aplicar filtros se fornecidos, senão listar todos
        if busca:
            itens = item_repo.buscar_itens(busca, 1, 100)
        else:
            itens = item_repo.obter_itens_por_pagina(1, 100)

        # Filtrar por tipo se especificado
        if tipo_item:
            itens = [item for item in itens if item.tipo.value == tipo_item]

        # Filtrar por status se especificado
        if status_filtro == "ativo":
            itens = [item for item in itens if item.ativo]
        elif status_filtro == "inativo":
            itens = [item for item in itens if not item.ativo]

        # Filtrar por fornecedor se especificado
        if fornecedor_id:
            try:
                fornecedor_id_int = int(fornecedor_id)
                itens = [item for item in itens if item.id_fornecedor == fornecedor_id_int]
            except ValueError:
                pass

        # Buscar dados dos fornecedores para exibir nomes
        fornecedores_dados = {}
        for item in itens:
            if item.id_fornecedor not in fornecedores_dados:
                try:
                    fornecedor = fornecedor_repo.obter_fornecedor_por_id(item.id_fornecedor)
                    if fornecedor:
                        fornecedores_dados[item.id_fornecedor] = fornecedor
                except Exception as e:
                    print(f"Erro ao buscar fornecedor {item.id_fornecedor}: {e}")
                    continue

        # Buscar todos os fornecedores para o filtro
        todos_fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 1000)

        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "itens": itens,
            "fornecedores_dados": fornecedores_dados,
            "todos_fornecedores": todos_fornecedores,
            "tipos_item": [tipo for tipo in TipoItem]
        })
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar itens"
        })

@router.get("/admin/item/{id_item}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def visualizar_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Visualiza detalhes de um item específico"""
    try:
        item = item_repo.obter_item_por_id(id_item)

        if not item:
            return templates.TemplateResponse("admin/itens.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Item não encontrado"
            })

        # Buscar dados do fornecedor
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(item.id_fornecedor)

        return templates.TemplateResponse("admin/item_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "item": item,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao visualizar item: {e}")
        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar item"
        })

@router.post("/admin/item/{id_item}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_item_admin(request: Request, id_item: int, usuario_logado: dict = None):
    """Ativa um item (admin pode ativar qualquer item)"""
    try:
        from util.database import obter_conexao
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE item SET ativo = 1 WHERE id = ?", (id_item,))
            sucesso = cursor.rowcount > 0

        if not sucesso:
            print(f"Falha ao ativar item {id_item}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao ativar item: {e}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/item/{id_item}/desativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def desativar_item_admin(request: Request, id_item: int, usuario_logado: dict = None):
    """Desativa um item (admin pode desativar qualquer item)"""
    try:
        from util.database import obter_conexao
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE item SET ativo = 0 WHERE id = ?", (id_item,))
            sucesso = cursor.rowcount > 0

        if not sucesso:
            print(f"Falha ao desativar item {id_item}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao desativar item: {e}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)

# ==================== RELATÓRIOS ====================

@router.get("/admin/relatorios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def relatorios(request: Request, usuario_logado: dict = None):
    """Página de relatórios e estatísticas"""
    try:
        # Estatísticas gerais do sistema
        stats_gerais = {
            "total_usuarios": usuario_repo.contar_usuarios(),
            "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
            "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
            "total_fornecedores": fornecedor_repo.contar_fornecedores(),
            "fornecedores_verificados": fornecedor_repo.contar_fornecedores() - fornecedor_repo.contar_fornecedores_nao_verificados(),
            "fornecedores_nao_verificados": fornecedor_repo.contar_fornecedores_nao_verificados(),
            "total_itens": item_repo.contar_itens(),
            "total_categorias": categoria_item_repo.contar_categorias(),
            "total_orcamentos": orcamento_repo.contar_orcamentos(),
            "total_demandas": demanda_repo.contar_demandas()
        }

        # Estatísticas de itens por tipo
        stats_itens = {
            "produtos": item_repo.contar_itens_por_tipo(TipoItem.PRODUTO),
            "servicos": item_repo.contar_itens_por_tipo(TipoItem.SERVICO),
            "espacos": item_repo.contar_itens_por_tipo(TipoItem.ESPACO),
            "detalhes_por_tipo": item_repo.obter_estatisticas_itens()
        }

        # Estatísticas de fornecedores por categoria
        try:
            fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 1000)
            stats_fornecedores = {
                "prestadores": len([f for f in fornecedores if f.prestador]),
                "vendedores": len([f for f in fornecedores if f.vendedor]),
                "locadores": len([f for f in fornecedores if f.locador]),
                "verificados": len([f for f in fornecedores if f.verificado]),
                "nao_verificados": len([f for f in fornecedores if not f.verificado])
            }
        except:
            stats_fornecedores = {
                "prestadores": 0,
                "vendedores": 0,
                "locadores": 0,
                "verificados": 0,
                "nao_verificados": 0
            }

        # Calcular percentuais
        total_usuarios = stats_gerais["total_usuarios"]
        percentuais = {
            "noivos": round((stats_gerais["total_noivos"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "fornecedores": round((stats_gerais["total_fornecedores"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "admins": round((stats_gerais["total_admins"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "fornecedores_verificados": round((stats_gerais["fornecedores_verificados"] / stats_gerais["total_fornecedores"] * 100) if stats_gerais["total_fornecedores"] > 0 else 0, 1)
        }

        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats_gerais": stats_gerais,
            "stats_itens": stats_itens,
            "stats_fornecedores": stats_fornecedores,
            "percentuais": percentuais
        })
    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")
        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao gerar relatórios"
        })

@router.get("/admin/relatorios/exportar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def exportar_relatorios(request: Request, formato: str = "json", usuario_logado: dict = None):
    """Exporta relatórios em formato JSON ou CSV"""
    try:
        from fastapi.responses import JSONResponse, PlainTextResponse
        from datetime import datetime

        # Coletar todos os dados
        dados = {
            "data_geracao": datetime.now().isoformat(),
            "sistema": {
                "total_usuarios": usuario_repo.contar_usuarios(),
                "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
                "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
                "total_fornecedores": fornecedor_repo.contar_fornecedores(),
                "fornecedores_verificados": fornecedor_repo.contar_fornecedores() - fornecedor_repo.contar_fornecedores_nao_verificados(),
                "fornecedores_nao_verificados": fornecedor_repo.contar_fornecedores_nao_verificados(),
                "total_itens": item_repo.contar_itens(),
                "total_categorias": categoria_item_repo.contar_categorias(),
                "total_orcamentos": orcamento_repo.contar_orcamentos(),
                "total_demandas": demanda_repo.contar_demandas()
            },
            "itens": {
                "produtos": item_repo.contar_itens_por_tipo(TipoItem.PRODUTO),
                "servicos": item_repo.contar_itens_por_tipo(TipoItem.SERVICO),
                "espacos": item_repo.contar_itens_por_tipo(TipoItem.ESPACO),
                "detalhes": item_repo.obter_estatisticas_itens()
            }
        }

        if formato.lower() == "csv":
            # Gerar CSV
            csv_content = "Categoria,Subcategoria,Valor\n"

            # Dados do sistema
            for chave, valor in dados["sistema"].items():
                csv_content += f"Sistema,{chave.replace('_', ' ').title()},{valor}\n"

            # Dados de itens
            for chave, valor in dados["itens"].items():
                if chave != "detalhes":
                    csv_content += f"Itens,{chave.replace('_', ' ').title()},{valor}\n"

            # Detalhes dos itens
            if dados["itens"]["detalhes"]:
                for item in dados["itens"]["detalhes"]:
                    csv_content += f"Detalhes Itens,{item['tipo']},{item['quantidade']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Médio,{item['preco_medio']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Mínimo,{item['preco_minimo']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Máximo,{item['preco_maximo']}\n"

            return PlainTextResponse(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=relatorio_case_bem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
            )
        else:
            # Retornar JSON
            return JSONResponse(content=dados)

    except Exception as e:
        print(f"Erro ao exportar relatórios: {e}")
        return JSONResponse(
            content={"erro": "Erro ao exportar relatórios"},
            status_code=500
        )

# ==================== CATEGORIAS DE ITEM ====================

@router.get("/admin/categorias")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_categorias(request: Request, usuario_logado: dict = None):
    """Lista todas as categorias de item com filtros"""
    try:
        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_fornecimento = request.query_params.get("tipo_fornecimento", "").strip()
        status_filtro = request.query_params.get("status", "").strip()

        # Aplicar filtros se fornecidos, senão listar todas
        if busca or tipo_fornecimento or status_filtro:
            categorias = categoria_item_repo.buscar_categorias(busca, tipo_fornecimento, status_filtro)
        else:
            categorias = categoria_item_repo.obter_todas_categorias()

        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categorias": categorias,
            "tipos_item": [tipo for tipo in TipoItem]
        })
    except Exception as e:
        print(f"Erro ao listar categorias: {e}")
        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar categorias"
        })

@router.get("/admin/categoria/nova")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def nova_categoria(request: Request, usuario_logado: dict = None):
    """Formulário para criar nova categoria"""
    return templates.TemplateResponse("admin/categoria_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "tipos_item": [tipo for tipo in TipoItem],
        "acao": "criar"
    })

@router.post("/admin/categoria/criar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def criar_categoria(
    request: Request,
    nome: str = Form(...),
    tipo_fornecimento: str = Form(...),
    descricao: str = Form(""),
    ativo: bool = Form(True),
    usuario_logado: dict = None
):
    """Cria uma nova categoria"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "criar",
                "erro": "Nome da categoria é obrigatório"
            })

        # Verificar se já existe categoria com o mesmo nome e tipo
        categoria_existente = categoria_item_repo.obter_categoria_por_nome(nome, TipoItem(tipo_fornecimento))
        if categoria_existente:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "criar",
                "erro": f"Já existe uma categoria '{nome}' para o tipo {tipo_fornecimento.capitalize()}"
            })

        categoria = CategoriaItem(
            id=0,
            nome=nome,
            tipo_fornecimento=TipoItem(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        categoria_id = categoria_item_repo.inserir_categoria_item(categoria)
        if categoria_id:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "criar",
                "erro": "Erro ao criar categoria"
            })
    except Exception as e:
        print(f"Erro ao criar categoria: {e}")
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "criar",
            "erro": "Erro ao criar categoria"
        })

@router.get("/admin/categoria/editar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def editar_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Formulário para editar categoria"""
    try:
        categoria = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
        if not categoria:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "editar"
        })
    except Exception as e:
        print(f"Erro ao carregar categoria para edição: {e}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/categoria/atualizar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_categoria(
    request: Request,
    id_categoria: int,
    nome: str = Form(...),
    tipo_fornecimento: str = Form(...),
    descricao: str = Form(""),
    ativo: bool = Form(True),
    usuario_logado: dict = None
):
    """Atualiza uma categoria existente"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "editar",
                "erro": "Nome da categoria é obrigatório"
            })

        # Verificar se já existe outra categoria com o mesmo nome e tipo
        categoria_existente = categoria_item_repo.obter_categoria_por_nome(nome, TipoItem(tipo_fornecimento))
        if categoria_existente and categoria_existente.id != id_categoria:
            categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "editar",
                "erro": f"Já existe outra categoria '{nome}' para o tipo {tipo_fornecimento.capitalize()}"
            })

        categoria = CategoriaItem(
            id=id_categoria,
            nome=nome,
            tipo_fornecimento=TipoItem(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        if categoria_item_repo.atualizar_categoria_item(categoria):
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "editar",
                "erro": "Erro ao atualizar categoria"
            })
    except Exception as e:
        print(f"Erro ao atualizar categoria: {e}")
        categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria_atual,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "editar",
            "erro": "Erro ao atualizar categoria"
        })

@router.post("/admin/categoria/excluir/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def excluir_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Exclui uma categoria"""
    try:
        categoria_item_repo.excluir_categoria_item(id_categoria)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/categoria/{id_categoria}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Ativa uma categoria"""
    try:
        sucesso = categoria_item_repo.ativar_categoria(id_categoria)
        if not sucesso:
            print(f"Falha ao ativar categoria {id_categoria}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao ativar categoria: {e}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/categoria/{id_categoria}/desativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def desativar_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Desativa uma categoria"""
    try:
        sucesso = categoria_item_repo.desativar_categoria(id_categoria)
        if not sucesso:
            print(f"Falha ao desativar categoria {id_categoria}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao desativar categoria: {e}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

# ==================== CONFIGURAÇÕES ====================

@router.get("/admin/configuracoes")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def configuracoes(request: Request, usuario_logado: dict = None):
    """Página de configurações do sistema"""
    return templates.TemplateResponse("admin/configuracoes.html", {
        "request": request,
        "usuario_logado": usuario_logado
    })