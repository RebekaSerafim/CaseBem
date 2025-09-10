@router.post("/cadastro")
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cpf: str = Form(None),
    telefone: str = Form(None)
):
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "Email já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)
    
    # Criar usuário
    usuario = Usuario(
        id=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        perfil="cliente"
    )
    
    usuario_id = usuario_repo.inserir(usuario)
    
    # Se tiver CPF/telefone, inserir na tabela cliente
    if cpf and telefone:
        cliente = Cliente(
            id=usuario_id,
            cpf=cpf,
            telefone=telefone
        )
        cliente_repo.inserir(cliente)
    
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)