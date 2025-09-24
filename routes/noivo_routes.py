from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.item_model import TipoItem
from model.demanda_model import Demanda
from repo import usuario_repo, item_repo, demanda_repo, orcamento_repo, casal_repo, favorito_repo, fornecedor_repo
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

def get_noivo_active_page(request: Request) -> str:
    """Determina qual página está ativa na área noivo"""
    url_path = str(request.url.path)

    if url_path == "/noivo/dashboard":
        return "dashboard"
    elif url_path == "/noivo/perfil":
        return "perfil"
    elif url_path.startswith("/noivo/fornecedores"):
        return "fornecedores"
    elif url_path.startswith("/noivo/demandas"):
        return "demandas"
    elif url_path.startswith("/noivo/orcamentos"):
        return "orcamentos"
    elif url_path.startswith("/noivo/checklist"):
        return "checklist"
    elif url_path.startswith("/noivo/favoritos"):
        return "favoritos"
    else:
        return ""

# ==================== REDIRECIONAMENTO RAIZ ====================

@router.get("/noivo")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def noivo_root(request: Request, usuario_logado: dict = None):
    """Redireciona /noivo para /noivo/dashboard"""
    return RedirectResponse("/noivo/dashboard", status_code=status.HTTP_302_FOUND)

# ==================== DASHBOARD ====================

@router.get("/noivo/dashboard")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def dashboard_noivo(request: Request, usuario_logado: dict = None):
    """Dashboard principal dos noivos"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar dados do noivo
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        # Buscar dados do casal
        try:
            casal = casal_repo.obter_casal_por_noivo(id_noivo)
        except:
            casal = None

        # Buscar demandas do casal
        try:
            if casal:
                demandas_casal = demanda_repo.obter_demandas_por_casal(casal.id)
                demandas_ativas = [d for d in demandas_casal if d.status.value == 'ATIVA']
                demandas_recentes = demandas_casal[:5]
            else:
                demandas_casal = []
                demandas_ativas = []
                demandas_recentes = []
        except:
            demandas_casal = []
            demandas_ativas = []
            demandas_recentes = []

        # Buscar orçamentos do noivo
        try:
            orcamentos_recebidos = orcamento_repo.obter_orcamentos_por_noivo(id_noivo)
            orcamentos_pendentes = [o for o in orcamentos_recebidos if o.status == 'PENDENTE']
        except:
            orcamentos_recebidos = []
            orcamentos_pendentes = []

        # Estatísticas para o noivo
        stats = {
            "demandas_ativas": len(demandas_ativas),
            "orcamentos_recebidos": len(orcamentos_recebidos),
            "orcamentos_pendentes": len(orcamentos_pendentes),
            "favoritos": favorito_repo.contar_favoritos_por_noivo(id_noivo)
        }

        return templates.TemplateResponse("noivo/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "casal": casal,
            "stats": stats,
            "demandas_recentes": demandas_recentes
        })
    except Exception as e:
        print(f"Erro no dashboard noivo: {e}")
        return templates.TemplateResponse("noivo/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar dashboard"
        })

# ==================== EXPLORAR ITENS ====================

@router.get("/noivo/produtos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_produtos(request: Request, usuario_logado: dict = None):
    """Lista produtos disponíveis"""
    try:
        produtos = item_repo.obter_produtos()

        return templates.TemplateResponse("noivo/produtos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "produtos": produtos
        })
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return templates.TemplateResponse("noivo/produtos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar produtos"
        })

@router.get("/noivo/servicos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_servicos(request: Request, usuario_logado: dict = None):
    """Lista serviços disponíveis"""
    try:
        servicos = item_repo.obter_servicos()

        return templates.TemplateResponse("noivo/servicos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "servicos": servicos
        })
    except Exception as e:
        print(f"Erro ao listar serviços: {e}")
        return templates.TemplateResponse("noivo/servicos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar serviços"
        })

@router.get("/noivo/espacos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_espacos(request: Request, usuario_logado: dict = None):
    """Lista espaços disponíveis"""
    try:
        espacos = item_repo.obter_espacos()

        return templates.TemplateResponse("noivo/espacos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "espacos": espacos
        })
    except Exception as e:
        print(f"Erro ao listar espaços: {e}")
        return templates.TemplateResponse("noivo/espacos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar espaços"
        })

@router.get("/noivo/buscar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def buscar_itens(request: Request, q: str = "", usuario_logado: dict = None):
    """Busca itens por termo"""
    try:
        resultados = []
        if q.strip():
            resultados = item_repo.buscar_itens(q.strip())

        return templates.TemplateResponse("noivo/buscar.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "resultados": resultados,
            "termo_busca": q
        })
    except Exception as e:
        print(f"Erro na busca: {e}")
        return templates.TemplateResponse("noivo/buscar.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro na busca",
            "termo_busca": q
        })

# ==================== DETALHES DE ITENS ====================

@router.get("/noivo/item/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def visualizar_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Visualiza detalhes de um item"""
    try:
        item = item_repo.obter_item_por_id(id_item)

        if not item or not item.ativo:
            return templates.TemplateResponse("noivo/item_nao_encontrado.html", {
                "request": request,
                "usuario_logado": usuario_logado
            })

        # Buscar dados do fornecedor
        fornecedor = None
        try:
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(item.id_fornecedor)
        except Exception as e:
            print(f"Erro ao buscar fornecedor {item.id_fornecedor}: {e}")

        return templates.TemplateResponse("noivo/item_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "item": item,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao visualizar item: {e}")
        return templates.TemplateResponse("noivo/item_nao_encontrado.html", {
            "request": request,
            "usuario_logado": usuario_logado
        })

