import os
from fastapi import APIRouter, HTTPException, Request
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repo import produto_repo, usuario_repo
from fastapi import status
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("usuario/alterar_senha.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/usuario/conversas")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("usuario/conversas.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/usuario/conversas/{id_conversa}")
@requer_autenticacao()
async def get_root(id_conversa: int, request: Request, usuario_logado: dict = None):    
    response = templates.TemplateResponse("usuario/chat.html", {"request": request, "usuario": usuario_logado})
    return response

@router.post("/produto/excluir/{id}")
@requer_autenticacao()
async def excluir_produto(id: int, usuario_logado: dict = None):
    # Verificar permissão adicional
    if usuario_logado['perfil'] != 'admin':
        raise HTTPException(403, "Apenas admins podem excluir produtos")
    
    produto_repo.excluir(id)
    return RedirectResponse("/produtos", status.HTTP_303_SEE_OTHER)

# routes/perfil_routes.py

@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: dict = None
):
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)