from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
async def get_root():
    response = templates.TemplateResponse("usuario/alterar_senha.html", {"request": {}})
    return response

@router.get("/usuario/conversas")
async def get_root():
    response = templates.TemplateResponse("usuario/conversas.html", {"request": {}})
    return response

@router.get("/usuario/conversas/{id_conversa}")
async def get_root(id_conversa: int):    
    response = templates.TemplateResponse("usuario/chat.html", {"request": {}})
    return response