# ==================== DEMANDAS ====================

@router.get("/noivo/demandas")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_demandas(request: Request, status: str = "", search: str = "", usuario_logado: dict = None):
    """Lista demandas do noivo"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar casal do noivo
        casal = casal_repo.obter_casal_por_noivo(id_noivo)
        if not casal:
            return templates.TemplateResponse("noivo/demandas.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Casal não encontrado"
            })

        # Buscar demandas do casal
        demandas = demanda_repo.obter_demandas_por_casal(casal.id)

        # Aplicar filtros
        if status:
            demandas = [d for d in demandas if d.status.value == status]

        if search:
            demandas = [d for d in demandas if search.lower() in d.titulo.lower() or search.lower() in d.descricao.lower()]

        # TODO: Implementar paginação real

        return templates.TemplateResponse("noivo/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "demandas": demandas
        })
    except Exception as e:
        print(f"Erro ao listar demandas: {e}")
        return templates.TemplateResponse("noivo/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar demandas"
        })

@router.get("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def nova_demanda_form(request: Request, usuario_logado: dict = None):
    """Formulário para criar nova demanda"""
    return templates.TemplateResponse("noivo/demanda_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar"
    })

@router.post("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def criar_demanda(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    id_categoria: int = Form(...),
    orcamento_min: float = Form(None),
    orcamento_max: float = Form(None),
    prazo_entrega: str = Form(""),
    observacoes: str = Form(""),
    usuario_logado: dict = None
):
    """Cria uma nova demanda"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar casal do noivo
        casal = casal_repo.obter_casal_por_noivo(id_noivo)
        if not casal:
            return templates.TemplateResponse("noivo/demanda_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Casal não encontrado",
                "acao": "criar"
            })

        # Criar nova demanda
        nova_demanda = Demanda(
            id=0,  # Será definido pelo banco
            id_casal=casal.id,
            id_categoria=id_categoria,
            titulo=titulo,
            descricao=descricao,
            orcamento_min=orcamento_min if orcamento_min else None,
            orcamento_max=orcamento_max if orcamento_max else None,
            prazo_entrega=prazo_entrega if prazo_entrega else None,
            observacoes=observacoes if observacoes else None
        )

        # Inserir no banco
        id_demanda = demanda_repo.inserir_demanda(nova_demanda)

        if id_demanda:
            return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("noivo/demanda_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao criar demanda no banco de dados",
                "acao": "criar"
            })

    except Exception as e:
        print(f"Erro ao criar demanda: {e}")
        return templates.TemplateResponse("noivo/demanda_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao criar demanda",
            "acao": "criar"
        })

# ==================== ORÇAMENTOS ====================

