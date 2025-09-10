@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
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
    
    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
    
    if usuario.perfil == "admin":
        return RedirectResponse("/admin", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)