@router.get("/noivo/orcamentos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_orcamentos(request: Request, status: str = "", demanda: str = "", search: str = "", usuario_logado: dict = None):
    """Lista orçamentos recebidos"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar orçamentos do noivo
        orcamentos = orcamento_repo.obter_orcamentos_por_noivo(id_noivo)

        # Aplicar filtros
        if status:
            orcamentos = [o for o in orcamentos if o.status == status]

        if demanda:
            orcamentos = [o for o in orcamentos if str(o.id_demanda) == demanda]

        if search:
            # Buscar por nome do fornecedor (precisamos buscar os dados do fornecedor)
            orcamentos_filtrados = []
            for orcamento in orcamentos:
                try:
                    fornecedor = fornecedor_repo.obter_fornecedor_por_id(orcamento.id_fornecedor)
                    if fornecedor and search.lower() in fornecedor.nome.lower():
                        orcamentos_filtrados.append(orcamento)
                except:
                    continue
            orcamentos = orcamentos_filtrados

        # Buscar casal do noivo
        casal = casal_repo.obter_casal_por_noivo(id_noivo)

        # Buscar demandas do casal para o filtro
        minhas_demandas = demanda_repo.obter_demandas_por_casal(casal.id) if casal else []

        # Enriquecer orçamentos com dados adicionais
        orcamentos_enriched = []
        for orcamento in orcamentos:
            try:
                # Buscar dados da demanda
                demanda_data = demanda_repo.obter_demanda_por_id(orcamento.id_demanda)
                # Buscar dados do fornecedor
                fornecedor_data = fornecedor_repo.obter_fornecedor_por_id(orcamento.id_fornecedor)
                # Buscar itens do orçamento
                itens_orcamento = item_orcamento_repo.obter_itens_por_orcamento(orcamento.id)

                orcamento_dict = {
                    "id": orcamento.id,
                    "id_demanda": orcamento.id_demanda,
                    "id_fornecedor": orcamento.id_fornecedor,
                    "status": orcamento.status,
                    "valor_total": orcamento.valor_total,
                    "data_envio": orcamento.data_envio,
                    "prazo_entrega": orcamento.prazo_entrega,
                    "observacoes": orcamento.observacoes,
                    "demanda_titulo": demanda_data.titulo if demanda_data else "Demanda não encontrada",
                    "fornecedor_nome": fornecedor_data.nome if fornecedor_data else "Fornecedor não encontrado",
                    "itens_count": len(itens_orcamento)
                }
                orcamentos_enriched.append(orcamento_dict)
            except Exception as e:
                print(f"Erro ao enriquecer orçamento {orcamento.id}: {e}")
                continue

        return templates.TemplateResponse("noivo/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": orcamentos_enriched,
            "minhas_demandas": minhas_demandas
        })
    except Exception as e:
        print(f"Erro ao listar orçamentos: {e}")
        return templates.TemplateResponse("noivo/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar orçamentos"
        })

@router.get("/noivo/orcamentos/{id_orcamento}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def visualizar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Visualiza detalhes de um orçamento"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar orçamento
        orcamento = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        if not orcamento:
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

        # Buscar demanda relacionada
        demanda = demanda_repo.obter_demanda_por_id(orcamento.id_demanda)

        # Buscar casal do noivo
        casal = casal_repo.obter_casal_por_noivo(id_noivo)

        if not demanda or not casal or demanda.id_casal != casal.id:
            # Verificar se o orçamento pertence ao casal do noivo logado
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

        # Buscar fornecedor
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(orcamento.id_fornecedor)

        # Buscar itens do orçamento
        itens_orcamento = item_orcamento_repo.obter_itens_por_orcamento(orcamento.id)

        # Enriquecer itens com dados do item
        itens_enriched = []
        for item_orc in itens_orcamento:
            try:
                item_data = item_repo.obter_item_por_id(item_orc.id_item)
                item_dict = {
                    "id_item": item_orc.id_item,
                    "nome_item": item_data.nome if item_data else "Item não encontrado",
                    "descricao_item": item_data.descricao if item_data else "",
                    "tipo_item": item_data.tipo.value if item_data else "",
                    "quantidade": item_orc.quantidade,
                    "preco_unitario": item_orc.preco_unitario,
                    "desconto": item_orc.desconto or 0,
                    "preco_total": item_orc.preco_total,
                    "observacoes": item_orc.observacoes
                }
                itens_enriched.append(item_dict)
            except Exception as e:
                print(f"Erro ao enriquecer item {item_orc.id_item}: {e}")
                continue

        # Criar objeto orçamento enriquecido
        orcamento_enriched = {
            "id": orcamento.id,
            "id_demanda": orcamento.id_demanda,
            "id_fornecedor": orcamento.id_fornecedor,
            "status": orcamento.status,
            "valor_total": orcamento.valor_total,
            "data_envio": orcamento.data_envio,
            "prazo_entrega": orcamento.prazo_entrega,
            "observacoes": orcamento.observacoes,
            "desconto": orcamento.desconto or 0,
            "data_resposta": getattr(orcamento, 'data_resposta', None),
            "itens": itens_enriched
        }

        return templates.TemplateResponse("noivo/orcamento_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamento": orcamento_enriched,
            "demanda": demanda,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao visualizar orçamento: {e}")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/noivo/orcamentos/{id_orcamento}/aceitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def aceitar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Aceita um orçamento"""
    try:
        # Buscar o orçamento para obter o id_demanda
        orcamento = orcamento_repo.obter_orcamento_por_id(id_orcamento)
        if not orcamento:
            return RedirectResponse("/noivo/orcamentos?erro=orcamento_nao_encontrado", status_code=status.HTTP_303_SEE_OTHER)

        # Aceitar este orçamento e rejeitar os outros da mesma demanda
        sucesso = orcamento_repo.aceitar_orcamento_e_rejeitar_outros(id_orcamento, orcamento.id_demanda)

        if sucesso:
            informar_sucesso(request, "Orçamento aceito com sucesso!")
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao aceitar orçamento!")
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        informar_erro(request, "Erro interno ao aceitar orçamento!")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/noivo/orcamentos/{id_orcamento}/rejeitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def rejeitar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Rejeita um orçamento"""
    try:
        # Rejeitar o orçamento
        sucesso = orcamento_repo.rejeitar_orcamento(id_orcamento)

        if sucesso:
            informar_sucesso(request, "Orçamento rejeitado com sucesso!")
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao rejeitar orçamento!")
            return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao rejeitar orçamento: {e}")
        informar_erro(request, "Erro interno ao rejeitar orçamento!")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

# ==================== PERFIL E CASAL ====================

@router.get("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def perfil_noivo(request: Request, usuario_logado: dict = None):
    """Página de perfil do noivo"""
    try:
        id_noivo = usuario_logado["id"]
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        # Buscar dados do casal
        casal = None
        try:
            casal = casal_repo.obter_casal_por_noivo(id_noivo)
        except Exception as e:
            print(f"Erro ao buscar dados do casal: {e}")

        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "casal": casal
        })
    except Exception as e:
        print(f"Erro ao carregar perfil: {e}")
        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar perfil"
        })

@router.post("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def atualizar_perfil_noivo(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(""),
    data_nascimento: str = Form(""),
    usuario_logado: dict = None
):
    """Atualiza perfil do noivo"""
    try:
        id_noivo = usuario_logado["id"]
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        if not noivo:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Atualizar dados
        noivo.nome = nome
        noivo.email = email
        noivo.telefone = telefone
        noivo.cpf = cpf if cpf else None
        noivo.data_nascimento = data_nascimento if data_nascimento else None

        sucesso = usuario_repo.atualizar_usuario(noivo)

        if sucesso:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "sucesso": "Perfil atualizado com sucesso!"
            })
        else:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "erro": "Erro ao atualizar perfil"
            })

    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor"
        })

# ==================== FAVORITOS ====================

@router.get("/noivo/favoritos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_favoritos(request: Request, usuario_logado: dict = None):
    """Lista itens favoritos do noivo"""
    try:
        id_noivo = usuario_logado["id"]
        favoritos = favorito_repo.obter_favoritos_por_noivo(id_noivo)

        return templates.TemplateResponse("noivo/favoritos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "favoritos": favoritos
        })
    except Exception as e:
        print(f"Erro ao listar favoritos: {e}")
        return templates.TemplateResponse("noivo/favoritos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar favoritos"
        })

@router.post("/noivo/favoritos/adicionar/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def adicionar_favorito(request: Request, id_item: int, usuario_logado: dict = None):
    """Adiciona um item aos favoritos"""
    try:
        id_noivo = usuario_logado["id"]
        sucesso = favorito_repo.adicionar_favorito(id_noivo, id_item)

        if sucesso:
            return {"success": True, "message": "Item adicionado aos favoritos"}
        else:
            return {"success": False, "message": "Erro ao adicionar favorito"}
    except Exception as e:
        print(f"Erro ao adicionar favorito: {e}")
        return {"success": False, "message": "Erro interno"}

@router.post("/noivo/favoritos/remover/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def remover_favorito(request: Request, id_item: int, usuario_logado: dict = None):
    """Remove um item dos favoritos"""
    try:
        id_noivo = usuario_logado["id"]
        sucesso = favorito_repo.remover_favorito(id_noivo, id_item)

        if sucesso:
            return {"success": True, "message": "Item removido dos favoritos"}
        else:
            return {"success": False, "message": "Erro ao remover favorito"}
    except Exception as e:
        print(f"Erro ao remover favorito: {e}")
        return {"success": False, "message": "Erro interno"}